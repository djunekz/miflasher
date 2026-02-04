import subprocess
from core.logger import log

def detect_device():
    """Detect device connected via USB / adb / fastboot"""
    try:
        adb_output = subprocess.run(["termux-usb", "-l"], capture_output=True, text=True).stdout
        fastboot_output = subprocess.run(["fastboot", "devices"], capture_output=True, text=True).stdout

        if adb_output.strip():
            log(f"Device detected via USB/ADB: {adb_output.strip()}")
        elif fastboot_output.strip():
            log(f"Device detected via Fastboot: {fastboot_output.strip()}")
        else:
            log("No device detected", level="error")
    except Exception as e:
        log(f"Error detecting device: {e}", level="error")
