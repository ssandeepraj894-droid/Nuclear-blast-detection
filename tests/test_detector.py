"""
Unit Test Suite for Nuclear Blast Detector Physics Engine & Sensor Fusion.
"""

import math
import unittest
from nuclear_blast_detector.detector import (
    BlastImpact,
    SensorTelemetry,
    AnalysisResult,
    calculate_blast_impact,
    analyze_sensor_data,
    issue_life_saving_alert,
)


class TestBlastImpactCalculator(unittest.TestCase):
    """Test scaling laws and blast impact radius calculations."""

    def test_standard_1kt_yield(self):
        impact = calculate_blast_impact(yield_kt=1.0, distance_km=1.0)
        self.assertIsInstance(impact, BlastImpact)
        self.assertEqual(impact.fireball_km, 0.07)
        self.assertEqual(impact.heavy_damage_km, 0.35)
        self.assertEqual(impact.moderate_damage_km, 0.85)
        self.assertEqual(impact.thermal_burn_km, 1.35)
        self.assertEqual(impact.light_damage_km, 2.20)
        self.assertAlmostEqual(impact.warning_time_sec, 2.9, places=1)

    def test_hiroshima_15kt_yield(self):
        impact = calculate_blast_impact(yield_kt=15.0, distance_km=5.0)
        scale = 15.0 ** (1 / 3)
        self.assertEqual(impact.fireball_km, round(0.07 * scale, 2))
        self.assertEqual(impact.heavy_damage_km, round(0.35 * scale, 2))

    def test_invalid_yield_raises_value_error(self):
        with self.assertRaises(ValueError):
            calculate_blast_impact(yield_kt=0.0, distance_km=10.0)

        with self.assertRaises(ValueError):
            calculate_blast_impact(yield_kt=-15.0, distance_km=10.0)

    def test_invalid_distance_raises_value_error(self):
        with self.assertRaises(ValueError):
            calculate_blast_impact(yield_kt=100.0, distance_km=-5.0)


class TestSensorFusionEngine(unittest.TestCase):
    """Test sensor fusion detection scoring and telemetry validation."""

    def test_normal_telemetry(self):
        result = analyze_sensor_data(
            optical_lux=500.0,
            emp_kvm=0.1,
            seismic_magnitude=1.5,
            gamma_usv=0.15
        )
        self.assertIsInstance(result, AnalysisResult)
        self.assertEqual(result.confidence_percentage, 0)
        self.assertIn("NORMAL", result.threat_level)
        self.assertEqual(len(result.detected_indicators), 0)

    def test_critical_detonation_telemetry(self):
        result = analyze_sensor_data(
            optical_lux=150000.0,
            emp_kvm=25.0,
            seismic_magnitude=5.5,
            gamma_usv=100.0
        )
        self.assertEqual(result.confidence_percentage, 100)
        self.assertIn("CRITICAL", result.threat_level)
        self.assertEqual(len(result.detected_indicators), 4)

    def test_warning_suspicious_event(self):
        # Optical + EMP only = 30 + 25 = 55%
        result = analyze_sensor_data(
            optical_lux=120000.0,
            emp_kvm=15.0,
            seismic_magnitude=2.0,
            gamma_usv=1.0
        )
        self.assertEqual(result.confidence_percentage, 55)
        self.assertIn("WARNING", result.threat_level)

    def test_invalid_sensor_telemetry_raises_error(self):
        with self.assertRaises(ValueError):
            SensorTelemetry(
                optical_lux=-10.0,
                emp_kvm=0.0,
                seismic_magnitude=0.0,
                gamma_usv=0.0
            )

        with self.assertRaises(ValueError):
            SensorTelemetry(
                optical_lux=float("nan"),
                emp_kvm=0.0,
                seismic_magnitude=0.0,
                gamma_usv=0.0
            )


class TestEmergencyAlertSystem(unittest.TestCase):
    """Test emergency alert text generation."""

    def test_issue_life_saving_alert_formatting(self):
        impact = calculate_blast_impact(yield_kt=100.0, distance_km=10.0)
        alert_str = issue_life_saving_alert("Sector 7", 10.0, impact)
        self.assertIn("Sector 7", alert_str)
        self.assertIn("DANGER ZONES & DAMAGE RADII", alert_str)
        self.assertIn("LIFE-SAVING INSTRUCTIONS FOR CITIZENS", alert_str)

    def test_ground_zero_alert_directive(self):
        impact = calculate_blast_impact(yield_kt=100.0, distance_km=0.1)
        alert_str = issue_life_saving_alert("Epicenter Zone", 0.1, impact)
        self.assertIn("GROUND ZERO DETONATION ZONE", alert_str)


if __name__ == "__main__":
    unittest.main()
