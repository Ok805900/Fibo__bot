# ⚡ Quick Start - Forex Fibonacci Bot

## 📦 Contenu du ZIP

```
fibo_bot/
├── config/              # Configuration
│   ├── settings.py      # 14 paires, SMA 200
│   └── secrets.py       # Variables d'environnement
├── core/                # Calculs techniques
│   ├── fibonacci.py     # 4 Fibonacci multi-niveaux ✨
│   ├── heiken_ashi.py   # Bougies Heiken Ashi
│   ├── technical.py     # SMA, RSI, S/R
│   └── scanner.py       # Scanner W1/D1/H1
├── data/                # Données
│   ├── twelvedata_client.py  # API Twelve Data
│   └── database.py      # SQLite
├── bot/                 # Bot Telegram
│   ├── telegram_bot.py
│   └── handlers.py
├── scheduler/           # Jobs automatiques
├── utils/               # Logging
├── main.py              # Point d'entrée
├── requirements.txt     # Dépendances
├── .env.example         # Template variables
├── DEPLOY.md            # Guide déploiement GitHub
└── Procfile             # Heroku
```

## 🚀 Démarrage Local (5 minutes)

### 1. Extraire et Préparer

```bash
unzip fibo_bot.zip
cd fibo_bot_release
```

### 2. Configurer les Secrets

```bash
cp .env.example .env
# Éditer .env avec vos secrets:
# TELEGRAM_TOKEN_FIBOBOT=8605370883:AAH4XVlq3lYVJzmAB9v3OC7J8x_6KLR4klw
# TWELVEDATA_API_KEY_FIBOBOT=9d61193621de4d7f976f78147fa689b1
```

### 3. Installer les Dépendances

```bash
pip install -r requirements.txt
```

### 4. Démarrer le Bot

```bash
python main.py
```

Vous devriez voir:
```
✅ Secrets chargés
✅ Client Twelve Data initialisé
✅ Bot Telegram configuré
✅ Scheduler configuré
🎯 Démarrage du bot...
```

## 🚀 Déploiement GitHub (10 minutes)

Voir le fichier `DEPLOY.md` pour:
- Créer repo GitHub
- Configurer secrets
- Déployer sur Render/Railway/Heroku

## 📊 Fonctionnalités

✨ **4 Fibonacci Multi-Niveaux**
- Mode BULLISH: Sommet → 4 creux
- Mode BEARISH: Creux → 4 sommets
- Détection zone [0.500, 0.618]

📊 **Multi-Timeframe**
- W1: Tendance (SMA 200)
- D1: Confirmation (SMA 200)
- H1: Signaux (Fibonacci + Heiken Ashi)

🔔 **Telegram**
- /start, /status, /pairs, /history, /stats

## 🔑 Variables d'Environnement

```
TELEGRAM_TOKEN_FIBOBOT=...
TWELVEDATA_API_KEY_FIBOBOT=...
LOG_LEVEL=INFO
```

## ✅ Tests

```bash
# Tous les tests
python tests.py

# Tests complets
python test_bot_complete.py

# Tests 4 Fibonacci
python test_4_fibonacci.py
```

## 📞 Commandes Utiles

```bash
# Voir les logs
tail -f bot.log

# Arrêter le bot
Ctrl+C
```

## 🎯 Prochaines Étapes

1. ✅ Configurer `.env`
2. ✅ Installer dépendances
3. ✅ Démarrer localement
4. ✅ Tester les commandes Telegram
5. ✅ Déployer sur GitHub
6. ✅ Déployer en production (Render/Railway/Heroku)

---

**Le bot est prêt à trader! 🚀**

Pour plus de détails: voir `DEPLOY.md`, `README.md`, `DOC_TECHNIQUE.md`
