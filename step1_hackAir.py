import zipfile
from pathlib import Path
import subprocess
import os
import shutil
import stat

# Search and extract air file
air_path = r"./air"
root = Path(air_path)
for path in root.iterdir():
    if path.is_file() and str(path).endswith("air"):
        with zipfile.ZipFile(path, "r") as z:
            z.extract('pxl.swf', './air')
            break

# Check if extract went well
swf_path = Path(r"./air/pxl.swf")
if not swf_path.exists():
    raise ValueError(f"Something wrong when trying to extract air file! Have you put it into air folder?")
else:
    print("Extracting air success.")

# Extracted files may contain readonly, which is hard to remove
def force_remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

# remove files from last time
pxl0_path = Path(r"./air/pxl-0")
pxlabc_path = Path(r"./air/pxl-0.abc")
if os.path.exists(pxl0_path):
    shutil.rmtree(pxl0_path, onerror=force_remove_readonly)
if os.path.exists(pxlabc_path):
    os.remove(pxlabc_path)

# Call outside program(RABCDAsm) to crack swf into asasm files
result = subprocess.run(
    [r"./RABCDAsm/abcexport", "pxl.swf"],
    cwd=air_path
)

if result.returncode != 0:
    raise ValueError(f"Cracking air file failed! This is not an usual error.")
else:
    print("Crack air file success.")

# Call outside program(RABCDAsm) to crack abc file
result = subprocess.run(
    [r"./RABCDAsm/rabcdasm", "pxl-0.abc"],
    cwd=air_path
)

if result.returncode != 0:
    raise ValueError(f"Cracking abc file failed! This is not an usual error.")
else:
    print("Crack abc file success. Exiting...")