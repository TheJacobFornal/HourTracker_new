# backend/run_api.py
import os
import socket
import multiprocessing
from pathlib import Path
from datetime import datetime

import uvicorn

# Import your FastAPI app instance
# Make sure app/main.py defines: app = create_app()
from app.main import app


def find_free_port(start_port: int = 8000, max_tries: int = 20) -> int:
    port = start_port
    for _ in range(max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.2)
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
        port += 1
    return start_port  # fallback


def run():
    # Ensure a logs dir
    base = Path(
        getattr(__import__("sys"), "frozen", False)
        and Path(__import__("sys").executable).parent
        or Path(__file__).parent
    )
    logs_dir = base / "logs"
    logs_dir.mkdir(exist_ok=True)
    log_file = logs_dir / f"hourtrack_api_{datetime.now().strftime('%Y%m%d')}.log"

    port = int(os.environ.get("HOURTRACK_PORT", find_free_port(8000)))
    host = os.environ.get("HOURTRACK_HOST", "127.0.0.1")

    # Start Uvicorn
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
    )


if __name__ == "__main__":
    multiprocessing.freeze_support()  # Needed for PyInstaller on Windows
    run()
