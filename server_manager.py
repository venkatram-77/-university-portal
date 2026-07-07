#!/usr/bin/env python
"""
Windows Service Manager for University Portal
Manages the server to keep it running 24/7
"""
import os
import sys
import subprocess
import time
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
LOG_DIR = Path(__file__).parent / 'logs'
LOG_DIR.mkdir(exist_ok=True)

log_file = LOG_DIR / f'server_{datetime.now().strftime("%Y%m%d")}.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
os.chdir(BASE_DIR)

def start_server():
    """Start the Gunicorn server"""
    logger.info("Starting University Portal Server...")

    cmd = [
        sys.executable, '-m', 'gunicorn',
        'university_portal.wsgi:application',
        '--bind', '0.0.0.0:8000',
        '--workers', '4',
        '--worker-class', 'sync',
        '--timeout', '90',
        '--max-requests', '1000',
        '--max-requests-jitter', '50',
        '--keep-alive', '5',
        '--access-logfile', str(LOG_DIR / 'access.log'),
        '--error-logfile', str(LOG_DIR / 'error.log'),
        '--log-level', 'info',
    ]

    try:
        process = subprocess.Popen(cmd)
        logger.info(f"Server started with PID: {process.pid}")
        return process
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        return None

def restart_server(process):
    """Restart the server"""
    logger.warning("Restarting server...")

    if process and process.poll() is None:
        try:
            process.terminate()
            process.wait(timeout=10)
            logger.info("Server stopped")
        except subprocess.TimeoutExpired:
            process.kill()
            logger.warning("Server killed forcefully")

    time.sleep(2)
    return start_server()

def monitor_server():
    """Monitor server and restart if needed"""
    logger.info("=== University Portal Server Monitor Started ===")
    logger.info(f"Admin Account: Admin1 / AdminRAM")
    logger.info(f"Access URL: http://localhost:8000")
    logger.info("Press Ctrl+C to stop")
    logger.info("=" * 50)

    process = start_server()
    restart_count = 0

    try:
        while True:
            time.sleep(5)

            # Check if process is still running
            if process is None or process.poll() is not None:
                logger.error("Server crashed!")
                restart_count += 1
                logger.warning(f"Restart attempt #{restart_count}")
                process = start_server()
                time.sleep(2)

            # Log status every 5 minutes
            if restart_count % 60 == 0 and restart_count > 0:
                logger.info(f"Server running (total restarts: {restart_count})")

    except KeyboardInterrupt:
        logger.info("Shutting down...")
        if process and process.poll() is None:
            process.terminate()
            process.wait(timeout=10)
        logger.info("Server stopped")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Monitor error: {e}")
        if process and process.poll() is None:
            process.kill()

if __name__ == '__main__':
    monitor_server()
