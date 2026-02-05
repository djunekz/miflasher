import subprocess
from core.logger import log
import sys
import time

def run_cmd(cmd, desc=None):
    if desc: print(f"-> {desc}")
    import subprocess
    subprocess.run(cmd, shell=True, check=True)
    if desc: print(f"-> {desc} OK")
def progress_bar(iterable, prefix="", size=30, file=sys.stdout):
    total=len(iterable)
    def show(j):
        x=int(size*j/total)
        file.write("%s[%s%s] %i/%i\r"%(prefix,"#"*x,"."*(size-x),j,total))
        file.flush()
    for i,item in enumerate(iterable):
        yield item
        show(i+1)
    file.write("\n")
