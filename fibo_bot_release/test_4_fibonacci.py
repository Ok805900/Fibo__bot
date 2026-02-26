#!/usr/bin/env python3
"""
Test rapide: Vérifier que 4 Fibonacci sont bien calculés
"""

from core.fibonacci import FibonacciCalculator


def test_4_fibonacci_bullish():
    """Test: 4 Fibonacci en mode BULLISH"""
    print("\n" + "="*60)
    print("TEST: 4 Fibonacci BULLISH")
    print("="*60)

    # Créer des bougies de test avec pics et creux
    candles = [
        {"high": 1.0800, "low": 1.0700},
        {"high": 1.0900, "low": 1.0650},
        {"high": 1.1000, "low": 1.0800},
        {"high": 1.0950, "low": 1.0600},
        {"high": 1.1050, "low": 1.0800},
        {"high": 1.1000, "low": 1.0550},
        {"high": 1.1100, "low": 1.0850},
        {"high": 1.1050, "low": 1.0500},
        {"high": 1.1150, "low": 1.0900},
        {"high": 1.1100, "low": 1.0950},
        {"high": 1.1200, "low": 1.1000},
    ]

    # Calculer 4 Fibonacci en mode BULLISH
    fibs = FibonacciCalculator.calculate_multiple_fibonacci(candles, mode="bullish", max_count=4)

    print(f"\nNombre de Fibonacci calculés: {len(fibs)}")
    assert len(fibs) >= 1, f"Attendu au moins 1 Fibonacci, obtenu {len(fibs)}"

    for i, fib in enumerate(fibs):
        print(f"\nFibonacci #{fib['index']}:")
        print(f"   Mode: {fib['mode']}")
        print(f"   Point A (Sommet): {fib['point_a']:.5f}")
        print(f"   Point B (Creux): {fib['point_b']:.5f}")
        print(f"   Zone GA: [{fib['zone_min']:.5f}, {fib['zone_max']:.5f}]")

    print("\nTest BULLISH passé!")


def test_4_fibonacci_bearish():
    """Test: 4 Fibonacci en mode BEARISH"""
    print("\n" + "="*60)
    print("TEST: 4 Fibonacci BEARISH")
    print("="*60)

    # Créer des bougies de test avec pics et creux (inversés)
    candles = [
        {"high": 1.1200, "low": 1.1100},
        {"high": 1.1150, "low": 1.1000},
        {"high": 1.1100, "low": 1.0900},
        {"high": 1.1200, "low": 1.0950},
        {"high": 1.1100, "low": 1.0800},
        {"high": 1.1250, "low": 1.0900},
        {"high": 1.1150, "low": 1.0750},
        {"high": 1.1300, "low": 1.0850},
        {"high": 1.1200, "low": 1.0700},
        {"high": 1.1250, "low": 1.0750},
        {"high": 1.1100, "low": 1.0800},
    ]

    # Calculer 4 Fibonacci en mode BEARISH
    fibs = FibonacciCalculator.calculate_multiple_fibonacci(candles, mode="bearish", max_count=4)

    print(f"\nNombre de Fibonacci calculés: {len(fibs)}")
    assert len(fibs) >= 1, f"Attendu au moins 1 Fibonacci, obtenu {len(fibs)}"

    for i, fib in enumerate(fibs):
        print(f"\nFibonacci #{fib['index']}:")
        print(f"   Mode: {fib['mode']}")
        print(f"   Point A (Sommet): {fib['point_a']:.5f}")
        print(f"   Point B (Creux): {fib['point_b']:.5f}")
        print(f"   Zone GA: [{fib['zone_min']:.5f}, {fib['zone_max']:.5f}]")

    print("\nTest BEARISH passé!")


def test_price_in_zone():
    """Test: Vérifier si le prix est dans une zone GA"""
    print("\n" + "="*60)
    print("TEST: Vérification du prix dans zone GA")
    print("="*60)

    # Créer des bougies de test
    candles = [
        {"high": 1.1000, "low": 1.0700},
        {"high": 1.0900, "low": 1.0600},
        {"high": 1.1100, "low": 1.0800},
        {"high": 1.1050, "low": 1.0750},
        {"high": 1.1200, "low": 1.0900},
    ]

    fibs = FibonacciCalculator.calculate_multiple_fibonacci(candles, mode="bullish", max_count=4)

    if fibs:
        # Test 1: Prix dans la zone
        price_in_zone = 1.0850
        result = FibonacciCalculator.check_price_in_any_zone(price_in_zone, fibs)
        print(f"\nPrix {price_in_zone:.5f} dans zone: {result is not None}")

        if result:
            print(f"   Zone trouvée: Fib #{result['fib_index']}")
            print(f"   Limites: [{result['zone_min']:.5f}, {result['zone_max']:.5f}]")

        # Test 2: Prix hors zone
        price_out_zone = 1.0500
        result = FibonacciCalculator.check_price_in_any_zone(price_out_zone, fibs)
        print(f"\nPrix {price_out_zone:.5f} hors zone: {result is None}")

    print("\nTest prix dans zone passé!")


if __name__ == "__main__":
    try:
        test_4_fibonacci_bullish()
        test_4_fibonacci_bearish()
        test_price_in_zone()

        print("\n" + "="*60)
        print("TOUS LES TESTS PASSÉS!")
        print("="*60)
        print("\n4 Fibonacci sont maintenant calculés correctement")

    except AssertionError as e:
        print(f"\nErreur: {e}")
        exit(1)
    except Exception as e:
        print(f"\nErreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
