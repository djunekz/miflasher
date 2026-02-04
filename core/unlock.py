from modules.miunlock_wrapper import run_miunlock
from core.logger import log

def unlock_bootloader():
    """Wrapper for official miunlock binary"""
    log("Starting bootloader unlock...")
    success = run_miunlock()
    if success:
        log("Bootloader unlocked successfully")
    else:
        log("Bootloader unlock failed", level="error")
