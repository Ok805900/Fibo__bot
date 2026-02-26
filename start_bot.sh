#!/bin/bash

# Script de démarrage du Forex Fibonacci Bot
# Usage: ./start_bot.sh

echo "=========================================="
echo "🤖 Forex Fibonacci Bot - Démarrage"
echo "=========================================="
echo ""

# Vérifier que .env existe
if [ ! -f .env ]; then
    echo "❌ Erreur: Fichier .env non trouvé"
    echo "Créez le fichier .env avec vos secrets:"
    echo "  TELEGRAM_TOKEN_FIBOBOT=..."
    echo "  TWELVEDATA_API_KEY_FIBOBOT=..."
    exit 1
fi

echo "✅ Fichier .env trouvé"

# Vérifier que Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Erreur: Python3 n'est pas installé"
    exit 1
fi

echo "✅ Python3 trouvé"

# Vérifier les dépendances
echo ""
echo "Vérification des dépendances..."
python3 -c "import telegram; import python_telegram_bot; import apscheduler; import dotenv" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Installation des dépendances..."
    pip install -r requirements.txt
fi

echo "✅ Dépendances OK"

# Créer le répertoire de données s'il n'existe pas
mkdir -p data

echo ""
echo "=========================================="
echo "🚀 Démarrage du bot..."
echo "=========================================="
echo ""

# Lancer le bot
python3 main.py

exit $?
