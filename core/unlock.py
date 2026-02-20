"""
MiFlasher Unlock Manager
Routes to MiUnlockWrapper — no USB required for Mi Account auth step.
"""

import subprocess


class UnlockManager:

    def __init__(self, log):
        self.log = log

    def _run(self, cmd: list, timeout: int = 30) -> tuple:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return r.returncode, r.stdout.strip(), r.stderr.strip()
        except Exception as e:
            return -1, "", str(e)

    def unlock(self, force: bool = False, token: str = None, fastboot_only: bool = False):
        self.log.header("Bootloader Unlock")

        self.log.warning("Unlocking the bootloader WILL wipe all user data!")
        self.log.warning("Make sure you have backed up all important files.")
        print()

        if not force:
            if not self.log.confirm("Continue with bootloader unlock?", default=False):
                self.log.info("Unlock cancelled.")
                return False

        from modules.miunlock_wrapper import MiUnlockWrapper
        wrapper = MiUnlockWrapper(self.log)
        return wrapper.run(token=token, fastboot_only=fastboot_only)
