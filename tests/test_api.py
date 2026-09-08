"""
Integration and API Test Suite for FastAPI Backend & SQLite DB.
"""

import unittest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


class TestFastAPIEndpoints(unittest.TestCase):
    """Test REST API endpoints and SQLite database operations."""

    def test_health_check_endpoint(self):
        response = client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "online")

    def test_analyze_telemetry_endpoint(self):
        payload = {
            "optical_lux": 150000.0,
            "emp_kvm": 25.0,
            "seismic_magnitude": 5.2,
            "gamma_usv": 120.0,
            "yield_kt": 100.0,
            "distance_km": 10.0,
            "location": "Test Area API"
        }
        response = client.post("/api/telemetry/analyze", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["confidence_percentage"], 100)
        self.assertIn("CRITICAL", data["threat_level"])
        self.assertIsNotNone(data["event_id"])
        self.assertIsNotNone(data["impact"])

    def test_calculate_blast_endpoint(self):
        payload = {
            "yield_kt": 15.0,
            "distance_km": 3.0,
            "location": "Hiroshima Test"
        }
        response = client.post("/api/blast/calculate", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["yield_kt"], 15.0)
        self.assertGreater(data["fireball_km"], 0)

    def test_get_events_endpoint(self):
        response = client.get("/api/events")
        self.assertEqual(response.status_code, 200)
        events = response.json()
        self.assertIsInstance(events, list)
        self.assertGreater(len(events), 0)

    def test_get_stats_endpoint(self):
        response = client.get("/api/stats")
        self.assertEqual(response.status_code, 200)
        stats = response.json()
        self.assertIn("total_events", stats)
        self.assertIn("critical_threats", stats)


if __name__ == "__main__":
    unittest.main()
