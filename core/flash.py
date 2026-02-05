import os
from core.utils import run_cmd
from core.logger import log

def flash_rom(rom_path):
    if not os.path.exists(rom_path):
        log(f"ROM not found: {rom_path}", level="error")
        return
    output_dir = "/sdcard/Download/miflasher_rom"
    os.makedirs(output_dir, exist_ok=True)
    run_cmd(f"pv -bpe '{rom_path}' | tar -xzf- -C {output_dir}", "Decompressing ROM")
    scripts = ["flash_all.sh", "flash_all_lock.sh", "flash_all_except_data_storage.sh"]
    for script in scripts:
        path = os.path.join(output_dir, script)
        if os.path.exists(path):
            run_cmd(f"bash {path}", f"Flashing {script}")

def flash_boot(boot_img):
    if not os.path.exists(boot_img):
        log(f"Boot image not found: {boot_img}", level="error")
        return
    run_cmd(f"fastboot flash boot {boot_img}", "Flashing boot image")
