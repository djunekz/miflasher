import subprocess
from core.logger import log

def detect_device():
    log("Detecting device...")
    try:
        adb = subprocess.run(["termux-usb", "-l"], capture_output=True, text=True).stdout.strip()
        fast = subprocess.run(["fastboot", "devices"], capture_output=True, text=True).stdout.strip()
        return adb or fast
    except Exception as e:
        log(f"Error detecting device: {e}", level="error")
        return None

def show_device_info():
    device = detect_device()
    if device:
        log(f"Device detected: {device}", level="success")
    else:
        log("No device detected!", level="error")
