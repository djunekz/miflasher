"""
MiFlasher Config Manager
"""
import os, json

CONFIG_FILE = os.path.expanduser("~/.config/miflasher/config.json")

DEFAULTS = {
    "theme":         "dark",
    "download_dir":  "~/storage/downloads/MiFlasher",
    "backup_dir":    "~/storage/downloads/MiFlasher/backups",
    "log_dir":       "~/.local/share/miflasher/logs",
    "auto_verify":   True,
    "auto_reboot":   True,
    "slot":          "all",
    "gui_port":      8080,
    "gui_host":      "localhost",
    "verbose":       False,
}


class ConfigManager:
    def __init__(self, log):
        self.log  = log
        self._cfg = self._load()

    def _load(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE) as f:
                    return {**DEFAULTS, **json.load(f)}
            except Exception:
                pass
        return dict(DEFAULTS)

    def _save(self):
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump(self._cfg, f, indent=2)

    def get(self, key):
        val = self._cfg.get(key)
        if val is None:
            self.log.warning(f"Unknown config key: {key}")
        else:
            self.log.info(f"{key} = {val}")
        return val

    def set(self, key, value):
        if key not in DEFAULTS:
            self.log.warning(f"Unknown key: {key} (will set anyway)")
        # Auto-cast bools
        if value.lower() in ("true","1","yes"):  value = True
        elif value.lower() in ("false","0","no"): value = False
        self._cfg[key] = value
        self._save()
        self.log.success(f"Set {key} = {value}")

    def show(self):
        rows = [(k, str(v)) for k, v in self._cfg.items()]
        self.log.table(["Key", "Value"], rows, title="MiFlasher Configuration")

    def reset(self):
        if self.log.confirm("Reset all config to defaults?", default=False):
            self._cfg = dict(DEFAULTS)
            self._save()
            self.log.success("Config reset to defaults.")
