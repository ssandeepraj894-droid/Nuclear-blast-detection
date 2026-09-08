#!/usr/bin/env python3
"""
Full-Stack Application Launcher Script for Nuclear Blast Detection System.
Launches FastAPI backend server on http://127.0.0.1:8000
"""

import sys
import subprocess
import os

def ensure_dependencies():
    """Ensure required packages are installed."""
    required = ["fastapi", "uvicorn", "sqlalchemy", "pydantic"]
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)

    if missing:
        print(f"[+] Installing missing backend dependencies: {missing}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)

def main():
    ensure_dependencies()
    
    import uvicorn
    print("\n==================================================================")
    print(" 🚀 STARTING FULL-STACK NUCLEAR BLAST DETECTION SYSTEM SERVER ")
    print("==================================================================")
    print(" Backend REST API : http://127.0.0.1:8000/api/health")
    print(" Interactive UI   : http://127.0.0.1:8000/")
    print(" Interactive Docs : http://127.0.0.1:8000/docs")
    print(" Database File    : nuclear_detector.db (SQLite)")
    print("==================================================================\n")

    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
