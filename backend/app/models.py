"""
SQLAlchemy database ORM models for Nuclear Blast Detection Events.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, Text
from .database import Base


class DetectionEvent(Base):
    """Represents a logged nuclear blast telemetry detection event."""
    __tablename__ = "detection_events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    location = Column(String(100), default="Sector 4 Central")

    # Sensor Input Telemetry
    optical_lux = Column(Float, nullable=False)
    emp_kvm = Column(Float, nullable=False)
    seismic_magnitude = Column(Float, nullable=False)
    gamma_usv = Column(Float, nullable=False)

    # Fusion Results
    confidence_percentage = Column(Integer, nullable=False)
    threat_level = Column(String(50), nullable=False)
    indicators = Column(Text, nullable=True)  # JSON-encoded string of list of reasons

    # Calculated Blast Impact Metrics
    yield_kt = Column(Float, default=100.0)
    distance_km = Column(Float, default=10.0)
    fireball_km = Column(Float, nullable=True)
    heavy_damage_km = Column(Float, nullable=True)
    moderate_damage_km = Column(Float, nullable=True)
    thermal_burn_km = Column(Float, nullable=True)
    light_damage_km = Column(Float, nullable=True)
    warning_time_sec = Column(Float, nullable=True)
