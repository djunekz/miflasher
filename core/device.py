import subprocess
from core.logger import log

def detect_device():
    log("Detecting device...")
    try:
        adb_out = subprocess.run(["termux-usb", "-l"], capture_output=True, text=True).stdout.strip()
        fastboot_out = subprocess.run(["fastboot", "devices"], capture_output=True, text=True).stdout.strip()

        if adb_out:
            log(f"Device detected via USB/ADB: {adb_out}", level="success")
        elif fastboot_out:
            log(f"Device detected via Fastboot: {fastboot_out}", level="success")
        else:
            log("No device detected", level="error")
    except Exception as e:
        log(f"Error detecting device: {e}", level="error")
