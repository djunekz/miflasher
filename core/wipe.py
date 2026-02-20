"""
MiFlasher Wipe Manager
"""
import subprocess


class WipeManager:
    def __init__(self, log):
        self.log = log

    def _run(self, cmd):
        import subprocess
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return r.returncode

    def wipe(self, data=False, cache=False, dalvik=False, force=False):
        self.log.header("Wipe Partitions")

        targets = []
        if data:    targets.append(("data",   "fastboot", ["fastboot","erase","userdata"]))
        if cache:   targets.append(("cache",  "fastboot", ["fastboot","erase","cache"]))
        if dalvik:  targets.append(("dalvik", "adb",      ["adb","shell","rm","-rf",
                                    "/data/dalvik-cache"]))

        if not targets:
            self.log.warning("No wipe targets specified. Use --data, --cache, --dalvik, or --all")
            return

        self.log.warning(f"About to wipe: {', '.join(t[0] for t in targets)}")
        if not force:
            if not self.log.confirm("This is IRREVERSIBLE. Continue?", default=False):
                self.log.info("Wipe cancelled.")
                return

        for i, (name, mode, cmd) in enumerate(targets, 1):
            self.log.step(i, len(targets), f"Wiping {name}...")
            rc = self._run(cmd)
            if rc == 0:
                self.log.success(f"Wiped: {name}")
            else:
                self.log.error(f"Failed to wipe: {name}")
