#!/usr/bin/env python3
"""
Tests unitaires du bot Fibonacci
"""

import unittest
from core.fibonacci import FibonacciCalculator
from core.heiken_ashi import HeikenAshiAnalyzer
from core.technical import TechnicalAnalyzer


class TestFibonacciCalculator(unittest.TestCase):
    """Tests du calculateur Fibonacci"""

    def test_calculate_levels(self):
        """Tester le calcul des niveaux Fibonacci"""
        high = 1.10000
        low = 1.08000

        levels = FibonacciCalculator.calculate_levels(high, low)

        self.assertAlmostEqual(levels["level_0"], 1.10000, places=5)
        self.assertAlmostEqual(levels["level_500"], 1.09000, places=5)
        self.assertAlmostEqual(levels["level_618"], 1.08764, places=5)
        self.assertAlmostEqual(levels["level_100"], 1.08000, places=5)

    def test_is_price_in_zone(self):
        """Tester si le prix est dans la zone GA"""
        high = 1.10000
        low = 1.08000
        levels = FibonacciCalculator.calculate_levels(high, low)

        # Prix dans la zone
        self.assertTrue(FibonacciCalculator.is_price_in_zone(1.08900, levels))

        # Prix hors zone
        self.assertFalse(FibonacciCalculator.is_price_in_zone(1.07000, levels))

    def test_find_peaks_and_troughs(self):
        """Tester la détection de pics et creux"""
        candles = [
            {"high": 1.10, "low": 1.08},
            {"high": 1.11, "low": 1.09},
            {"high": 1.09, "low": 1.07},  # Creux
            {"high": 1.12, "low": 1.08},  # Sommet
            {"high": 1.10, "low": 1.06},
        ]

        peaks, troughs = FibonacciCalculator.find_peaks_and_troughs(candles)

        self.assertGreater(len(peaks), 0)
        self.assertGreater(len(troughs), 0)


class TestHeikenAshiAnalyzer(unittest.TestCase):
    """Tests de l'analyseur Heiken Ashi"""

    def test_convert_to_heiken_ashi(self):
        """Tester la conversion en Heiken Ashi"""
        candles = [
            {"open": 1.10, "high": 1.11, "low": 1.09, "close": 1.105},
            {"open": 1.105, "high": 1.12, "low": 1.10, "close": 1.115},
        ]

        ha_candles = HeikenAshiAnalyzer.convert_to_heiken_ashi(candles)

        self.assertEqual(len(ha_candles), 2)
        self.assertIn("ha_open", ha_candles[0])
        self.assertIn("ha_close", ha_candles[0])
        self.assertIn("ha_high", ha_candles[0])
        self.assertIn("ha_low", ha_candles[0])

    def test_is_bullish(self):
        """Tester la détection de bougie haussière"""
        ha_candle = {
            "ha_open": 1.10,
            "ha_close": 1.11,
        }

        self.assertTrue(HeikenAshiAnalyzer.is_bullish(ha_candle))

    def test_is_bearish(self):
        """Tester la détection de bougie baissière"""
        ha_candle = {
            "ha_open": 1.11,
            "ha_close": 1.10,
        }

        self.assertTrue(HeikenAshiAnalyzer.is_bearish(ha_candle))

    def test_detect_color_change(self):
        """Tester la détection de changement de couleur"""
        prev_candle = {"ha_open": 1.10, "ha_close": 1.09}  # Baissier
        curr_candle = {"ha_open": 1.09, "ha_close": 1.10}  # Haussier

        change = HeikenAshiAnalyzer.detect_color_change(prev_candle, curr_candle)

        self.assertEqual(change, "red_to_green")


class TestTechnicalAnalyzer(unittest.TestCase):
    """Tests de l'analyseur technique"""

    def test_calculate_sma(self):
        """Tester le calcul de la SMA"""
        candles = [
            {"close": 1.10},
            {"close": 1.11},
            {"close": 1.12},
            {"close": 1.11},
            {"close": 1.10},
        ]

        sma = TechnicalAnalyzer.calculate_sma(candles, 5)

        expected = (1.10 + 1.11 + 1.12 + 1.11 + 1.10) / 5
        self.assertAlmostEqual(sma, expected, places=5)

    def test_determine_trend(self):
        """Tester la détermination de la tendance"""
        # Haussier
        trend = TechnicalAnalyzer.determine_trend(1.11, 1.10)
        self.assertEqual(trend, "BULLISH")

        # Baissier
        trend = TechnicalAnalyzer.determine_trend(1.09, 1.10)
        self.assertEqual(trend, "BEARISH")

        # Neutre
        trend = TechnicalAnalyzer.determine_trend(1.10, 1.10)
        self.assertEqual(trend, "NEUTRAL")

    def test_find_support_resistance(self):
        """Tester la détection de support/résistance"""
        candles = [
            {"high": 1.10, "low": 1.08},
            {"high": 1.11, "low": 1.09},
            {"high": 1.09, "low": 1.07},
            {"high": 1.12, "low": 1.08},
            {"high": 1.10, "low": 1.06},
        ]

        supports, resistances = TechnicalAnalyzer.find_support_resistance(candles)

        self.assertIsInstance(supports, list)
        self.assertIsInstance(resistances, list)


if __name__ == "__main__":
    unittest.main()
