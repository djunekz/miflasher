"""
MiFlasher Banner
"""

BANNER = r"""
                                                       
                                                       
       ██▄  ▄██ ▄▄ ██████ ▄▄     ▄▄▄   ▄▄▄▄ ▄▄ ▄▄ ▄▄▄▄▄ ▄▄▄▄  
       ██ ▀▀ ██ ██ ██▄▄   ██    ██▀██ ███▄▄ ██▄██ ██▄▄  ██▄█▄ 
       ██    ██ ██ ██     ██▄▄▄ ██▀██ ▄▄██▀ ██ ██ ██▄▄▄ ██ ██ 
                                                       
"""

VERSION_LINE = "  v2.0.0 | Advanced Xiaomi Flash & Unlock Toolkit | Termux Edition"
SEPARATOR    = "  " + "─" * 67


def print_banner():
    try:
        # Try colored output
        CYAN   = "\033[1;36m"
        YELLOW = "\033[1;33m"
        DIM    = "\033[2m"
        RESET  = "\033[0m"
        print(f"{YELLOW}{BANNER}{RESET}")
        print(f"{YELLOW}{VERSION_LINE}{RESET}")
        print(f"{DIM}{SEPARATOR}{RESET}")
        print()
    except Exception:
        print(BANNER)
        print(VERSION_LINE)
        print(SEPARATOR)
        print()
