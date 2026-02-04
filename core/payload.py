from core.utils import run_cmd
from core.logger import log
import os

def flash_payload(payload_file):
    if not os.path.exists(payload_file):
        log(f"Payload not found: {payload_file}", level="error")
        return
    run_cmd(f"python3 -m fcetool {payload_file}", "Flashing payload")
