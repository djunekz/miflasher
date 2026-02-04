from core.utils import run_cmd
from core.logger import log
import requests
import os

def download_rom(url, dest=None):
    if not dest:
        dest = "/sdcard/Download"
    os.makedirs(dest, exist_ok=True)
    filename = os.path.join(dest, url.split("/")[-1])
    log(f"Downloading ROM: {filename}")
    r = requests.get(url, stream=True)
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    log(f"Download completed: {filename}", level="success")
    return filename
