"""
FastAPI Main Application Server for Nuclear Blast Detector System.
"""

import os
import json
from datetime import datetime, timedelta
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from .database import engine, Base, get_db
from .models import DetectionEvent
from .schemas import (
    TelemetryInput,
    BlastCalculationInput,
    BlastImpactResponse,
    DetectionAnalysisResponse,
    DetectionEventResponse,
    SystemStatsResponse,
)
from .physics import calculate_blast_impact, analyze_sensor_data, get_life_saving_directives

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Nuclear Blast Detection & Alert System API",
    description="Multi-sensor telemetry fusion engine & physics scaling REST backend",
    version="2.0.0"
)

# Enable CORS for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def seed_database_defaults(db: Session):
    """Seed initial sample detection events into SQLite if empty."""
    if db.query(DetectionEvent).count() > 0:
        return

    sample_events = [
        {
            "timestamp": datetime.utcnow() - timedelta(minutes=45),
            "location": "City Center Sector 4",
            "optical_lux": 150000.0,
            "emp_kvm": 25.0,
            "seismic_magnitude": 5.2,
            "gamma_usv": 120.0,
            "confidence_percentage": 100,
            "threat_level": "CRITICAL - DETONATION CONFIRMED",
            "indicators": json.dumps([
                "Extreme optical flash spike detected (Double-pulse signature)",
                "High-voltage Electromagnetic Pulse (EMP) burst detected",
                "Severe Gamma radiation ionization spike detected",
                "Shallow epicentral acoustic/seismic shockwave detected"
            ]),
            "yield_kt": 100.0,
            "distance_km": 10.0,
        },
        {
            "timestamp": datetime.utcnow() - timedelta(hours=3),
            "location": "Outpost Gamma North",
            "optical_lux": 120000.0,
            "emp_kvm": 12.5,
            "seismic_magnitude": 2.1,
            "gamma_usv": 1.2,
            "confidence_percentage": 55,
            "threat_level": "WARNING - SUSPICIOUS EVENT",
            "indicators": json.dumps([
                "Extreme optical flash spike detected (Double-pulse signature)",
                "High-voltage Electromagnetic Pulse (EMP) burst detected"
            ]),
            "yield_kt": 50.0,
            "distance_km": 15.0,
        },
        {
            "timestamp": datetime.utcnow() - timedelta(hours=12),
            "location": "Sector 1 Baseline Station",
            "optical_lux": 450.0,
            "emp_kvm": 0.2,
            "seismic_magnitude": 1.4,
            "gamma_usv": 0.15,
            "confidence_percentage": 0,
            "threat_level": "NORMAL - NO NUCLEAR THREAT DETECTED",
            "indicators": json.dumps([]),
            "yield_kt": 15.0,
            "distance_km": 25.0,
        }
    ]

    for data in sample_events:
        impact = calculate_blast_impact(data["yield_kt"], data["distance_km"])
        event = DetectionEvent(
            timestamp=data["timestamp"],
            location=data["location"],
            optical_lux=data["optical_lux"],
            emp_kvm=data["emp_kvm"],
            seismic_magnitude=data["seismic_magnitude"],
            gamma_usv=data["gamma_usv"],
            confidence_percentage=data["confidence_percentage"],
            threat_level=data["threat_level"],
            indicators=data["indicators"],
            yield_kt=data["yield_kt"],
            distance_km=data["distance_km"],
            fireball_km=impact.fireball_km,
            heavy_damage_km=impact.heavy_damage_km,
            moderate_damage_km=impact.moderate_damage_km,
            thermal_burn_km=impact.thermal_burn_km,
            light_damage_km=impact.light_damage_km,
            warning_time_sec=impact.warning_time_sec,
        )
        db.add(event)
    db.commit()


@app.on_event("startup")
def startup_event():
    """Ensure database has initial seed records on startup."""
    db = next(get_db())
    try:
        seed_database_defaults(db)
    finally:
        db.close()


# API REST Endpoints
@app.get("/api/health", summary="Check backend system health")
def health_check():
    return {
        "status": "online",
        "service": "Nuclear Blast Detection API",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/telemetry/analyze", response_model=DetectionAnalysisResponse, summary="Analyze telemetry & persist to DB")
def analyze_telemetry(payload: TelemetryInput, db: Session = Depends(get_db)):
    """
    Analyzes sensor telemetry, computes threat score, saves event to SQLite DB,
    and returns blast impact radii + life-saving directives.
    """
    result = analyze_sensor_data(payload)

    # Compute impact data
    impact = calculate_blast_impact(payload.yield_kt or 100.0, payload.distance_km or 10.0)
    directives = get_life_saving_directives(payload.distance_km or 10.0, impact)

    # Save to SQLite Database
    db_event = DetectionEvent(
        timestamp=datetime.utcnow(),
        location=payload.location or "Sector 4 Central",
        optical_lux=payload.optical_lux,
        emp_kvm=payload.emp_kvm,
        seismic_magnitude=payload.seismic_magnitude,
        gamma_usv=payload.gamma_usv,
        confidence_percentage=result.confidence_percentage,
        threat_level=result.threat_level,
        indicators=json.dumps(result.detected_indicators),
        yield_kt=payload.yield_kt or 100.0,
        distance_km=payload.distance_km or 10.0,
        fireball_km=impact.fireball_km,
        heavy_damage_km=impact.heavy_damage_km,
        moderate_damage_km=impact.moderate_damage_km,
        thermal_burn_km=impact.thermal_burn_km,
        light_damage_km=impact.light_damage_km,
        warning_time_sec=impact.warning_time_sec,
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return DetectionAnalysisResponse(
        confidence_percentage=result.confidence_percentage,
        threat_level=result.threat_level,
        detected_indicators=result.detected_indicators,
        impact=impact,
        event_id=db_event.id,
        timestamp=db_event.timestamp.isoformat(),
        directives=directives
    )


@app.post("/api/blast/calculate", response_model=BlastImpactResponse, summary="Calculate blast radii")
def calculate_blast(payload: BlastCalculationInput):
    """Calculates weapon blast radii based on yield in kilotons and distance."""
    try:
        return calculate_blast_impact(payload.yield_kt, payload.distance_km)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/api/events", response_model=List[DetectionEventResponse], summary="Retrieve historical events from DB")
def get_events(limit: int = 50, db: Session = Depends(get_db)):
    """Retrieves stored detection events from the SQLite database."""
    events = db.query(DetectionEvent).order_by(DetectionEvent.timestamp.desc()).limit(limit).all()
    formatted = []
    for ev in events:
        try:
            indicators_list = json.loads(ev.indicators) if ev.indicators else []
        except Exception:
            indicators_list = []

        formatted.append(DetectionEventResponse(
            id=ev.id,
            timestamp=ev.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC"),
            location=ev.location,
            optical_lux=ev.optical_lux,
            emp_kvm=ev.emp_kvm,
            seismic_magnitude=ev.seismic_magnitude,
            gamma_usv=ev.gamma_usv,
            confidence_percentage=ev.confidence_percentage,
            threat_level=ev.threat_level,
            indicators=indicators_list,
            yield_kt=ev.yield_kt or 100.0,
            distance_km=ev.distance_km or 10.0,
            fireball_km=ev.fireball_km or 0.0,
            heavy_damage_km=ev.heavy_damage_km or 0.0,
            moderate_damage_km=ev.moderate_damage_km or 0.0,
            thermal_burn_km=ev.thermal_burn_km or 0.0,
            light_damage_km=ev.light_damage_km or 0.0,
            warning_time_sec=ev.warning_time_sec or 0.0
        ))
    return formatted


@app.delete("/api/events", summary="Clear database event history")
def clear_events(db: Session = Depends(get_db)):
    """Clears all stored historical detection records from SQLite."""
    db.query(DetectionEvent).delete()
    db.commit()
    return {"message": "All detection event history cleared from database."}


@app.get("/api/stats", response_model=SystemStatsResponse, summary="Get summary dashboard metrics")
def get_stats(db: Session = Depends(get_db)):
    """Returns aggregated summary metrics for the dashboard."""
    events = db.query(DetectionEvent).all()
    total = len(events)
    critical = sum(1 for e in events if e.confidence_percentage >= 75)
    suspicious = sum(1 for e in events if 40 <= e.confidence_percentage < 75)
    normal = sum(1 for e in events if e.confidence_percentage < 40)
    avg_conf = round(sum(e.confidence_percentage for e in events) / total, 1) if total > 0 else 0.0

    return SystemStatsResponse(
        total_events=total,
        critical_threats=critical,
        suspicious_events=suspicious,
        normal_events=normal,
        average_confidence=avg_conf
    )


# Serve Static Frontend Files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/", include_in_schema=False)
    def read_root():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
