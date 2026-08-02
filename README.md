# Nuclear Blast Detection & Emergency Life-Saving Alert System

An AI-powered multi-sensor fusion engine and physics-based blast impact calculator designed to detect nuclear detonation signatures, compute physical damage radii, and issue automated life-saving emergency warnings.

---

## 🌟 Key Features

- **Multi-Sensor Fusion Algorithm**: Evaluates telemetry from optical sensors, EMP sensors, gamma-ray ionizers, and seismic shockwave detectors to compute threat confidence scores.
- **Empirical Scaling Physics Engine**: Uses cube-root scaling laws ($R = k \times Y^{1/3}$) to calculate fireball, heavy damage (20 PSI), moderate damage (5 PSI), thermal radiation, and glass-shatter radii based on weapon yield in kilotons.
- **Dynamic Warning Arrival Calculation**: Computes acoustic shockwave propagation time based on atmospheric speed of sound ($\sim 340 \text{ m/s}$).
- **Actionable Survival Directives**: Generates location-specific early warnings with immediate life-saving instructions for citizens based on proximity.
- **Interactive & CLI Interface**: Includes both an interactive terminal interface and flag-based non-interactive automation.
- **Comprehensive Unit Testing**: Includes unit test coverage for validation, scaling calculations, sensor fusion logic, and boundary conditions.

---

## 📁 Repository Structure

```
nuclear_blast_detector/
├── nuclear_blast_detector/
│   ├── __init__.py          # Package exports
│   ├── detector.py          # Core dataclasses, physics calculations, & sensor fusion
│   └── cli.py               # Interactive simulation loop & CLI argument parser
├── tests/
│   ├── __init__.py
│   └── test_detector.py     # Unittest test suite
├── main.py                  # Root execution script
├── README.md                # Documentation
└── .gitignore               # Python gitignore configuration
```

---

## 🚀 Quick Start

### 1. Interactive Simulation
Run the main script to launch the interactive simulation menu:

```bash
python main.py
```

### 2. Automated Telemetry Analysis via CLI Flags
Run non-interactive sensor analysis by passing sensor readings:

```bash
python main.py --optical 150000 --emp 25 --seismic 5.2 --gamma 120 --yield-kt 100 --distance-km 10 --location "Metropolitan Area"
```

### 3. Quick Blast Radius Calculation
Calculate blast radii directly from command line:

```bash
python main.py --yield-kt 15 --distance-km 3.5 --location "Hiroshima-Scale Test"
```

---

## 🧪 Running Unit Tests

Execute the built-in test suite to verify code correctness and boundary handling:

```bash
python -m unittest discover -s tests
```

---

## 📐 Physics Formulas & Thresholds

### Sensor Fusion Scoring Matrix
| Sensor Metric | Threshold | Score Contribution | Indicator Signature |
| :--- | :--- | :--- | :--- |
| **Optical Flash** | $> 100,000\text{ lux}$ | $+30\%$ | Double-pulse optical curve |
| **EMP** | $> 10.0\text{ kV/m}$ | $+25\%$ | Prompt high-voltage burst |
| **Gamma Radiation** | $> 50.0\ \mu\text{Sv/hr}$ | $+25\%$ | Severe ionization spike |
| **Seismic Shock** | $> 4.0\text{ Richter}$ | $+20\%$ | Shallow surface acoustic shockwave |

- **Detonation Confirmed**: Total Confidence $\ge 75\%$
- **Suspicious Warning**: Total Confidence $\ge 40\%$
- **Normal Baseline**: Total Confidence $< 40\%$

---

## 📜 License

MIT License. Designed for safety, educational, and defense simulation applications.
