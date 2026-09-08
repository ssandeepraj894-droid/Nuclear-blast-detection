"""
Pydantic data schemas for request parsing and API response serialization.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class TelemetryInput(BaseModel):
    """Input payload for multi-sensor telemetry analysis."""
    optical_lux: float = Field(..., ge=0.0, description="Optical illumination in lux")
    emp_kvm: float = Field(..., ge=0.0, description="EMP field strength in kV/m")
    seismic_magnitude: float = Field(..., description="Acoustic/seismic Richter magnitude")
    gamma_usv: float = Field(..., ge=0.0, description="Gamma radiation rate in uSv/hr")
    yield_kt: Optional[float] = Field(default=100.0, gt=0.0, description="Optional weapon yield in KT")
    distance_km: Optional[float] = Field(default=10.0, ge=0.0, description="Optional distance in km")
    location: Optional[str] = Field(default="Sector 4 Central", description="Location designation")


class BlastCalculationInput(BaseModel):
    """Input payload for calculating weapon blast damage radii."""
    yield_kt: float = Field(..., gt=0.0, description="Weapon yield in kilotons (e.g. 15 for Hiroshima, 100 for modern warhead)")
    distance_km: float = Field(..., ge=0.0, description="Distance from blast center in km")
    location: Optional[str] = Field(default="Target Sector", description="Target location name")


class BlastImpactResponse(BaseModel):
    """Blast damage radii and arrival time result."""
    yield_kt: float
    distance_km: float
    fireball_km: float
    heavy_damage_km: float
    moderate_damage_km: float
    thermal_burn_km: float
    light_damage_km: float
    warning_time_sec: float


class DetectionAnalysisResponse(BaseModel):
    """Result payload from multi-sensor fusion analysis."""
    confidence_percentage: int
    threat_level: str
    detected_indicators: List[str]
    impact: Optional[BlastImpactResponse] = None
    event_id: Optional[int] = None
    timestamp: Optional[str] = None
    directives: Optional[List[str]] = None


class DetectionEventResponse(BaseModel):
    """Response schema for historical SQLite database events."""
    id: int
    timestamp: str
    location: str
    optical_lux: float
    emp_kvm: float
    seismic_magnitude: float
    gamma_usv: float
    confidence_percentage: int
    threat_level: str
    indicators: List[str]
    yield_kt: float
    distance_km: float
    fireball_km: float
    heavy_damage_km: float
    moderate_damage_km: float
    thermal_burn_km: float
    light_damage_km: float
    warning_time_sec: float

    class Config:
        orm_mode = True


class SystemStatsResponse(BaseModel):
    """Summary dashboard statistics response."""
    total_events: int
    critical_threats: int
    suspicious_events: int
    normal_events: int
    average_confidence: float
