"""
Configuration du bot Telegram - Compatible v20+
"""

import os
import logging
from telegram.ext import Application

logger = logging.getLogger(__name__)


class FiboBotManager:
    """Gestionnaire du bot Telegram"""

    def __init__(self):
        self.application = None

    async def setup(self):
        """Configurer le bot"""
        try:
            token = os.environ.get('TELEGRAM_TOKEN_FIBOBOT')
            if not token:
                raise ValueError("TELEGRAM_TOKEN_FIBOBOT non défini")

            # Nouvelle API v20+
            self.application = Application.builder().token(token).build()
            
            logger.info("✅ Bot Telegram configuré avec succès")
            return self.application

        except Exception as e:
            logger.error(f"Erreur configuration bot: {e}")
            raise

    def start(self):
        """Démarrer le bot (non-async pour le scheduler)"""
        if self.application:
            self.application.run_polling()
