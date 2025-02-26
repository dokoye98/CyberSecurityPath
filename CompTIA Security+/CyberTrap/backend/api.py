from fastapi import APIRouter
from utils.logger import write_log
import os

# Ensure logs are read from the correct directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Create router
router = APIRouter()

@router.get("/")
async def root():
    return {"message": "API is running from API Router"}

@router.post("/logs/{service}")
async def add_log(service: str, message: str):
    """
    Write a log entry for a service.

    Args:
        service (str): The service name (ssh, ftp, telnet).
        message (str): The log message.

    Returns:
        JSON object confirming log entry.
    """
    valid_services = ["ssh", "ftp", "telnet"]

    if service not in valid_services:
        return {"error": "Invalid service name"}

    write_log(service, message)
    return {"success": f"Log added to {service}.log"}

@router.get("/logs/{service}")
async def get_logs(service: str):
    """
    Fetch logs from the respective service log files.

    Args:
        service (str): The service name (ssh, ftp, telnet).

    Returns:
        JSON object containing the logs or an error message.
    """
    log_file = os.path.join(LOG_DIR, f"{service}.log")

    if not os.path.exists(log_file):
        return {"error": f"Log file for {service} not found"}

    try:
        with open(log_file, "r") as file:
            log_data = file.readlines()
        return {"logs": log_data}
    except Exception as e:
        return {"error": f"Failed to read logs: {str(e)}"}
