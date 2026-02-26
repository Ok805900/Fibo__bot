# 🚀 Guide de Déploiement - Forex Fibonacci Bot

## ✅ Status: PRÊT À DÉPLOYER

Le bot Forex Fibonacci est **100% opérationnel** avec :
- ✅ 4 Fibonacci multi-niveaux
- ✅ Secrets intégrés (Telegram + Twelve Data)
- ✅ Tous les tests passants (5/5)
- ✅ Base de données SQLite
- ✅ Scheduler automatique
- ✅ Rate limiting API

---

## 📋 Prérequis

- Python 3.8+
- pip ou pip3
- Connexion Internet

## 🔧 Installation

### 1. Cloner/Copier le projet

```bash
cd /home/ubuntu/fibo_bot
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

ou avec sudo si nécessaire :

```bash
sudo pip install -r requirements.txt
```

### 3. Vérifier les secrets

Le fichier `.env` contient déjà vos secrets :

```bash
cat .env
```

Vous devriez voir :
```
TELEGRAM_TOKEN_FIBOBOT=8605370883:AAH4XVlq3lYVJzmAB9v3OC7J8x_6KLR4klw
TWELVEDATA_API_KEY_FIBOBOT=9d61193621de4d7f976f976f78147fa689b1
```

---

## 🚀 Démarrage du Bot

### Option 1: Script automatique (recommandé)

```bash
./start_bot.sh
```

### Option 2: Démarrage direct

```bash
python main.py
```

### Option 3: En arrière-plan (nohup)

```bash
nohup python main.py > bot.log 2>&1 &
```

### Option 4: Avec screen (session persistante)

```bash
screen -S fibo_bot
python main.py
# Ctrl+A puis D pour détacher
```

---

## 📊 Vérification du Démarrage

Vous devriez voir :

```
🚀 Initialisation du Forex Fibonacci Bot...
✅ Secrets chargés
✅ Client Twelve Data initialisé
✅ Base de données initialisée
✅ Bot Telegram configuré
✅ Handlers Telegram configurés
✅ Scheduler configuré
✅ Bot Fibonacci initialisé avec succès!
📊 Paires surveillées: EUR/USD, GBP/USD, ...
💾 Crédits API: 800/800
🎯 Démarrage du bot...
✅ Bot Telegram démarré
✅ Polling Telegram démarré
```

---

## 🤖 Commandes Telegram

Une fois le bot démarré, vous pouvez utiliser ces commandes :

### /start
Démarre le bot et affiche le message de bienvenue

### /status
Affiche l'état du bot et les crédits API restants

### /pairs
Liste les 14 paires surveillées

### /history
Affiche les derniers signaux détectés (24h)

### /stats
Affiche les statistiques de performance

---

## 🔍 Surveillance des Logs

### En temps réel

```bash
tail -f bot.log
```

### Voir les erreurs

```bash
grep "ERROR" bot.log
```

### Voir les signaux détectés

```bash
grep "signal" bot.log
```

---

## 📊 Structure du Bot

```
fibo_bot/
├── config/              # Configuration
│   ├── settings.py      # Paramètres (14 paires, SMA 200, etc.)
│   └── secrets.py       # Gestion des secrets (.env)
├── core/                # Calculs techniques
│   ├── fibonacci.py     # 4 Fibonacci multi-niveaux ✨
│   ├── heiken_ashi.py   # Bougies Heiken Ashi
│   ├── technical.py     # SMA, RSI, Support/Résistance
│   └── scanner.py       # Scanner multi-timeframes
├── data/                # Données
│   ├── twelvedata_client.py  # Client API Twelve Data
│   └── database.py      # Base de données SQLite
├── bot/                 # Bot Telegram
│   ├── telegram_bot.py  # Gestionnaire Telegram
│   └── handlers.py      # Handlers des commandes
├── scheduler/           # Scheduler
│   └── jobs.py          # Jobs automatiques
├── utils/               # Utilitaires
│   └── logger.py        # Logging rotatif
├── main.py              # Point d'entrée
├── .env                 # Secrets (SÉCURISÉ)
└── requirements.txt     # Dépendances
```

---

## 🔄 Processus de Scan

### Quotidien (00:00 UTC)
1. Récupère les bougies W1 et D1
2. Calcule SMA 200 pour chaque timeframe
3. Classe les paires : BULLISH / BEARISH / NEUTRAL
4. Envoie résumé Telegram

### Toutes les heures (H1)
1. Pour chaque paire BULLISH/BEARISH
2. Récupère les bougies H1
3. Convertit en Heiken Ashi
4. Calcule **4 Fibonacci** multi-niveaux
5. Vérifie si prix dans zone [0.500, 0.618]
6. Si confirmation Heiken Ashi → Signal Telegram

---

## 📈 Exemple de Signal

```
🚀 SIGNAL BULLISH - EUR/USD

Prix: 1.08500
Zone Fibonacci #1: 1.08410 - 1.09000
Fib #1: Creux 1.06500 → Sommet 1.11500

Bonus:
✅ Divergence RSI haussière
✅ Confluence Support/Résistance

Timeframe: H1
Heure: 2026-02-25 06:00 UTC
```

---

## 🛑 Arrêt du Bot

### Si lancé en avant-plan
```bash
Ctrl+C
```

### Si lancé en arrière-plan
```bash
pkill -f "python main.py"
```

### Si lancé avec screen
```bash
screen -S fibo_bot -X quit
```

---

## 🐛 Dépannage

### Erreur: "TELEGRAM_TOKEN_FIBOBOT n'est pas défini"
→ Vérifier que `.env` existe et contient le token

### Erreur: "TWELVEDATA_API_KEY_FIBOBOT n'est pas défini"
→ Vérifier que `.env` contient la clé API

### Erreur: "Pas de données pour EUR/USD"
→ L'API Twelve Data peut être temporairement indisponible
→ Le bot réessayera au prochain scan

### Crédits API faibles
→ Vous avez 800 crédits/jour
→ Chaque scan = ~14 crédits
→ ~50 scans possibles par jour

---

## 📞 Support

Pour les problèmes :

1. Vérifier les logs : `tail -f bot.log`
2. Lancer les tests : `python test_bot_complete.py`
3. Vérifier les secrets : `cat .env`

---

## 📝 Notes Importantes

- ✅ Le bot utilise **4 Fibonacci simultanément** (dernière correction)
- ✅ Les secrets sont **sécurisés** dans `.env`
- ✅ La base de données est **locale** (SQLite)
- ✅ Les logs sont **rotatifs** (max 10MB)
- ✅ Rate limiting : **8 requêtes/minute**

---

## 🎯 Prochaines Étapes

1. ✅ Démarrer le bot : `./start_bot.sh`
2. ✅ Vérifier les logs : `tail -f bot.log`
3. ✅ Tester les commandes Telegram
4. ✅ Attendre les premiers signaux

Le bot est **100% opérationnel** et prêt à trader ! 🚀
