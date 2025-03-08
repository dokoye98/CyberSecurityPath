from fastapi import FastAPI
from api import router as api_router
import uvicorn
import subprocess
import os

app = FastAPI()

app.include_router(api_router, prefix="/api")

ssh_honeypot_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "honeypots/ssh_server.py"))
telnet_honeypot_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "honeypots/telnet_server.py"))

def start_ssh_honeypot():
    
    print("Starting Telnet Honeypot...")
    subprocess.Popen(["python", telnet_honeypot_script])
   

@app.on_event("startup")
async def startup_event():
    start_ssh_honeypot()



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
