# Nuclear Blast Detection & Emergency Life-Saving Alert System

A full-stack, real-world application featuring an **AI Multi-Sensor Fusion Engine**, **FastAPI REST Backend**, **SQLite Persistent Database**, **Interactive HTML5 Canvas Radar Visualizer**, and **Web Audio Emergency Siren Synthesizer**.

---

## 🌟 Full-Stack Features

- **Frontend (Web Dashboard)**:
  - Sleek dark-mode glassmorphism design system.
  - Interactive multi-sensor sliders (Optical Lux, EMP, Seismic Magnitude, Gamma Radiation).
  - Real-time auto-simulation mode generating live telemetry fluctuations.
  - Dynamic 2D HTML5 Canvas radar visualizer showing blast damage concentric circles (Fireball, Heavy 20 PSI, Moderate 5 PSI, Thermal Burn, Shatter 1 PSI) with animated shockwaves.
  - Web Audio API alarm siren synthesizer playing audio warnings on `CRITICAL` threat levels.
  - Actionable life-saving emergency citizen directives with countdown arrival timer.
  - Connected database table displaying logged events with CSV export, filter, and clear actions.

- **Backend (FastAPI REST Server)**:
  - Python FastAPI REST API endpoints (`/api/telemetry/analyze`, `/api/blast/calculate`, `/api/events`, `/api/stats`).
  - Automatic database schema initialization and initial seed records.
  - Multi-sensor fusion detection scoring engine ($0-100\%$).
  - Physics-based empirical scaling laws ($R = k \times Y^{1/3}$) for blast radii and acoustic shockwave arrival time ($\sim 340 \text{ m/s}$).

- **Database (SQLite Persistence)**:
  - Persistent SQLite storage (`nuclear_detector.db`) keeping historical sensor logs, detection events, and threat classifications.

---

## 📁 Repository Structure

```
nuclear_blast_detector/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI server, REST routes, CORS, & static mounting
│   │   ├── database.py      # SQLite connection & session management
│   │   ├── models.py        # SQLAlchemy ORM models (DetectionEvent)
│   │   ├── schemas.py       # Pydantic request/response schemas
│   │   └── physics.py       # Physics scaling & sensor fusion algorithms
│   └── requirements.txt     # Backend dependencies
├── frontend/
│   ├── index.html           # Dashboard HTML layout
│   ├── styles.css           # Glassmorphism dark UI stylesheet
│   └── app.js               # Frontend JS state manager, REST client, Canvas radar & Audio siren
├── tests/
│   ├── __init__.py
│   ├── test_detector.py     # Core physics unit tests
│   └── test_api.py          # FastAPI REST API & SQLite integration tests
├── main.py                  # CLI simulation script
├── run_server.py            # Easy full-stack launcher script
├── README.md                # Documentation
└── .gitignore               # Git ignore rules
```

---

## 🚀 Quick Start (Running Locally)

### 1. Launch Full-Stack Application Server
Run the single command below to automatically install missing dependencies, seed the SQLite database, and launch the FastAPI web server:

```bash
python run_server.py
```

Open your browser at:
- **Web Dashboard UI**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Interactive OpenAPI Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **API Health Check**: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

---

## 🧪 Running Unit & Integration Tests

Execute the complete test suite:

```bash
python -m unittest discover -s tests
```

---

## 🌐 REST API Specifications

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Backend status & health check |
| `POST` | `/api/telemetry/analyze` | Analyzes sensor telemetry, computes threat, saves to SQLite DB, returns alert |
| `POST` | `/api/blast/calculate` | Calculates damage radii for specified weapon yield & distance |
| `GET` | `/api/events` | Retrieves historical detection event logs from SQLite database |
| `DELETE` | `/api/events` | Clears all stored database detection records |
| `GET` | `/api/stats` | Aggregated dashboard summary statistics |

---

## 📜 License

MIT License. Educational, safety simulation, and defense research application.
