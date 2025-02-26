import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
LOG_DIR = os.path.join(BASE_DIR, "logs")


if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def write_log(service: str, message: str):
   
    log_file = os.path.join(LOG_DIR, f"{service}.log")

    with open(log_file, "a") as file:
        file.write(message + "\n")
