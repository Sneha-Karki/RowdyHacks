"""
Startup script to run both FastAPI backend and Flet frontend together
"""
import os
import subprocess
import sys
import time
from multiprocessing import Process

def start_api():
    """Start FastAPI backend server"""
    port = int(os.getenv("PORT", 8000))
    api_port = 8000  # Internal API port
    
    print(f"🚀 Starting FastAPI backend on port {api_port}...")
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "api:app",
        "--host", "0.0.0.0",
        "--port", str(api_port)
    ])

def start_flet():
    """Start Flet web app"""
    port = int(os.getenv("PORT", 10000))
    
    # Wait for API to start
    time.sleep(3)
    
    print(f"🚀 Starting Flet web app on port {port}...")
    subprocess.run([
        sys.executable, "main.py"
    ])

if __name__ == "__main__":
    # Start API in background process
    api_process = Process(target=start_api)
    api_process.start()
    
    # Start Flet app in main process (this is what Render exposes)
    start_flet()
