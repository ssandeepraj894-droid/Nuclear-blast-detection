"""
================================================================================
  NUCLEAR WEAPON BLAST DETECTION & EMERGENCY LIFE-SAVING ALERT SYSTEM
================================================================================
  Purpose: Detect nuclear blast signatures via multi-sensor fusion, calculate
           blast damage radii, and issue rapid emergency warnings to save lives.
================================================================================
"""

import math
from dataclasses import dataclass, field
from typing import List, Dict, Any, Union


@dataclass(frozen=True)
class BlastImpact:
    """Represents calculated blast impact radii and arrival warning time."""
    yield_kt: float
    distance_km: float
    fireball_km: float
    heavy_damage_km: float
    moderate_damage_km: float
    thermal_burn_km: float
    light_damage_km: float
    warning_time_sec: float

    def to_dict(self) -> Dict[str, Union[float, int]]:
        """Converts impact data to a standard dictionary format."""
        return {
            "yield_kt": self.yield_kt,
            "distance_km": self.distance_km,
            "fireball_km": self.fireball_km,
            "heavy_damage_km": self.heavy_damage_km,
            "moderate_damage_km": self.moderate_damage_km,
            "thermal_burn_km": self.thermal_burn_km,
            "light_damage_km": self.light_damage_km,
            "warning_time_sec": self.warning_time_sec,
        }


@dataclass(frozen=True)
class SensorTelemetry:
    """Represents multi-sensor measurement inputs."""
    optical_lux: float
    emp_kvm: float
    seismic_magnitude: float
    gamma_usv: float

    def __post_init__(self):
        """Validate telemetry numerical boundaries."""
        if any(math.isnan(v) or math.isinf(v) for v in (self.optical_lux, self.emp_kvm, self.seismic_magnitude, self.gamma_usv)):
            raise ValueError("Sensor telemetry values must be finite numbers.")
        if self.optical_lux < 0 or self.emp_kvm < 0 or self.gamma_usv < 0:
            raise ValueError("Optical, EMP, and Gamma telemetry values cannot be negative.")


@dataclass(frozen=True)
class AnalysisResult:
    """Represents the output of the multi-sensor fusion algorithm."""
    confidence_percentage: int
    threat_level: str
    detected_indicators: List[str] = field(default_factory=list)


def calculate_blast_impact(yield_kt: float, distance_km: float) -> BlastImpact:
    """
    Calculates key blast radii based on weapon yield in kilotons (kT)
    using physics-based empirical scaling laws.

    Args:
        yield_kt: Weapon yield in kilotons (> 0).
        distance_km: Distance to detonation epicenter in kilometers (>= 0).

    Returns:
        BlastImpact dataclass instance.

    Raises:
        ValueError: If yield_kt <= 0 or distance_km < 0.
    """
    if yield_kt <= 0:
        raise ValueError(f"Weapon yield must be greater than zero. Provided: {yield_kt}")
    if distance_km < 0:
        raise ValueError(f"Distance to epicenter cannot be negative. Provided: {distance_km}")

    # Empirical yield scaling factor relative to 1 KT standard yield (Cube-root law)
    scale = yield_kt ** (1 / 3)

    # Radii in kilometers
    fireball_radius = round(0.07 * scale, 2)           # Vaporization zone
    heavy_damage_radius = round(0.35 * scale, 2)       # 20 PSI overpressure (total collapse)
    moderate_damage_radius = round(0.85 * scale, 2)    # 5 PSI overpressure (residential collapse)
    thermal_burn_radius = round(1.35 * scale, 2)       # 3rd-degree thermal burns
    light_damage_radius = round(2.20 * scale, 2)       # 1 PSI overpressure (glass shatter)

    # Shockwave propagation speed in standard atmosphere (~340 m/s = 0.34 km/s)
    shockwave_speed_kms = 0.34
    warning_time_sec = round(max(0.0, distance_km / shockwave_speed_kms), 1)

    return BlastImpact(
        yield_kt=float(yield_kt),
        distance_km=float(distance_km),
        fireball_km=fireball_radius,
        heavy_damage_km=heavy_damage_radius,
        moderate_damage_km=moderate_damage_radius,
        thermal_burn_km=thermal_burn_radius,
        light_damage_km=light_damage_radius,
        warning_time_sec=warning_time_sec
    )


def analyze_sensor_data(
    optical_lux: float,
    emp_kvm: float,
    seismic_magnitude: float,
    gamma_usv: float
) -> AnalysisResult:
    """
    Multi-sensor fusion algorithm to detect nuclear detonation signatures.

    Args:
        optical_lux: Optical sensor illumination in lux (> 0).
        emp_kvm: Electromagnetic field gradient in kV/m.
        seismic_magnitude: Epicentral acoustic/seismic Richter magnitude.
        gamma_usv: Gamma radiation rate in uSv/hr.

    Returns:
        AnalysisResult dataclass instance.
    """
    # Create validated Telemetry object
    telemetry = SensorTelemetry(
        optical_lux=float(optical_lux),
        emp_kvm=float(emp_kvm),
        seismic_magnitude=float(seismic_magnitude),
        gamma_usv=float(gamma_usv)
    )

    score = 0
    reasons = []

    # 1. Optical Flash Detection (Double-pulse characteristic)
    if telemetry.optical_lux > 100000:
        score += 30
        reasons.append("Extreme optical flash spike detected (Double-pulse signature)")

    # 2. Electromagnetic Pulse (EMP)
    if telemetry.emp_kvm > 10.0:
        score += 25
        reasons.append("High-voltage Electromagnetic Pulse (EMP) burst detected")

    # 3. Radiation Ionization Spike (Gamma / Prompt Neutron)
    if telemetry.gamma_usv > 50.0:
        score += 25
        reasons.append("Severe Gamma radiation ionization spike detected")

    # 4. Shallow Seismic Shockwave (Atmospheric/Surface signature)
    if telemetry.seismic_magnitude > 4.0:
        score += 20
        reasons.append("Shallow epicentral acoustic/seismic shockwave detected")

    if score >= 75:
        threat_level = "CRITICAL - DETONATION CONFIRMED"
    elif score >= 40:
        threat_level = "WARNING - SUSPICIOUS EVENT"
    else:
        threat_level = "NORMAL - NO NUCLEAR THREAT DETECTED"

    return AnalysisResult(
        confidence_percentage=score,
        threat_level=threat_level,
        detected_indicators=reasons
    )


def issue_life_saving_alert(location: str, distance_km: float, impact: Union[BlastImpact, Dict[str, Any]]) -> str:
    """
    Generates actionable emergency life-saving directives based on distance and warning time.

    Args:
        location: Name or designation of target location.
        distance_km: Distance to epicentre in kilometers.
        impact: BlastImpact instance or dictionary containing blast impact metrics.

    Returns:
        Formatted alert broadcast string.
    """
    if isinstance(impact, dict):
        fireball_km = impact["fireball_km"]
        heavy_damage_km = impact["heavy_damage_km"]
        moderate_damage_km = impact["moderate_damage_km"]
        thermal_burn_km = impact["thermal_burn_km"]
        light_damage_km = impact["light_damage_km"]
        warning_sec = impact["warning_time_sec"]
    else:
        fireball_km = impact.fireball_km
        heavy_damage_km = impact.heavy_damage_km
        moderate_damage_km = impact.moderate_damage_km
        thermal_burn_km = impact.thermal_burn_km
        light_damage_km = impact.light_damage_km
        warning_sec = impact.warning_time_sec

    lines = [
        "",
        "=" * 70,
        " [ALERT] EMERGENCY BROADCAST SYSTEM: EARLY WARNING ACTIVATED",
        "=" * 70,
        f" Target Area           : {location}",
        f" Distance to Epicenter : {distance_km:.2f} km",
        f" Estimated Shockwave Arrival Time: {warning_sec:.1f} seconds",
        "-" * 70,
        " DANGER ZONES & DAMAGE RADII:",
        f"  * Fireball / Vaporization Zone : 0.00 - {fireball_km:.2f} km",
        f"  * Heavy Damage Zone (20 PSI)   : {fireball_km:.2f} - {heavy_damage_km:.2f} km",
        f"  * Moderate Damage (5 PSI)      : {heavy_damage_km:.2f} - {moderate_damage_km:.2f} km",
        f"  * Thermal Radiation (3rd Burns): up to {thermal_burn_km:.2f} km",
        f"  * Light Damage (Glass Shatter) : up to {light_damage_km:.2f} km",
        "-" * 70,
        " LIFE-SAVING INSTRUCTIONS FOR CITIZENS:"
    ]

    if distance_km <= fireball_km:
        lines.extend([
            "  1. GROUND ZERO DETONATION ZONE - IMMEDIATE VAPORIZATION RISK.",
            "  2. If sheltered underground, remain stationary and protect head/airway.",
            "  3. Do NOT look at flash. Seal eyes and face immediately."
        ])
    elif distance_km <= heavy_damage_km:
        lines.extend([
            "  1. DO NOT LOOK AT THE FLASH. Close eyes and cover face immediately.",
            "  2. Lie flat on the ground facing AWAY from blast center.",
            "  3. Take immediate shelter inside underground basements or reinforced structures."
        ])
    elif distance_km <= light_damage_km:
        lines.extend([
            "  1. Move away from all windows immediately to avoid shattered glass.",
            "  2. Take cover behind solid walls or heavy furniture.",
            "  3. Stay indoors to prevent fallout radiation exposure."
        ])
    else:
        lines.extend([
            "  1. Remain indoors and seal doors/windows against fallout dust.",
            "  2. Tune into emergency communication broadcasts."
        ])

    lines.append("=" * 70 + "\n")
    alert_text = "\n".join(lines)
    print(alert_text)
    return alert_text
