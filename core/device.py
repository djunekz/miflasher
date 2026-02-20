"""
MiFlasher Device Manager
Handles ADB/Fastboot device detection, info gathering, and reboot modes.
"""

import subprocess
import json
import time
import re
import os
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class DeviceInfo:
    serial:      str = "unknown"
    mode:        str = "unknown"     # adb | fastboot | fastbootd | recovery | edl
    brand:       str = "unknown"
    model:       str = "unknown"
    codename:    str = "unknown"
    android:     str = "unknown"
    miui:        str = "unknown"
    build:       str = "unknown"
    cpu_abi:     str = "unknown"
    battery:     str = "unknown"
    slot:        str = "unknown"     # a | b | N/A
    unlocked:    str = "unknown"     # yes | no | unknown
    storage:     str = "unknown"
    ram:         str = "unknown"
    display:     str = "unknown"
    kernel:      str = "unknown"
    security:    str = "unknown"     # Android security patch


class DeviceManager:

    REBOOT_CMDS = {
        "system":      ["adb", "reboot"],
        "bootloader":  ["adb", "reboot", "bootloader"],
        "recovery":    ["adb", "reboot", "recovery"],
        "fastbootd":   ["fastboot", "reboot-recovery"],
        "edl":         ["adb", "reboot", "edl"],
    }
    FASTBOOT_REBOOT = {
        "system":     ["fastboot", "reboot"],
        "bootloader": ["fastboot", "reboot-bootloader"],
        "recovery":   ["fastboot", "reboot-recovery"],
        "fastbootd":  ["fastboot", "reboot-recovery"],
        "edl":        ["fastboot", "oem", "edl"],
    }

    def __init__(self, log):
        self.log  = log
        self._info: Optional[DeviceInfo] = None

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _run(self, cmd: list, timeout: int = 8) -> str:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return (r.stdout + r.stderr).strip()
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            return ""

    def _adb(self, *args) -> str:
        return self._run(["adb", *args])

    def _adb_prop(self, prop: str) -> str:
        return self._adb("shell", "getprop", prop)

    def _fastboot(self, *args) -> str:
        return self._run(["fastboot", *args])

    def _fastboot_var(self, var: str) -> str:
        out = self._fastboot("getvar", var)
        # output is "var: value"
        for line in out.splitlines():
            if var in line:
                return line.split(":", 1)[-1].strip()
        return ""

    # ── Detection ─────────────────────────────────────────────────────────────

    def detect(self) -> Optional[DeviceInfo]:
        info = DeviceInfo()

        # 1. Try ADB
        adb_out = self._run(["adb", "devices"])
        adb_lines = [l for l in adb_out.splitlines()[1:] if l.strip() and "offline" not in l]
        if adb_lines:
            info.serial = adb_lines[0].split()[0]
            state       = adb_lines[0].split()[-1]  # device | recovery | sideload
            if state == "recovery":
                info.mode = "recovery"
            else:
                info.mode = "adb"
            self._gather_adb(info)
            self._info = info
            return info

        # 2. Try Fastboot
        fb_out = self._run(["fastboot", "devices"])
        fb_lines = [l for l in fb_out.splitlines() if l.strip()]
        if fb_lines:
            info.serial = fb_lines[0].split()[0]
            info.mode   = "fastboot"
            self._gather_fastboot(info)
            self._info = info
            return info

        # 3. Termux USB
        usb_out = self._run(["termux-usb", "-l"])
        if usb_out:
            info.serial = usb_out.split("\n")[0].strip()
            info.mode   = "usb-unknown"
            self._info = info
            return info

        self._info = None
        return None

    def _gather_adb(self, info: DeviceInfo):
        """Populate DeviceInfo via ADB shell getprop."""
        props = {
            "brand":    "ro.product.brand",
            "model":    "ro.product.model",
            "codename": "ro.product.device",
            "android":  "ro.build.version.release",
            "miui":     "ro.miui.ui.version.name",
            "build":    "ro.build.display.id",
            "cpu_abi":  "ro.product.cpu.abi",
            "kernel":   "ro.kernel.version",
            "security": "ro.build.version.security_patch",
        }
        for attr, prop in props.items():
            val = self._adb_prop(prop)
            if val:
                setattr(info, attr, val)

        # Battery
        bat = self._adb("shell", "dumpsys", "battery")
        level_m = re.search(r"level:\s*(\d+)", bat)
        status_m = re.search(r"status:\s*(\d+)", bat)
        stat_map = {"1":"Unknown","2":"Charging","3":"Discharging","4":"Not charging","5":"Full"}
        if level_m:
            level   = level_m.group(1)
            status  = stat_map.get(status_m.group(1) if status_m else "", "?")
            info.battery = f"{level}% ({status})"

        # Slot (A/B)
        slot = self._adb_prop("ro.boot.slot_suffix")
        info.slot = slot if slot else "N/A (A-only)"

        # Bootloader lock state
        verif = self._adb_prop("ro.boot.verifiedbootstate")
        lock  = self._adb_prop("ro.boot.flash.locked")
        if verif == "green" or lock == "1":
            info.unlocked = "no (locked)"
        elif verif in ("orange", "yellow") or lock == "0":
            info.unlocked = "yes (unlocked)"

        # Storage
        df = self._adb("shell", "df", "/data")
        for line in df.splitlines():
            parts = line.split()
            if len(parts) >= 4 and "/data" in line:
                try:
                    used = int(parts[2]) // 1024
                    avail= int(parts[3]) // 1024
                    info.storage = f"{used} MB used / {avail} MB free"
                except Exception:
                    pass
                break

        # RAM
        mem = self._adb("shell", "cat", "/proc/meminfo")
        total_m = re.search(r"MemTotal:\s*(\d+)", mem)
        avail_m = re.search(r"MemAvailable:\s*(\d+)", mem)
        if total_m and avail_m:
            total_mb = int(total_m.group(1)) // 1024
            avail_mb = int(avail_m.group(1)) // 1024
            info.ram = f"{avail_mb} MB free / {total_mb} MB total"

        # Display
        wm = self._adb("shell", "wm", "size")
        den = self._adb("shell", "wm", "density")
        if wm:
            size_m = re.search(r"(\d+x\d+)", wm)
            den_m  = re.search(r"(\d+)", den)
            if size_m:
                info.display = size_m.group(1)
                if den_m:
                    info.display += f" @ {den_m.group(1)} DPI"

    def _gather_fastboot(self, info: DeviceInfo):
        """Populate DeviceInfo via fastboot getvar."""
        varmap = {
            "product":           "codename",
            "version-baseband":  "build",
            "slot-count":        "slot",
            "current-slot":      None,
            "unlocked":          "unlocked",
        }
        current_slot = self._fastboot_var("current-slot")
        for var, attr in varmap.items():
            val = self._fastboot_var(var)
            if val and attr:
                setattr(info, attr, val)
        if current_slot:
            info.slot = f"_{current_slot}"

        # unlocked comes as "yes" / "no" from fastboot
        ul = self._fastboot_var("unlocked")
        info.unlocked = "yes (unlocked)" if ul == "yes" else "no (locked)" if ul == "no" else "unknown"

    # ── Public API ────────────────────────────────────────────────────────────

    def show_info(self, json_output=False):
        self.log.header("Device Detection")
        info = self.detect()
        if not info:
            self.log.error("No device detected. Check USB cable & USB Debugging.")
            self.log.info("Tips:")
            self.log.info("  • Enable Developer Options → USB Debugging")
            self.log.info("  • For Fastboot: hold Vol- + Power during boot")
            self.log.info("  • Run: adb kill-server && adb start-server")
            return

        if json_output:
            print(json.dumps(asdict(info), indent=2))
            return

        rows = [
            ("Serial",           info.serial),
            ("Mode",             info.mode.upper()),
            ("Brand",            info.brand),
            ("Model",            info.model),
            ("Codename",         info.codename),
            ("Android Version",  info.android),
            ("MIUI Version",     info.miui),
            ("Build ID",         info.build),
            ("Security Patch",   info.security),
            ("CPU ABI",          info.cpu_abi),
            ("RAM",              info.ram),
            ("Storage",          info.storage),
            ("Display",          info.display),
            ("Slot",             info.slot),
            ("Bootloader",       info.unlocked),
            ("Battery",          info.battery),
            ("Kernel",           info.kernel),
        ]
        self.log.table(["Property", "Value"], rows, title="Device Information")

    def watch(self, interval: float = 2.0):
        """Watch for device connect/disconnect in real-time."""
        self.log.header("Device Watch Mode")
        self.log.info("Watching for device changes... (Ctrl+C to stop)")
        last_serial = None
        try:
            while True:
                info = self.detect()
                serial = info.serial if info else None
                if serial != last_serial:
                    if info:
                        self.log.success(f"Device connected: {info.brand} {info.model} ({info.serial}) [{info.mode.upper()}]")
                    else:
                        self.log.warning("Device disconnected.")
                    last_serial = serial
                time.sleep(interval)
        except KeyboardInterrupt:
            self.log.info("Watch stopped.")

    def reboot(self, mode: str):
        """Reboot connected device to specified mode."""
        self.log.header(f"Reboot → {mode.upper()}")
        info = self.detect()
        if not info:
            self.log.error("No device connected.")
            return False

        if info.mode in ("adb", "recovery"):
            cmd = self.REBOOT_CMDS.get(mode)
        else:
            cmd = self.FASTBOOT_REBOOT.get(mode)

        if not cmd:
            self.log.error(f"Unknown mode: {mode}")
            return False

        self.log.step(1, 1, f"Rebooting to {mode}...")
        out = self._run(cmd)
        if out:
            self.log.debug(out)
        self.log.success(f"Reboot command sent → {mode}")
        return True
