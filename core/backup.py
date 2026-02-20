"""
MiFlasher Backup Manager
Full and partial partition backup/restore via fastboot or ADB.
"""

import os
import time
import subprocess
import tarfile
from datetime import datetime
from pathlib import Path


COMMON_PARTITIONS = [
    "boot", "boot_a", "boot_b",
    "recovery",
    "vbmeta", "vbmeta_a", "vbmeta_b",
    "super",
    "persist",
    "modem",
    "bluetooth",
    "dsp",
    "cust",
]


class BackupManager:

    def __init__(self, log):
        self.log = log

    def _run(self, cmd: list) -> tuple:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return r.returncode, r.stdout.strip(), r.stderr.strip()
        except Exception as e:
            return -1, "", str(e)

    def _fmt_size(self, path: str) -> str:
        if not os.path.exists(path):
            return "0 B"
        size = os.path.getsize(path)
        for u in ("B","KB","MB","GB"):
            if size < 1024: return f"{size:.1f} {u}"
            size /= 1024
        return f"{size:.1f} TB"

    def backup(self, partitions: list = None, out_dir: str = None, compress: bool = False):
        self.log.header("Partition Backup")

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_dir = out_dir or os.path.expanduser(f"~/storage/downloads/MiFlasher/backups/backup_{ts}")
        os.makedirs(out_dir, exist_ok=True)

        targets = partitions or COMMON_PARTITIONS
        self.log.info(f"Partitions: {', '.join(targets)}")
        self.log.info(f"Output:     {out_dir}")
        print()

        backed_up = []
        failed    = []

        for i, part in enumerate(targets, 1):
            out_img = os.path.join(out_dir, f"{part}.img")
            self.log.step(i, len(targets), f"Backing up: {part}")

            # Try fastboot first
            rc, _, err = self._run(["fastboot", "fetch", part, out_img])
            if rc == 0 and os.path.exists(out_img):
                self.log.success(f"  ✓ {part}.img ({self._fmt_size(out_img)})")
                backed_up.append(part)
                continue

            # Fallback: ADB pull (if partition visible in /dev/block/)
            block = f"/dev/block/by-name/{part}"
            rc, out, _ = self._run(["adb", "shell", "ls", block])
            if rc == 0:
                rc, _, err = self._run(["adb", "pull", block, out_img])
                if rc == 0 and os.path.exists(out_img):
                    self.log.success(f"  ✓ {part}.img ({self._fmt_size(out_img)}) [adb]")
                    backed_up.append(part)
                    continue

            self.log.warning(f"  ✗ Could not backup: {part} ({err})")
            failed.append(part)

        # Summary
        print()
        self.log.table(
            ["Result", "Count", "Partitions"],
            [
                ["✅ Success", str(len(backed_up)), ", ".join(backed_up) or "-"],
                ["❌ Failed",  str(len(failed)),    ", ".join(failed)    or "-"],
            ],
            title="Backup Summary"
        )

        # Compress if requested
        if compress and backed_up:
            archive = f"{out_dir}.tar.gz"
            self.log.info(f"Compressing to {archive}...")
            with tarfile.open(archive, "w:gz") as tar:
                tar.add(out_dir, arcname=os.path.basename(out_dir))
            self.log.success(f"Archive: {archive} ({self._fmt_size(archive)})")

        self.log.success(f"Backup saved to: {out_dir}")
        return out_dir

    def restore(self, path: str, partitions: list = None):
        self.log.header("Partition Restore")

        if not os.path.exists(path):
            self.log.error(f"Backup path not found: {path}")
            return False

        # If archive, extract first
        if path.endswith(".tar.gz") or path.endswith(".tgz"):
            self.log.info(f"Extracting archive: {path}")
            extract_dir = path.replace(".tar.gz", "").replace(".tgz", "")
            os.makedirs(extract_dir, exist_ok=True)
            with tarfile.open(path) as tar:
                tar.extractall(extract_dir)
            path = extract_dir

        imgs = list(Path(path).glob("*.img"))
        if not imgs:
            self.log.error("No .img files found in backup!")
            return False

        if partitions:
            imgs = [img for img in imgs if img.stem in partitions]

        self.log.info(f"Found {len(imgs)} image(s) to restore")
        if not self.log.confirm(f"Restore {len(imgs)} partition(s)?", default=False):
            self.log.info("Restore cancelled.")
            return False

        success = True
        for i, img in enumerate(imgs, 1):
            partition = img.stem
            self.log.step(i, len(imgs), f"Restoring {partition}")
            rc, _, err = self._run(["fastboot", "flash", partition, str(img)])
            if rc == 0:
                self.log.success(f"  ✓ {partition}")
            else:
                self.log.error(f"  ✗ {partition}: {err}")
                success = False

        if success:
            self.log.success("Restore complete! Rebooting...")
            self._run(["fastboot", "reboot"])
        return success
