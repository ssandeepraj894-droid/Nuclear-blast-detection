"""
Physics engine scaling laws and multi-sensor fusion logic.
"""

from typing import Dict, Any, List
from .schemas import BlastImpactResponse, DetectionAnalysisResponse, TelemetryInput


def calculate_blast_impact(yield_kt: float, distance_km: float) -> BlastImpactResponse:
    """
    Calculates key blast damage radii based on weapon yield in kilotons (kT)
    using physics-based empirical scaling laws.
    """
    if yield_kt <= 0:
        raise ValueError(f"Weapon yield must be greater than zero. Provided: {yield_kt}")
    if distance_km < 0:
        raise ValueError(f"Distance to epicenter cannot be negative. Provided: {distance_km}")

    # Empirical yield scaling factor relative to 1 KT standard yield (Cube-root scaling law)
    scale = yield_kt ** (1 / 3)

    fireball_radius = round(0.07 * scale, 2)           # Vaporization zone
    heavy_damage_radius = round(0.35 * scale, 2)       # 20 PSI overpressure (total structural collapse)
    moderate_damage_radius = round(0.85 * scale, 2)    # 5 PSI overpressure (residential collapse)
    thermal_burn_radius = round(1.35 * scale, 2)       # 3rd-degree thermal burns
    light_damage_radius = round(2.20 * scale, 2)       # 1 PSI overpressure (glass shatter)

    # Atmospheric speed of shockwave (~340 m/s = 0.34 km/s)
    shockwave_speed_kms = 0.34
    warning_time_sec = round(max(0.0, distance_km / shockwave_speed_kms), 1)

    return BlastImpactResponse(
        yield_kt=float(yield_kt),
        distance_km=float(distance_km),
        fireball_km=fireball_radius,
        heavy_damage_km=heavy_damage_radius,
        moderate_damage_km=moderate_damage_radius,
        thermal_burn_km=thermal_burn_radius,
        light_damage_km=light_damage_radius,
        warning_time_sec=warning_time_sec
    )


def analyze_sensor_data(telemetry: TelemetryInput) -> DetectionAnalysisResponse:
    """
    Multi-sensor fusion algorithm evaluating optical, EMP, seismic, and gamma telemetry.
    """
    score = 0
    reasons = []

    # 1. Optical Flash Detection (Double-pulse curve characteristic)
    if telemetry.optical_lux > 100000:
        score += 30
        reasons.append("Extreme optical flash spike detected (Double-pulse signature)")

    # 2. Electromagnetic Pulse (EMP)
    if telemetry.emp_kvm > 10.0:
        score += 25
        reasons.append("High-voltage Electromagnetic Pulse (EMP) burst detected")

    # 3. Gamma Ionization Spike
    if telemetry.gamma_usv > 50.0:
        score += 25
        reasons.append("Severe Gamma radiation ionization spike detected")

    # 4. Shallow Seismic Shockwave
    if telemetry.seismic_magnitude > 4.0:
        score += 20
        reasons.append("Shallow epicentral acoustic/seismic shockwave detected")

    if score >= 75:
        threat_level = "CRITICAL - DETONATION CONFIRMED"
    elif score >= 40:
        threat_level = "WARNING - SUSPICIOUS EVENT"
    else:
        threat_level = "NORMAL - NO NUCLEAR THREAT DETECTED"

    impact = None
    directives = None
    if score >= 40 and telemetry.yield_kt and telemetry.distance_km:
        impact = calculate_blast_impact(telemetry.yield_kt, telemetry.distance_km)
        directives = get_life_saving_directives(telemetry.distance_km, impact)

    return DetectionAnalysisResponse(
        confidence_percentage=score,
        threat_level=threat_level,
        detected_indicators=reasons,
        impact=impact,
        directives=directives
    )


def get_life_saving_directives(distance_km: float, impact: BlastImpactResponse) -> List[str]:
    """Generates actionable citizen directives based on epicenter proximity."""
    if distance_km <= impact.fireball_km:
        return [
            "GROUND ZERO DETONATION ZONE - IMMEDIATE VAPORIZATION RISK.",
            "If sheltered underground, remain stationary and protect head/airway.",
            "Do NOT look at flash. Seal eyes and face immediately."
        ]
    elif distance_km <= impact.heavy_damage_km:
        return [
            "DO NOT LOOK AT THE FLASH. Close eyes and cover face immediately.",
            "Lie flat on the ground facing AWAY from blast center.",
            "Take immediate shelter inside underground basements or reinforced structures."
        ]
    elif distance_km <= impact.light_damage_km:
        return [
            "Move away from all windows immediately to avoid shattered glass.",
            "Take cover behind solid walls or heavy furniture.",
            "Stay indoors to prevent fallout radiation exposure."
        ]
    else:
        return [
            "Remain indoors and seal doors/windows against fallout dust.",
            "Tune into emergency communication broadcasts."
        ]
