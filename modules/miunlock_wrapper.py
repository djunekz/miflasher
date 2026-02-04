from core.logger import log
import subprocess

def run_miunlock():
    log("Running official MiUnlockTool...")
    try:
        subprocess.run(["miunlock"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
