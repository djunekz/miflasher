"""
MiFlasher Logger — Rich colorful logging with file output support.
"""

import sys
import os
import time
import json
from datetime import datetime


class Logger:
    COLORS = {
        "debug":   "\033[2;37m",
        "info":    "\033[1;34m",
        "success": "\033[1;32m",
        "warning": "\033[1;33m",
        "error":   "\033[1;31m",
        "critical":"\033[1;41m",
        "step":    "\033[1;36m",
        "header":  "\033[1;35m",
    }
    ICONS = {
        "debug":   "🔍",
        "info":    "ℹ ",
        "success": "✅",
        "warning": "⚠️ ",
        "error":   "❌",
        "critical":"🔥",
        "step":    "▶ ",
        "header":  "━━",
    }
    RESET = "\033[0m"

    def __init__(self):
        self.verbose  = False
        self.no_color = False
        self._file    = None
        self._entries = []  # in-memory log buffer

    def set_file(self, path):
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        self._file = open(path, "a", encoding="utf-8")

    def _format(self, level, msg, timestamp=True):
        ts = datetime.now().strftime("%H:%M:%S") if timestamp else ""
        icon = self.ICONS.get(level, "  ")
        if self.no_color:
            return f"[{ts}] {level.upper():8s} {icon} {msg}"
        color = self.COLORS.get(level, "")
        return f"\033[2m[{ts}]\033[0m {color}{level.upper():8s} {icon} {msg}{self.RESET}"

    def _write(self, level, msg):
        entry = {
            "time":    datetime.now().isoformat(),
            "level":   level,
            "message": msg,
        }
        self._entries.append(entry)
        if self._file:
            self._file.write(json.dumps(entry) + "\n")
            self._file.flush()

    def __call__(self, msg, level="info"):
        """Shorthand: log('msg') or log('msg', 'error')"""
        self.log(msg, level)

    def log(self, msg, level="info"):
        if level == "debug" and not self.verbose:
            return
        print(self._format(level, msg), flush=True)
        self._write(level, msg)

    def debug(self, msg):   self.log(msg, "debug")
    def info(self, msg):    self.log(msg, "info")
    def success(self, msg): self.log(msg, "success")
    def warning(self, msg): self.log(msg, "warning")
    def error(self, msg):   self.log(msg, "error")
    def critical(self, msg):self.log(msg, "critical")

    def step(self, n, total, msg):
        """Log a numbered step."""
        self.log(f"[{n}/{total}] {msg}", "step")

    def header(self, msg):
        """Print a section header."""
        sep = "─" * (len(msg) + 4)
        print(f"\n\033[1;35m  ┌{sep}┐\033[0m")
        print(f"\033[1;35m  │  {msg}  │\033[0m")
        print(f"\033[1;35m  └{sep}┘\033[0m\n")
        self._write("header", msg)

    def confirm(self, msg, default=False):
        """Prompt user for yes/no confirmation."""
        yn = "Y/n" if default else "y/N"
        try:
            ans = input(f"\033[1;33m  ⚡ {msg} [{yn}]: \033[0m").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return False
        if ans == "":
            return default
        return ans in ("y", "yes")

    def progress(self, iterable, desc="Progress", total=None, unit="B"):
        """
        Rich progress bar wrapping any iterable.
        Returns a generator that yields items while drawing progress.
        """
        import shutil
        term_width = shutil.get_terminal_size((80, 20)).columns
        bar_width  = min(35, term_width - 40)

        total_size = total or (len(iterable) if hasattr(iterable, "__len__") else None)
        start_time = time.time()
        done       = 0

        def fmt_size(b):
            for u in ("B","KB","MB","GB"):
                if b < 1024: return f"{b:.1f}{u}"
                b /= 1024
            return f"{b:.1f}TB"

        def fmt_speed(bps):
            return fmt_size(bps) + "/s"

        def fmt_eta(secs):
            if secs < 60: return f"{int(secs)}s"
            return f"{int(secs//60)}m{int(secs%60):02d}s"

        def draw(done_bytes):
            elapsed = max(time.time() - start_time, 0.001)
            speed   = done_bytes / elapsed

            if total_size:
                frac    = min(done_bytes / total_size, 1.0)
                filled  = int(bar_width * frac)
                bar     = "█" * filled + "░" * (bar_width - filled)
                pct     = f"{frac*100:5.1f}%"
                eta_sec = (total_size - done_bytes) / max(speed, 1)
                eta_str = fmt_eta(eta_sec)
                size_str= f"{fmt_size(done_bytes)}/{fmt_size(total_size)}"
                line    = (f"  \033[1;36m{desc}\033[0m "
                           f"\033[1;34m[{bar}]\033[0m "
                           f"\033[1;32m{pct}\033[0m "
                           f"\033[2m{size_str} @ {fmt_speed(speed)} ETA {eta_str}\033[0m")
            else:
                spinner = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"[int(elapsed * 5) % 10]
                line    = (f"  \033[1;36m{desc}\033[0m "
                           f"\033[1;34m{spinner}\033[0m "
                           f"\033[2m{fmt_size(done_bytes)} @ {fmt_speed(speed)}\033[0m")

            sys.stdout.write("\r" + line[:term_width])
            sys.stdout.flush()

        for item in iterable:
            yield item
            if isinstance(item, (bytes, bytearray)):
                done += len(item)
            else:
                done += 1
            draw(done)

        elapsed = max(time.time() - start_time, 0.001)
        final_size = fmt_size(done)
        print(f"\r  \033[1;32m✅ {desc}: {final_size} in {elapsed:.1f}s\033[0m" + " " * 20)

    def table(self, headers, rows, title=None):
        """Print a neat ASCII table."""
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))

        sep  = "  +" + "+".join("-" * (w + 2) for w in col_widths) + "+"
        hdr  = "  |" + "|".join(f" {h:<{col_widths[i]}} " for i, h in enumerate(headers)) + "|"

        if title:
            print(f"\n  \033[1;35m{title}\033[0m")
        print(sep)
        print(f"\033[1;36m{hdr}\033[0m")
        print(sep)
        for row in rows:
            line = "  |" + "|".join(f" {str(c):<{col_widths[i]}} " for i, c in enumerate(row)) + "|"
            print(line)
        print(sep)
        print()

    def get_entries(self):
        return list(self._entries)

    def close(self):
        if self._file:
            self._file.close()
