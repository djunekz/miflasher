import requests, os
from core.logger import log
from core.utils import progress_bar

def download_rom(url, dest="/sdcard/Download"):
    os.makedirs(dest, exist_ok=True)
    filename = os.path.join(dest, url.split("/")[-1])
    log(f"Downloading ROM from {url}")
    r = requests.get(url, stream=True)
    total_length = int(r.headers.get('content-length', 0))
    with open(filename, 'wb') as f:
        for chunk in progress_bar(r.iter_content(chunk_size=8192), prefix="Downloading:"):
            if chunk:
                f.write(chunk)
    log(f"Downloaded to {filename}", level="success")
    return filename
