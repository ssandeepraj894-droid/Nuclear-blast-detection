# 🛡️ Nuclear Blast Early Detection & Life-Saving System (AI Multi-Sensor Fusion)

[![Python 3.x](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![100 Codes Challenge](https://img.shields.io/badge/Project-100Codes-green.svg)](https://github.com/ssandeepraj894-droid/100codes)

> **Mission Statement:** A real-time early-warning simulation system designed to detect nuclear detonation signatures, calculate blast/thermal radii, and automatically broadcast immediate emergency survival directives to save millions of lives.

---

## 🌟 Key Features

1. **Multi-Sensor Data Fusion Algorithm:**
   - **Optical Flash Detection:** Identifies the unique double-pulse light curve characteristic of nuclear fireballs.
   - **Electromagnetic Pulse (EMP):** Detects high-voltage E1/E2 EMP bursts.
   - **Radiation Ionization:** Monitors prompt gamma radiation and neutron flux spikes.
   - **Acoustic & Seismic Waves:** Differentiates atmospheric shockwaves from subterranean tectonic earthquakes.

2. **Physics-Based Blast Damage Estimator:**
   - Computes empirical scaling laws ($R \propto Y^{1/3}$) for weapon yields ranging from tactical kilotons to strategic megatons.
   - Estimates Fireball Radius, Heavy Damage (20 PSI overpressure), Moderate Damage (5 PSI overpressure), Thermal Burn Radius (3rd degree burns), and Shattered Glass Zones (1 PSI).

3. **Automated Life-Saving Broadcast Directives:**
   - Computes shockwave arrival window (seconds to impact based on distance).
   - Generates actionable safety advice (e.g., immediate face-down posture, underground concrete sheltering, glass injury prevention).

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.x (No external dependencies required)

### Run the Interactive Simulation
Open your terminal/command prompt and run:
```bash
python nuclear_blast_detector.py
```

### Options:
- **Mode 1:** Run automated sensor telemetry test to simulate a live 100 KT detonation event.
- **Mode 2:** Custom weapon yield calculator (enter yield in KT and distance in KM to get exact safety radii & arrival warning time).

---

## 📂 Project Structure

```
100codes/
│
├── nuclear_blast_detector.py   # Core AI detection algorithm & alert engine
├── count_vowels.py             # Basic string processing exercise
└── README.md                   # Project documentation & GitHub showcase
```

---

## 🔗 GitHub & ChatGPT Codex Integration

To push this project to your GitHub repository and link it with ChatGPT Codex:

```bash
git add .
git commit -m "Add Nuclear Blast Detection & Life-Saving Alert System"
git push origin main
```

---

## 📜 License
This project is licensed under the MIT License - feel free to use, study, and expand it for disaster management research.
