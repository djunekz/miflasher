"""
MiFlasher Session Manager
"""
import os, json
from datetime import datetime

LOG_DIR = os.path.expanduser("~/.local/share/miflasher/logs")


class Session:
    def __init__(self, log):
        self.log = log
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(LOG_DIR, exist_ok=True)
        log_path = os.path.join(LOG_DIR, f"session_{self.session_id}.jsonl")
        log.set_file(log_path)


class SessionLog:
    def __init__(self, log):
        self.log = log

    def _get_sessions(self):
        if not os.path.isdir(LOG_DIR):
            return []
        return sorted([
            f for f in os.listdir(LOG_DIR)
            if f.startswith("session_") and f.endswith(".jsonl")
        ], reverse=True)

    def list_sessions(self):
        sessions = self._get_sessions()
        if not sessions:
            self.log.info("No session logs found.")
            return
        rows = []
        for s in sessions:
            path = os.path.join(LOG_DIR, s)
            size = os.path.getsize(path)
            sid  = s.replace("session_","").replace(".jsonl","")
            rows.append([sid, f"{size} B", path])
        self.log.table(["Session ID","Size","Path"], rows, title="Session Logs")

    def tail(self, n: int = 50):
        sessions = self._get_sessions()
        if not sessions:
            self.log.info("No session logs found.")
            return
        path = os.path.join(LOG_DIR, sessions[0])
        self.log.header(f"Log: {sessions[0]}")
        lines = []
        with open(path) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    lines.append(entry)
                except Exception:
                    pass
        for entry in lines[-n:]:
            level = entry.get("level","info")
            msg   = entry.get("message","")
            ts    = entry.get("time","")[:19]
            self.log.log(f"[{ts}] {msg}", level)

    def show_session(self, session_id: str):
        path = os.path.join(LOG_DIR, f"session_{session_id}.jsonl")
        if not os.path.exists(path):
            self.log.error(f"Session not found: {session_id}")
            return
        self.tail(9999)

    def clear(self):
        if self.log.confirm("Clear ALL session logs?", default=False):
            import shutil
            shutil.rmtree(LOG_DIR, ignore_errors=True)
            os.makedirs(LOG_DIR, exist_ok=True)
            self.log.success("All logs cleared.")
