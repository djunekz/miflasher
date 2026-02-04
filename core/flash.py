from core.utils import run_cmd, progress_bar
from core.logger import log
import os

def flash_rom(rom_path: str):
    if not os.path.exists(rom_path):
        log(f"ROM not found: {rom_path}", level="error")
        return

    log(f"Decompressing ROM: {rom_path}")
    run_cmd(f"pv -bpe '{rom_path}' | tar -xzf- -C /sdcard/Download/mi-flash", "Extract ROM")

    # list flash scripts
    scripts = ["flash_all.sh", "flash_all_lock.sh"]
    for script in scripts:
        script_path = f"/sdcard/Download/mi-flash/{script}"
        if os.path.exists(script_path):
            log(f"Flashing script: {script_path}")
            run_cmd(f"bash {script_path}", "Flashing")
