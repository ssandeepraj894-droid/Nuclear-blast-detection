"""
Command Line Interface (CLI) for Nuclear Blast Detection & Emergency Alert System.
"""

import sys
import time
import argparse
from typing import Optional

from .detector import (
    analyze_sensor_data,
    calculate_blast_impact,
    issue_life_saving_alert,
)


def run_interactive_simulation() -> None:
    """
    Interactive CLI entry point for nuclear blast detection simulation.
    """
    while True:
        print("\n==================================================================")
        print("   AI NUCLEAR BLAST DETECTION & LIFE SAVING ALERT SYSTEM (v1.1)   ")
        print("==================================================================")
        print(" Select Mode:")
        print("  1. Automated Sensor Telemetry Test (Simulation)")
        print("  2. Custom Weapon Yield & Blast Impact Calculator")
        print("  3. Exit")

        choice = input("\nEnter option (1-3): ").strip()

        if choice == "1":
            print("\n[+] Initializing Sensor Telemetry Feeds...")
            time.sleep(0.5)

            # Test Case: Simulated 100 KT Detonation Sensors
            optical = 150000.0   # lux
            emp = 25.0           # kV/m
            seismic = 5.2        # Richter
            gamma = 120.0        # uSv/hr

            print("\n[SENSOR DATA RECEIVED]")
            print(f"  * Optical Sensor : {optical:,.1f} lux")
            print(f"  * EMP Sensor     : {emp:.1f} kV/m")
            print(f"  * Seismic Sensor : {seismic:.1f} Richter scale")
            print(f"  * Gamma Detector : {gamma:.1f} uSv/hr")

            result = analyze_sensor_data(optical, emp, seismic, gamma)

            print(f"\nAnalysis Result   : {result.threat_level}")
            print(f"Threat Confidence : {result.confidence_percentage}%")
            print("Indicators Found:")
            for ind in result.detected_indicators:
                print(f"  - {ind}")

            if result.confidence_percentage >= 75:
                # Calculate blast impact for 100 KT yield at 10 km distance
                impact = calculate_blast_impact(yield_kt=100.0, distance_km=10.0)
                issue_life_saving_alert(location="City Center Sector 4", distance_km=10.0, impact=impact)

        elif choice == "2":
            try:
                yield_val = float(input("Enter nuclear weapon yield in kilotons (e.g. 15 for Hiroshima, 100 for modern warhead): "))
                dist_val = float(input("Enter distance from blast epicenter in kilometers: "))

                impact = calculate_blast_impact(yield_val, dist_val)
                issue_life_saving_alert(location="Custom User Location", distance_km=dist_val, impact=impact)
            except ValueError as e:
                print(f"\n[ERROR] Invalid input: {e}. Please enter positive numerical values.")

        elif choice == "3":
            print("\nExiting Nuclear Blast Detection System. Stay safe!")
            break
        else:
            print("\n[!] Invalid choice option. Please select option 1, 2, or 3.")


def cli_main(argv: Optional[list] = None) -> None:
    """
    Main entry point supporting both argument parsing and interactive fallback.
    """
    parser = argparse.ArgumentParser(
        description="Nuclear Weapon Blast Detection & Emergency Life-Saving Alert System"
    )
    parser.add_argument("--optical", type=float, help="Optical flash lux level")
    parser.add_argument("--emp", type=float, help="Electromagnetic pulse strength in kV/m")
    parser.add_argument("--seismic", type=float, help="Seismic shockwave Richter magnitude")
    parser.add_argument("--gamma", type=float, help="Gamma radiation rate in uSv/hr")
    parser.add_argument("--yield-kt", type=float, help="Weapon yield in kilotons for impact calculation")
    parser.add_argument("--distance-km", type=float, help="Distance to epicenter in km")
    parser.add_argument("--location", type=str, default="Target Area", help="Location name string")

    args = parser.parse_args(argv)

    # Check if telemetry arguments were passed directly
    if any(v is not None for v in (args.optical, args.emp, args.seismic, args.gamma)):
        optical = args.optical if args.optical is not None else 0.0
        emp = args.emp if args.emp is not None else 0.0
        seismic = args.seismic if args.seismic is not None else 0.0
        gamma = args.gamma if args.gamma is not None else 0.0

        try:
            result = analyze_sensor_data(optical, emp, seismic, gamma)
            print("\n[SENSOR ANALYSIS RESULT]")
            print(f"Threat Level      : {result.threat_level}")
            print(f"Confidence Score  : {result.confidence_percentage}%")
            for ind in result.detected_indicators:
                print(f"  - {ind}")

            if result.confidence_percentage >= 75 and args.yield_kt and args.distance_km:
                impact = calculate_blast_impact(args.yield_kt, args.distance_km)
                issue_life_saving_alert(args.location, args.distance_km, impact)
        except Exception as e:
            print(f"Error processing sensor telemetry: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.yield_kt is not None and args.distance_km is not None:
        try:
            impact = calculate_blast_impact(args.yield_kt, args.distance_km)
            issue_life_saving_alert(args.location, args.distance_km, impact)
        except Exception as e:
            print(f"Error calculating blast impact: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        run_interactive_simulation()
