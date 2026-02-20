"""
MiFlasher Downloader
Supports: resumable downloads, MD5/SHA256 verification, progress bar, mirrors.
"""

import os
import hashlib
import time
import requests
from pathlib import Path
from typing import Optional


DEFAULT_DEST = os.path.expanduser("~/storage/downloads/MiFlasher")


class Downloader:

    CHUNK_SIZE  = 1024 * 1024  # 1 MB
    MAX_RETRIES = 3
    RETRY_DELAY = 3  # seconds

    def __init__(self, log):
        self.log = log

    # ── Checksum ──────────────────────────────────────────────────────────────

    def _checksum(self, path: str, algo: str = "sha256") -> str:
        h = hashlib.new(algo)
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def verify(self, path: str, expected: str, algo: str = "sha256") -> bool:
        self.log.info(f"Verifying {algo.upper()} checksum...")
        actual = self._checksum(path, algo)
        if actual.lower() == expected.lower():
            self.log.success(f"Checksum OK: {actual[:16]}...")
            return True
        else:
            self.log.error(f"Checksum MISMATCH!")
            self.log.error(f"  Expected: {expected}")
            self.log.error(f"  Got:      {actual}")
            return False

    # ── Download ──────────────────────────────────────────────────────────────

    def download(
        self,
        url: str,
        dest_dir: str = DEFAULT_DEST,
        filename: Optional[str] = None,
        checksum: Optional[str] = None,
        checksum_algo: str = "sha256",
        resume: bool = True,
    ) -> Optional[str]:
        os.makedirs(dest_dir, exist_ok=True)
        filename = filename or url.split("?")[0].split("/")[-1] or "rom_download"
        dest     = os.path.join(dest_dir, filename)
        tmp      = dest + ".miflasher_part"

        self.log.header("Download")
        self.log.info(f"URL:  {url}")
        self.log.info(f"Dest: {dest}")

        existing = os.path.getsize(tmp) if os.path.exists(tmp) else 0

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                headers = {}
                if resume and existing > 0:
                    headers["Range"] = f"bytes={existing}-"
                    self.log.info(f"Resuming from {self._fmt_size(existing)} (attempt {attempt})")
                else:
                    self.log.info(f"Starting download (attempt {attempt})")

                with requests.get(url, headers=headers, stream=True, timeout=30) as r:
                    r.raise_for_status()

                    total = int(r.headers.get("content-length", 0))
                    if r.status_code == 206:       # partial content
                        total += existing
                    elif r.status_code == 200:
                        existing = 0               # server doesn't support range

                    mode  = "ab" if (resume and existing > 0) else "wb"
                    start = time.time()
                    done  = existing

                    with open(tmp, mode) as f:
                        for chunk in self.log.progress(
                            r.iter_content(chunk_size=self.CHUNK_SIZE),
                            desc="Downloading",
                            total=total if total else None,
                            unit="B",
                        ):
                            if chunk:
                                f.write(chunk)
                                done += len(chunk)

                # Download complete — rename temp file
                os.replace(tmp, dest)
                elapsed = max(time.time() - start, 0.001)
                self.log.success(
                    f"Download complete: {self._fmt_size(os.path.getsize(dest))} "
                    f"in {elapsed:.1f}s ({self._fmt_size(os.path.getsize(dest)/elapsed)}/s avg)"
                )

                # Verify checksum if provided
                if checksum:
                    ok = self.verify(dest, checksum, checksum_algo)
                    if not ok:
                        self.log.error("Removing corrupt download.")
                        os.remove(dest)
                        return None

                return dest

            except requests.exceptions.ConnectionError as e:
                self.log.warning(f"Connection error: {e}")
                existing = os.path.getsize(tmp) if os.path.exists(tmp) else 0
            except requests.exceptions.HTTPError as e:
                self.log.error(f"HTTP error: {e}")
                break
            except KeyboardInterrupt:
                self.log.warning("Download paused. Run again to resume.")
                return None
            except Exception as e:
                self.log.error(f"Unexpected error: {e}")

            if attempt < self.MAX_RETRIES:
                self.log.info(f"Retrying in {self.RETRY_DELAY}s...")
                time.sleep(self.RETRY_DELAY)

        self.log.error(f"Download failed after {self.MAX_RETRIES} attempts.")
        return None

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _fmt_size(b: float) -> str:
        for u in ("B", "KB", "MB", "GB", "TB"):
            if b < 1024:
                return f"{b:.1f} {u}"
            b /= 1024
        return f"{b:.1f} PB"


def download_rom(url: str, log, dest_dir: str = DEFAULT_DEST,
                 checksum: str = None) -> Optional[str]:
    """Convenience wrapper used by flash.py and the CLI."""
    d = Downloader(log)
    return d.download(url, dest_dir=dest_dir, checksum=checksum)
