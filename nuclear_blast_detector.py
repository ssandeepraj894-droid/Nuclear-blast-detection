"""
================================================================================
  NUCLEAR WEAPON BLAST DETECTION & EMERGENCY LIFE-SAVING ALERT SYSTEM
================================================================================
  Purpose: Detect nuclear blast signatures via multi-sensor fusion, calculate
           blast damage radii, and issue rapid emergency warnings to save lives.
================================================================================
"""

import time

def calculate_blast_impact(yield_kt, distance_km):
    """
    Calculates key blast radii based on weapon yield in kilotons (kT)
    using physics-based empirical scaling laws.
    """
    # Scaling factor relative to 1 KT standard yields
    scale = yield_kt ** (1 / 3)
    
    # Radii in kilometers
    fireball_radius = 0.07 * scale                 # Vaporization zone
    heavy_damage_radius = 0.35 * scale             # 20 PSI overpressure (total collapse)
    moderate_damage_radius = 0.85 * scale          # 5 PSI overpressure (residential collapse)
    thermal_burn_radius = 1.35 * scale             # 3rd-degree burns
    light_damage_radius = 2.20 * scale             # 1 PSI overpressure (shattered glass)
    
    # Speed of shockwave in air (~340 m/s = 0.34 km/s)
    shockwave_speed_kms = 0.34
    warning_time_sec = max(0, distance_km / shockwave_speed_kms)
    
    return {
        "fireball_km": round(fireball_radius, 2),
        "heavy_damage_km": round(heavy_damage_radius, 2),
        "moderate_damage_km": round(moderate_damage_radius, 2),
        "thermal_burn_km": round(thermal_burn_radius, 2),
        "light_damage_km": round(light_damage_radius, 2),
        "warning_time_sec": round(warning_time_sec, 1)
    }

def analyze_sensor_data(optical_lux, emp_kvm, seismic_magnitude, gamma_usv):
    """
    Multi-sensor fusion algorithm to detect nuclear detonation signatures.
    Returns detection status and threat confidence level.
    """
    score = 0
    reasons = []

    # 1. Optical Flash Detection (Double-pulse curve characteristic of nuclear detonation)
    if optical_lux > 100000:
        score += 30
        reasons.append("Extreme optical flash spike detected (Double-pulse signature)")

    # 2. Electromagnetic Pulse (EMP)
    if emp_kvm > 10:
        score += 25
        reasons.append("High-voltage Electromagnetic Pulse (EMP) burst detected")

    # 3. Radiation Spike (Gamma / Prompt Neutron Radiation)
    if gamma_usv > 50:
        score += 25
        reasons.append("Severe Gamma radiation ionization spike detected")

    # 4. Shallow Seismic Shockwave (Surface/Atmospheric detonation signature)
    if seismic_magnitude > 4.0:
        score += 20
        reasons.append("Shallow epicentral acoustic/seismic shockwave detected")

    if score >= 75:
        threat_level = "CRITICAL - DETONATION CONFIRMED"
    elif score >= 40:
        threat_level = "WARNING - SUSPICIOUS EVENT"
    else:
        threat_level = "NORMAL - NO NUCLEAR THREAT DETECTED"

    return {
        "confidence_percentage": score,
        "threat_level": threat_level,
        "detected_indicators": reasons
    }

def issue_life_saving_alert(location, distance_km, impact_data):
    """
    Generates actionable emergency life-saving directives based on warning time.
    """
    warning_sec = impact_data["warning_time_sec"]
    
    print("\n" + "="*70)
    print(" [ALERT] EMERGENCY BROADCAST SYSTEM: EARLY WARNING ACTIVATED")
    print("="*70)
    print(f" Target Area           : {location}")
    print(f" Distance to Epicenter : {distance_km} km")
    print(f" Estimated Shockwave Arrival Time: {warning_sec} seconds")
    print("-"*70)
    print(" DANGER ZONES & DAMAGE RADII:")
    print(f"  * Fireball / Vaporization Zone : 0.00 - {impact_data['fireball_km']} km")
    print(f"  * Heavy Damage Zone (20 PSI)   : {impact_data['fireball_km']} - {impact_data['heavy_damage_km']} km")
    print(f"  * Moderate Damage (5 PSI)      : {impact_data['heavy_damage_km']} - {impact_data['moderate_damage_km']} km")
    print(f"  * Thermal Radiation (3rd Burns): up to {impact_data['thermal_burn_km']} km")
    print(f"  * Light Damage (Glass Shatter) : up to {impact_data['light_damage_km']} km")
    print("-"*70)
    print(" LIFE-SAVING INSTRUCTIONS FOR CITIZENS:")
    
    if distance_km <= impact_data["heavy_damage_km"]:
        print("  1. DO NOT LOOK AT THE FLASH. Close eyes and cover face immediately.")
        print("  2. Lie flat on the ground facing AWAY from blast center.")
        print("  3. Take immediate shelter inside underground basements or reinforced structures.")
    elif distance_km <= impact_data["light_damage_km"]:
        print("  1. Move away from all windows immediately to avoid shattered glass.")
        print("  2. Take cover behind solid walls or heavy furniture.")
        print("  3. Stay indoors to prevent fallout radiation exposure.")
    else:
        print("  1. Remain indoors and seal doors/windows against fallout dust.")
        print("  2. Tune into emergency communication broadcasts.")

    print("="*70 + "\n")

def run_simulation():
    """
    Interactive program entry point for simulation.
    """
    print("\n==================================================================")
    print("   AI NUCLEAR BLAST DETECTION & LIFE SAVING ALERT SYSTEM (v1.0)   ")
    print("==================================================================")
    print(" Select Mode:")
    print("  1. Automated Sensor Telemetry Test (Simulation)")
    print("  2. Custom Weapon Yield & Blast Impact Calculator")
    print("  3. Exit")
    
    choice = input("\nEnter option (1-3): ").strip()
    
    if choice == "1":
        print("\n[+] Initializing Sensor Telemetry Feeds...")
        time.sleep(1)
        
        # Test Case: Simulated 100 KT Detonation Sensors
        optical = 150000   # lux
        emp = 25           # kV/m
        seismic = 5.2      # Richter
        gamma = 120        # uSv
        
        print("\n[SENSOR DATA RECEIVED]")
        print(f"  * Optical Sensor : {optical:,} lux")
        print(f"  * EMP Sensor     : {emp} kV/m")
        print(f"  * Seismic Sensor : {seismic} Richter scale")
        print(f"  * Gamma Detector : {gamma} uSv/hr")
        
        result = analyze_sensor_data(optical, emp, seismic, gamma)
        
        print(f"\nAnalysis Result: {result['threat_level']}")
        print(f"Threat Confidence: {result['confidence_percentage']}%")
        print("Indicators Found:")
        for ind in result["detected_indicators"]:
            print(f"  - {ind}")
            
        if result["confidence_percentage"] >= 75:
            # Calculate blast impact for 100 KT yield at 10 km away
            impact = calculate_blast_impact(yield_kt=100, distance_km=10)
            issue_life_saving_alert(location="City Center Sector 4", distance_km=10, impact_data=impact)
            
    elif choice == "2":
        try:
            yield_kt = float(input("Enter nuclear weapon yield in kilotons (e.g. 15 for Hiroshima, 100 for modern warhead): "))
            dist_km = float(input("Enter distance from blast center in kilometers: "))
            
            impact = calculate_blast_impact(yield_kt, dist_km)
            issue_life_saving_alert(location="Custom User Location", distance_km=dist_km, impact_data=impact)
        except ValueError:
            print("Invalid numeric input. Please enter valid numbers.")
    else:
        print("Exiting system. Stay safe!")

if __name__ == "__main__":
    run_simulation()
