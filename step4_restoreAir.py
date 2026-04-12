import zipfile
from pathlib import Path
import shutil
import subprocess
import os

# Search and extract air file
air_path = r"./translated"
root = Path(air_path)

# Copy swf file
origin_swf = Path(r"./air/pxl.swf")
dst_swf = Path(r"./translated/pxl.swf")
shutil.copy(origin_swf, dst_swf)

# Check if extract went well
core_file = Path("./translated/pxl-0/pxl-0.main.asasm")
if not core_file.exists():
    raise ValueError(f"Something wrong when trying to extract air file! Have you run step 3?")
else:
    print("Trying to rebuild...")


# Call outside program(RABCDAsm) to crack swf into asasm files
result = subprocess.run(
    [r"./RABCDAsm_v1.18/rabcasm", "pxl-0/pxl-0.main.asasm"],
    cwd=air_path
)

if result.returncode != 0:
    raise ValueError(f"Rebuild abc file failed! This is not an usual error.")
else:
    print("Rebuild abc file success.")

# Call outside program(RABCDAsm) to crack abc file
result = subprocess.run(
    [r"./RABCDAsm_v1.18/abcreplace",
     "./pxl.swf", "0", "pxl-0/pxl-0.main.abc"],
    cwd=air_path
)

if result.returncode != 0:
    raise ValueError(f"Rebuild swf file failed! This is not an usual error.")
else:    print("Rebuild swf success. Exiting...")

build_swf = Path(r"./translated/src/pxl.swf")
shutil.copy(dst_swf, build_swf)
