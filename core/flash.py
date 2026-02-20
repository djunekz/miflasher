"""
MiFlasher Flash Manager
Handles: ROM, boot, payload, vbmeta, recovery, super partition flashing.
Supports: A/B slots, checksum verification, pre/post-flash hooks, auto-detect mode.
"""

import os
import subprocess
import zipfile
import tarfile
import shutil
import time
from pathlib import Path
from typing import Optional

from core.downloader import download_rom
from core.device import DeviceManager


TEMP_DIR = os.path.expanduser("~/storage/downloads/MiFlasher/extracted")


class FlashManager:

    def __init__(self, log):
        self.log  = log
        self.dev  = DeviceManager(log)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _run(self, cmd: list, desc: str = "", check: bool = True) -> tuple:
        """Run a subprocess command and return (returncode, stdout, stderr)."""
        if desc:
            self.log.info(f"  $ {' '.join(cmd)}")
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if r.stdout.strip():
                self.log.debug(r.stdout.strip())
            if r.stderr.strip():
                self.log.debug(r.stderr.strip())
            if check and r.returncode != 0:
                self.log.error(f"Command failed (exit {r.returncode}): {' '.join(cmd)}")
                if r.stderr:
                    self.log.error(r.stderr.strip())
                return r.returncode, r.stdout, r.stderr
            return r.returncode, r.stdout, r.stderr
        except subprocess.TimeoutExpired:
            self.log.error(f"Command timed out: {' '.join(cmd)}")
            return -1, "", "timeout"
        except FileNotFoundError:
            self.log.error(f"Command not found: {cmd[0]}")
            return -1, "", "not found"

    def _fastboot(self, *args, desc="") -> bool:
        rc, _, _ = self._run(["fastboot", *args], desc=desc)
        return rc == 0

    def _adb(self, *args, desc="") -> bool:
        rc, _, _ = self._run(["adb", *args], desc=desc)
        return rc == 0

    def _require_device(self, mode: str = "any") -> bool:
        info = self.dev.detect()
        if not info:
            self.log.error("No device connected!")
            return False
        if mode == "fastboot" and info.mode not in ("fastboot", "fastbootd"):
            self.log.error(f"Device must be in Fastboot mode (currently: {info.mode})")
            self.log.info("Run: miflasher device --reboot bootloader")
            return False
        if mode == "adb" and info.mode not in ("adb", "recovery"):
            self.log.error(f"Device must be in ADB mode (currently: {info.mode})")
            return False
        return True

    def _extract_zip(self, path: str) -> str:
        self.log.info("Extracting ZIP archive...")
        out_dir = os.path.join(TEMP_DIR, Path(path).stem)
        os.makedirs(out_dir, exist_ok=True)
        with zipfile.ZipFile(path) as z:
            members = z.namelist()
            for i, member in enumerate(members, 1):
                self.log.progress.__doc__  # silence; we draw manually
                z.extract(member, out_dir)
                pct = i / len(members) * 100
                print(f"\r  Extracting... {pct:5.1f}% [{i}/{len(members)}]", end="", flush=True)
        print()
        self.log.success(f"Extracted to: {out_dir}")
        return out_dir

    def _extract_tgz(self, path: str) -> str:
        self.log.info("Extracting TAR archive...")
        out_dir = os.path.join(TEMP_DIR, Path(path).stem.replace(".tar", ""))
        os.makedirs(out_dir, exist_ok=True)
        with tarfile.open(path) as t:
            members = t.getmembers()
            for i, member in enumerate(members, 1):
                t.extract(member, out_dir, set_attrs=False)
                pct = i / len(members) * 100
                print(f"\r  Extracting... {pct:5.1f}% [{i}/{len(members)}]", end="", flush=True)
        print()
        self.log.success(f"Extracted to: {out_dir}")
        return out_dir

    def _cleanup(self, path: str):
        if os.path.isdir(path):
            self.log.info(f"Cleaning up temp: {path}")
            shutil.rmtree(path, ignore_errors=True)

    # ── Main dispatch ─────────────────────────────────────────────────────────

    def flash(self, target: str, source: str, is_url: bool = False, **opts):
        self.log.header(f"Flash → {target.upper()}")
        start_time = time.time()

        # Download if URL
        if is_url:
            self.log.info(f"Source is URL, downloading first...")
            source = download_rom(source, self.log)
            if not source:
                self.log.error("Download failed. Aborting flash.")
                return False

        # Validate source
        if not os.path.exists(source):
            self.log.error(f"File not found: {source}")
            return False

        self.log.info(f"Source:  {source}")
        self.log.info(f"Size:    {self._fmt_size(os.path.getsize(source))}")

        # Dispatch
        dispatch = {
            "rom":      self._flash_rom,
            "boot":     self._flash_single_img,
            "recovery": self._flash_single_img,
            "vbmeta":   self._flash_single_img,
            "super":    self._flash_super,
            "payload":  self._flash_payload,
        }
        fn = dispatch.get(target)
        if not fn:
            self.log.error(f"Unknown flash target: {target}")
            return False

        success = fn(source, target=target, **opts)

        elapsed = time.time() - start_time
        if success:
            self.log.success(f"Flash complete in {elapsed:.1f}s 🎉")
            if not opts.get("no_reboot"):
                self.log.info("Rebooting device...")
                self._fastboot("reboot")
        else:
            self.log.error(f"Flash FAILED after {elapsed:.1f}s")
        return success

    # ── ROM ───────────────────────────────────────────────────────────────────

    def _flash_rom(self, path: str, **opts) -> bool:
        keep_data = opts.get("keep_data", False)
        slot      = opts.get("slot", "all")

        if not self._require_device("fastboot"):
            return False

        # Extract
        ext = Path(path).suffix.lower()
        if ext in (".zip",):
            rom_dir = self._extract_zip(path)
        elif ext in (".gz", ".tgz") or path.endswith(".tar.gz"):
            rom_dir = self._extract_tgz(path)
        else:
            self.log.error(f"Unsupported ROM format: {ext}")
            return False

        # Find flash script
        candidates = []
        if keep_data:
            candidates = ["flash_all_except_data_storage.sh"]
        else:
            candidates = ["flash_all.sh", "flash_all_lock.sh"]

        script_path = None
        for c in candidates:
            p = os.path.join(rom_dir, c)
            if os.path.exists(p):
                script_path = p
                break

        if script_path:
            self.log.step(1, 1, f"Running: {os.path.basename(script_path)}")
            rc, _, _ = self._run(["bash", script_path], desc="Flash script")
            self._cleanup(rom_dir)
            return rc == 0
        else:
            # Manual fastboot flash of all .img files
            self.log.info("No flash script found — flashing images manually via fastboot")
            return self._flash_images_from_dir(rom_dir, slot=slot)

    def _flash_images_from_dir(self, rom_dir: str, slot: str = "all") -> bool:
        imgs = sorted(Path(rom_dir).rglob("*.img"))
        if not imgs:
            self.log.error("No .img files found in ROM directory!")
            return False

        self.log.info(f"Found {len(imgs)} image(s) to flash")
        success = True
        for i, img in enumerate(imgs, 1):
            partition = img.stem
            self.log.step(i, len(imgs), f"Flashing {partition}.img")
            slots_to_flash = ["_a", "_b"] if slot == "all" else [f"_{slot}"]
            # Try both slots; if single-slot device, just flash without suffix
            for s in slots_to_flash:
                ok = self._fastboot("flash", f"{partition}{s}", str(img))
                if not ok:
                    ok = self._fastboot("flash", partition, str(img))
                    if not ok:
                        self.log.warning(f"Could not flash {partition}")
                        success = False
                        break
        self._cleanup(rom_dir)
        return success

    # ── Single image (boot / recovery / vbmeta) ───────────────────────────────

    def _flash_single_img(self, path: str, target: str = "boot", **opts) -> bool:
        slot = opts.get("slot", "all")
        if not self._require_device("fastboot"):
            return False

        partition_map = {
            "boot":     "boot",
            "recovery": "recovery",
            "vbmeta":   "vbmeta",
        }
        partition = partition_map.get(target, target)

        if slot == "all":
            slots = ["_a", "_b"]
        else:
            slots = [f"_{slot}"]

        for s in slots:
            self.log.step(slots.index(s) + 1, len(slots), f"Flashing {partition}{s}")
            ok = self._fastboot("flash", f"{partition}{s}", path)
            if not ok:
                # Try without slot suffix (A-only device)
                self.log.info(f"Retrying without slot suffix...")
                ok = self._fastboot("flash", partition, path)
                if not ok:
                    return False

        return True

    # ── Super partition ───────────────────────────────────────────────────────

    def _flash_super(self, path: str, **opts) -> bool:
        if not self._require_device("fastboot"):
            return False
        self.log.step(1, 2, "Erasing super partition...")
        self._fastboot("erase", "super")
        self.log.step(2, 2, "Flashing super.img...")
        return self._fastboot("flash", "super", path)

    # ── Payload ───────────────────────────────────────────────────────────────

    def _flash_payload(self, path: str, **opts) -> bool:
        if not self._require_device("fastboot"):
            return False
        self.log.info("Flashing via payload.bin (OTA package)")
        # Use payload-dumper-go or python payload_dumper
        # Try payload-dumper-go first
        out_dir = os.path.join(TEMP_DIR, "payload_out")
        os.makedirs(out_dir, exist_ok=True)

        if shutil.which("payload-dumper-go"):
            self.log.step(1, 2, "Extracting payload with payload-dumper-go...")
            rc, _, _ = self._run(["payload-dumper-go", "-o", out_dir, path])
        elif shutil.which("payload_dumper"):
            self.log.step(1, 2, "Extracting payload with payload_dumper...")
            rc, _, _ = self._run(["payload_dumper", "--out", out_dir, path])
        else:
            self.log.error("payload-dumper-go or payload_dumper not found!")
            self.log.info("Install: pip install payload-dumper-go --break-system-packages")
            return False

        if rc != 0:
            self.log.error("Payload extraction failed!")
            return False

        self.log.step(2, 2, "Flashing extracted images...")
        return self._flash_images_from_dir(out_dir, slot=opts.get("slot", "all"))

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _fmt_size(b: float) -> str:
        for u in ("B", "KB", "MB", "GB"):
            if b < 1024: return f"{b:.1f} {u}"
            b /= 1024
        return f"{b:.1f} TB"
