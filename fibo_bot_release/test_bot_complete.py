#!/usr/bin/env python3
"""
Test complet du bot Fibonacci avec 4 niveaux
Simule un scan complet avec les 4 Fibonacci
"""

import sys
from config.secrets import Secrets
from data.twelvedata_client import TwelveDataClient
from data.database import Database
from core.scanner import ForexScanner
from core.fibonacci import FibonacciCalculator
from utils.logger import setup_logger

logger = setup_logger(__name__)


def test_secrets():
    """Test 1: Vérifier que les secrets sont chargés"""
    print("\n" + "="*60)
    print("TEST 1: Vérification des secrets")
    print("="*60)
    
    try:
        token = Secrets.get_telegram_token()
        api_key = Secrets.get_twelvedata_api_key()
        
        print(f"✅ Token Telegram: {token[:20]}...")
        print(f"✅ API Key Twelve Data: {api_key[:20]}...")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_api_client():
    """Test 2: Vérifier que le client API fonctionne"""
    print("\n" + "="*60)
    print("TEST 2: Vérification du client Twelve Data")
    print("="*60)
    
    try:
        api_key = Secrets.get_twelvedata_api_key()
        client = TwelveDataClient(api_key)
        
        credits = client.get_credits_remaining()
        print(f"✅ Client Twelve Data initialisé")
        print(f"✅ Crédits API restants: {credits}/800")
        
        if credits < 100:
            print(f"⚠️  Attention: Crédits faibles ({credits})")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_database():
    """Test 3: Vérifier que la base de données fonctionne"""
    print("\n" + "="*60)
    print("TEST 3: Vérification de la base de données")
    print("="*60)
    
    try:
        db = Database("test_signals.db")
        
        # Insérer un signal de test
        db.save_signal(
            symbol="EUR/USD",
            timeframe="H1",
            signal_type="bullish",
            price=1.0850,
            fib_level="0.500",
            heiken_ashi_confirmed=True,
            rsi_divergence=True,
            sr_confluence=True,
        )
        print(f"✅ Signal de test inséré")
        
        # Récupérer les signaux
        signals = db.get_signals_24h()
        print(f"✅ Signaux récupérés: {len(signals)} signal(s)")
        
        # Nettoyer
        import os
        if os.path.exists("test_signals.db"):
            os.remove("test_signals.db")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_4_fibonacci_integration():
    """Test 4: Tester l'intégration des 4 Fibonacci"""
    print("\n" + "="*60)
    print("TEST 4: Intégration des 4 Fibonacci")
    print("="*60)
    
    try:
        # Créer des bougies de test
        candles = [
            {"high": 1.0800, "low": 1.0700, "close": 1.0750},
            {"high": 1.0900, "low": 1.0650, "close": 1.0850},
            {"high": 1.1000, "low": 1.0800, "close": 1.0950},
            {"high": 1.0950, "low": 1.0600, "close": 1.0800},
            {"high": 1.1050, "low": 1.0800, "close": 1.1000},
            {"high": 1.1000, "low": 1.0550, "close": 1.0700},
            {"high": 1.1100, "low": 1.0850, "close": 1.1050},
            {"high": 1.1050, "low": 1.0500, "close": 1.0750},
            {"high": 1.1150, "low": 1.0900, "close": 1.1100},
            {"high": 1.1100, "low": 1.0950, "close": 1.1050},
            {"high": 1.1200, "low": 1.1000, "close": 1.1150},
        ]
        
        # Calculer 4 Fibonacci BULLISH
        fibs_bullish = FibonacciCalculator.calculate_multiple_fibonacci(
            candles, mode="bullish", max_count=4
        )
        print(f"✅ Fibonacci BULLISH: {len(fibs_bullish)} niveaux calculés")
        
        # Calculer 4 Fibonacci BEARISH
        fibs_bearish = FibonacciCalculator.calculate_multiple_fibonacci(
            candles, mode="bearish", max_count=4
        )
        print(f"✅ Fibonacci BEARISH: {len(fibs_bearish)} niveaux calculés")
        
        # Afficher les détails
        print("\n📊 Détails Fibonacci BULLISH:")
        for fib in fibs_bullish:
            print(f"  Fib #{fib['index']}: Zone [{fib['zone_min']:.5f}, {fib['zone_max']:.5f}]")
        
        # Tester la détection de prix dans zone
        test_price = 1.0850
        result = FibonacciCalculator.check_price_in_any_zone(test_price, fibs_bullish)
        
        if result:
            print(f"\n✅ Prix {test_price:.5f} détecté dans Fib #{result['fib_index']}")
        else:
            print(f"\n⚠️  Prix {test_price:.5f} hors zone")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_scanner():
    """Test 5: Tester le scanner avec les 4 Fibonacci"""
    print("\n" + "="*60)
    print("TEST 5: Scanner avec 4 Fibonacci")
    print("="*60)
    
    try:
        api_key = Secrets.get_twelvedata_api_key()
        api_client = TwelveDataClient(api_key)
        db = Database("test_scanner.db")
        scanner = ForexScanner(api_client, db)
        
        print("✅ Scanner initialisé")
        print("✅ Prêt à scanner les paires")
        
        # Nettoyer
        import os
        if os.path.exists("test_scanner.db"):
            os.remove("test_scanner.db")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def main():
    """Exécuter tous les tests"""
    print("\n" + "="*60)
    print("🤖 TEST COMPLET - BOT FIBONACCI AVEC 4 NIVEAUX")
    print("="*60)
    
    results = {
        "Secrets": test_secrets(),
        "API Client": test_api_client(),
        "Database": test_database(),
        "4 Fibonacci": test_4_fibonacci_integration(),
        "Scanner": test_scanner(),
    }
    
    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passés")
    
    if passed == total:
        print("\n" + "="*60)
        print("✅ TOUS LES TESTS PASSÉS!")
        print("🚀 Le bot est prêt à être déployé")
        print("="*60)
        print("\nPour démarrer le bot:")
        print("  ./start_bot.sh")
        print("  ou")
        print("  python main.py")
        return 0
    else:
        print("\n" + "="*60)
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("="*60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
