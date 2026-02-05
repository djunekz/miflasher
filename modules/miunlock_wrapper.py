import subprocess
from core.logger import log

def run_miunlock():
    log("Running MiUnlock tool...")
    try:
        subprocess.run(["miunlock"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
