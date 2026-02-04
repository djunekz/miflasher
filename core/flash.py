from core.utils import run_cmd
from core.logger import log
import os

def flash_rom(rom_path):
    if not os.path.exists(rom_path):
        log(f"ROM not found: {rom_path}", level="error")
        return
    log(f"Decompressing ROM: {rom_path}")
    output_dir = "/sdcard/Download/mi-flash"
    os.makedirs(output_dir, exist_ok=True)
    run_cmd(f"pv -bpe '{rom_path}' | tar -xzf- -C {output_dir}", "Extract ROM")

    # run flash scripts
    for script in ["flash_all.sh", "flash_all_lock.sh"]:
        script_path = os.path.join(output_dir, script)
        if os.path.exists(script_path):
            run_cmd(f"bash {script_path}", f"Flashing {script}")
