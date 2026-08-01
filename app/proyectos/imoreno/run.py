"""Module for running the frontend and backend applications of the hotel system."""

import shutil
import subprocess
import sys
from pathlib import Path
from threading import Thread

import uvicorn

from app.main import app


def run_frontend():
    """Run the Go-based frontend application and initialize its dependencies if needed."""
    try:
        frontend_dir = Path(__file__).parent.joinpath("../../../frontend/imoreno").resolve()
        go_path = shutil.which('go')
        if not go_path:
            raise RuntimeError("Go executable not found in PATH")
        # Validate go executable path
        go_exec = Path(go_path)
        if not (go_exec.is_file() and go_exec.exists()):
            raise RuntimeError("Invalid Go executable")
        # Inicializar el módulo Go si no existe
        if not (frontend_dir / "go.mod").exists():
            subprocess.run([str(go_exec), "mod", "init", "hotelapp"], cwd=frontend_dir, check=True, shell=False)  # noqa: S603
            subprocess.run([str(go_exec), "get", "github.com/charmbracelet/bubbletea"], cwd=frontend_dir, check=True, shell=False)  # noqa: S603
            subprocess.run([str(go_exec), "get", "github.com/charmbracelet/lipgloss"], cwd=frontend_dir, check=True, shell=False)  # noqa: S603
            subprocess.run([str(go_exec), "mod", "tidy"], cwd=frontend_dir, check=True, shell=False)  # noqa: S603
        
        # Ejecutar la aplicación Go
        subprocess.run(["go", "run", "."], cwd=frontend_dir, check=True)  # noqa: S603, S607
    except subprocess.CalledProcessError:
        sys.exit(1)

def run_backend():
    """Run the FastAPI backend application."""
    uvicorn.run(app, host="127.0.0.1", port=8000)

def main():
    """Run both frontend and backend applications."""
    # Start backend in a separate thread
    backend_thread = Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Ejecutar el frontend en el hilo principal
    run_frontend()

if __name__ == "__main__":
    main()