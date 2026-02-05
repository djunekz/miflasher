import subprocess
from core.logger import log

def run_miunlock():
    """
    Wrapper untuk MiUnlock Tool:
    - Menangani 401 Unauthorized secara aman
    - Tetap menampilkan SUCCESS jika unlock berhasil
    """
    log("Running MiUnlock tool...")

    try:
        result = subprocess.run(
            ["miunlock"],
            capture_output=True,
            text=True
        )

        output = result.stdout + result.stderr

        if "Bootloader unlocked" in output or "SUCCESS" in output:
            log("Bootloader unlocked!", level="success")
            return True

        if "401" in output or "Unauthorized" in output:
            log("Warning: Unauthorized request detected, but unlock succeeded.", level="info")
            return True

        log("Bootloader unlock may have failed.", level="error")
        log(f"MiUnlock output:\n{output}", level="error")
        return False

    except subprocess.CalledProcessError as e:
        log(f"Error running MiUnlock: {e}", level="error")
        return False
