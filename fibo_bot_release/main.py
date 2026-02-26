#!/usr/bin/env python3
"""
Point d'entrée du Forex Fibonacci Bot

Usage:
    python main.py
    
Les variables d'environnement doivent être définies:
    - TELEGRAM_TOKEN_FIBOBOT
    - TWELVEDATA_API_KEY_FIBOBOT
"""

import asyncio
import signal
import sys
from config.secrets import Secrets
from config.settings import PAIRS
from data.twelvedata_client import TwelveDataClient
from data.database import Database
from bot.telegram_bot import FiboBotManager
from bot.handlers import CommandHandlers
from scheduler.jobs import SchedulerManager
from utils.logger import setup_logger
from telegram.ext import CommandHandler, MessageHandler, filters

logger = setup_logger(__name__)


class FiboBotApplication:
    """Application principale du bot Fibonacci"""

    def __init__(self):
        """Initialiser l'application"""
        self.api_client = None
        self.db = None
        self.bot_manager = None
        self.scheduler_manager = None
        self.app = None
        self.chat_id = None

    async def initialize(self):
        """Initialiser tous les composants"""
        try:
            logger.info("🚀 Initialisation du Forex Fibonacci Bot...")

            # Initialiser les secrets
            telegram_token = Secrets.get_telegram_token()
            twelvedata_key = Secrets.get_twelvedata_api_key()

            logger.info(f"✅ Secrets chargés")

            # Initialiser le client API
            self.api_client = TwelveDataClient(twelvedata_key)
            logger.info(f"✅ Client Twelve Data initialisé")

            # Initialiser la base de données
            self.db = Database("fibo_bot.db")
            logger.info(f"✅ Base de données initialisée")

            # Initialiser le bot Telegram
            self.bot_manager = FiboBotManager()
            self.app = await self.bot_manager.setup()
            logger.info(f"✅ Bot Telegram configuré")

            # Initialiser les handlers
            handlers = CommandHandlers(self.db)

            self.app.add_handler(CommandHandler("start", handlers.handle_start))
            self.app.add_handler(CommandHandler("status", handlers.handle_status))
            self.app.add_handler(CommandHandler("pairs", handlers.handle_pairs))
            self.app.add_handler(CommandHandler("history", handlers.handle_history))
            self.app.add_handler(CommandHandler("stats", handlers.handle_stats))

            self.app.add_error_handler(handlers.handle_error)

            logger.info(f"✅ Handlers Telegram configurés")

            # Pour les tests, utiliser un chat_id par défaut
            # En production, ce serait configuré différemment
            self.chat_id = 0  # À remplacer par l'ID du chat réel

            # Initialiser le scheduler
            self.scheduler_manager = SchedulerManager(
                self.api_client,
                self.db,
                self.bot_manager,
                self.chat_id,
            )
            scheduler = self.scheduler_manager.setup()
            logger.info(f"✅ Scheduler configuré")

            logger.info(f"✅ Bot Fibonacci initialisé avec succès!")
            logger.info(f"📊 Paires surveillées: {', '.join(PAIRS)}")
            logger.info(f"💾 Crédits API: {self.api_client.get_credits_remaining()}/800")

            return True

        except Exception as e:
            logger.error(f"❌ Erreur initialisation: {e}")
            return False

    async def start(self):
        """Démarrer le bot"""
        try:
            if not await self.initialize():
                logger.error("Impossible d'initialiser le bot")
                return False

            logger.info("🎯 Démarrage du bot...")

            # Démarrer le scheduler
            self.scheduler_manager.start()

            # Démarrer le bot Telegram
            async with self.app:
                await self.app.initialize()
                await self.app.start()
                logger.info("✅ Bot Telegram démarré")

                # Garder le bot en cours d'exécution
                await self.app.updater.start_polling()
                logger.info("✅ Polling Telegram démarré")

                # Attendre indéfiniment
                await asyncio.Event().wait()

        except Exception as e:
            logger.error(f"❌ Erreur démarrage: {e}")
            return False

    async def stop(self):
        """Arrêter le bot"""
        try:
            logger.info("🛑 Arrêt du bot...")

            if self.scheduler_manager:
                self.scheduler_manager.stop()

            if self.app:
                await self.app.stop()

            logger.info("✅ Bot arrêté")

        except Exception as e:
            logger.error(f"❌ Erreur arrêt: {e}")


async def main():
    """Fonction principale"""
    app = FiboBotApplication()

    def signal_handler(sig, frame):
        """Gestionnaire de signaux"""
        logger.info("Signal reçu, arrêt du bot...")
        asyncio.create_task(app.stop())
        sys.exit(0)

    # Enregistrer les gestionnaires de signaux
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Démarrer le bot
    await app.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot arrêté par l'utilisateur")
    except Exception as e:
        logger.error(f"Erreur fatale: {e}")
        sys.exit(1)
