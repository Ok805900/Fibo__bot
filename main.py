#!/usr/bin/env python3
"""
Point d'entrée du Forex Fibonacci Bot
"""

import asyncio
import signal
import sys
import threading
import os
from flask import Flask
from config.secrets import Secrets
from config.settings import PAIRS
from data.twelvedata_client import TwelveDataClient
from data.database import Database
from bot.telegram_bot import FiboBotManager
from bot.handlers import CommandHandlers
from scheduler.jobs import SchedulerManager
from utils.logger import setup_logger
from telegram.ext import CommandHandler

logger = setup_logger(__name__)

# Serveur web pour UptimeRobot
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return {"status": "alive", "bot": "FiboBot"}

@web_app.route('/health')
def health():
    return {"status": "healthy"}, 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port, threaded=True)


class FiboBotApplication:
    def __init__(self):
        self.api_client = None
        self.db = None
        self.bot_manager = None
        self.scheduler_manager = None
        self.app = None
        self.chat_id = None

    async def initialize(self):
        try:
            logger.info("🚀 Initialisation du Forex Fibonacci Bot...")

            # Initialiser les secrets
            telegram_token = Secrets.get_telegram_token()
            twelvedata_key = Secrets.get_twelvedata_api_key()

            # Initialiser le client API
            self.api_client = TwelveDataClient(twelvedata_key)

            # Initialiser la base de données
            self.db = Database("fibo_bot.db")

            # Initialiser le bot Telegram (nouvelle API v20+)
            self.bot_manager = FiboBotManager()
            self.app = await self.bot_manager.setup()

            # Initialiser les handlers
            handlers = CommandHandlers(self.db)
            self.app.add_handler(CommandHandler("start", handlers.handle_start))
            self.app.add_handler(CommandHandler("status", handlers.handle_status))
            self.app.add_handler(CommandHandler("pairs", handlers.handle_pairs))
            self.app.add_handler(CommandHandler("history", handlers.handle_history))
            self.app.add_handler(CommandHandler("stats", handlers.handle_stats))
            self.app.add_error_handler(handlers.handle_error)

            self.chat_id = 0

            # Initialiser le scheduler
            self.scheduler_manager = SchedulerManager(
                self.api_client, self.db, self.bot_manager, self.chat_id
            )
            self.scheduler_manager.setup()

            logger.info(f"✅ Bot Fibonacci initialisé!")
            logger.info(f"📊 Paires: {', '.join(PAIRS)}")
            return True

        except Exception as e:
            logger.error(f"❌ Erreur initialisation: {e}")
            return False

    async def start(self):
        if not await self.initialize():
            return False

        logger.info("🎯 Démarrage du bot...")

        # Démarrer le scheduler
        self.scheduler_manager.start()

        # Démarrer le bot avec la nouvelle API v20+
        logger.info("✅ Démarrage du polling...")
        await self.app.run_polling()

    async def stop(self):
        logger.info("🛑 Arrêt du bot...")
        if self.scheduler_manager:
            self.scheduler_manager.stop()
        if self.app:
            await self.app.stop()


async def main():
    # Démarrer le serveur web dans un thread séparé
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    logger.info("🌐 Serveur web démarré")

    app = FiboBotApplication()

    def signal_handler(sig, frame):
        asyncio.create_task(app.stop())
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    await app.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot arrêté")
    except Exception as e:
        logger.error(f"Erreur fatale: {e}")
        sys.exit(1)
