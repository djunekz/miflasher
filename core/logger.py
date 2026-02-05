import sys

def log(msg, level="info"):
    colors = {"info":"\033[1;34m", "success":"\033[1;32m", "error":"\033[1;31m"}
    reset="\033[0m"
    print(f"{colors.get(level,'')}{level.upper()}: {msg}{reset}")
