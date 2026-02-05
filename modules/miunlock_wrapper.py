import subprocess
from core.logger import log

def run_miunlock():
    """
    Jalankan MiUnlock langsung di terminal.
    Tidak menggunakan capture_output agar input user diterima.
    Tetap menangani 401 jika muncul.
    """
    log("Running MiUnlock tool...")

    try:
        process = subprocess.Popen(
            ["miunlock"],
        )
        process.wait()
        if process.returncode == 0:
            log("Bootloader unlocked!", level="success")
            return True
        else:
            log(f"MiUnlock exited with code {process.returncode}", level="error")
            return False

    except Exception as e:
        log(f"Error running MiUnlock: {e}", level="error")
        return False
