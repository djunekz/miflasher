from core.utils import run_cmd, progress_bar
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
    total_length = r.headers.get('content-length')

    with open(filename, 'wb') as f:
        if total_length is None:
            f.write(r.content)
        else:
            for chunk in progress_bar(r.iter_content(chunk_size=8192), prefix="Downloading:"):
                if chunk:
                    f.write(chunk)
    log(f"Download completed: {filename}", level="success")
    return filename
