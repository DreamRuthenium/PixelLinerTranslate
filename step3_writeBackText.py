import os
import re
import csv
from pathlib import Path
import shutil
import argparse
import stat

# python step3_writeBackText.py 014en

pattern = r'"([^"\n]+)"'
pattern_jp = r'"[^"\n]*[\u3040-\u30FF\u4E00-\u9FFF][^"\n]*"'

parser = argparse.ArgumentParser(description="Extract all JP lines")
parser.add_argument("filename", nargs="?", help="The filename for you translate file(without extension)", default="ch")
args = parser.parse_args()



# Copy original version into output path
src_path = Path("./air/pxl-0/")
dst_path = Path("./translated/pxl-0/")

if not src_path.exists() or not src_path.is_dir():
    raise ValueError(f"Unable to find source : {src_path}")

# Extracted files may contain readonly, which is hard to remove
def force_remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

# remove files from last time
if os.path.exists(dst_path):
    shutil.rmtree(dst_path, onerror=force_remove_readonly)



print(f"Copying swf files from {src_path} to {dst_path}")
shutil.copytree(src_path, dst_path, dirs_exist_ok=True)

# Read origin version and translated version
with open("./air/doNotModify/translateFrom.txt", "r", encoding="utf-8") as f:
    origin_lines = f.read().splitlines()
with open(f"./{str(args.filename)}.txt", "r", encoding="utf-8") as f:
    translated_lines = f.read().splitlines()

# Create a dictory for searching
from_num = []
from_text = []
to_num = []
to_text = []
for line in origin_lines:
    m = re.search(pattern, line)
    if m and (line[0:6] != "XXXXXX"):
        from_text.append(m.group())
        from_num.append(int(line[0:6]))

for line in translated_lines:
    m = re.search(pattern, line)
    if m and (line[0:6] != "XXXXXX"):
        to_text.append(m.group())
        to_num.append(int(line[0:6]))

print(len(from_num), len(from_text), len(to_num), len(to_text))

to_map = dict(zip(to_num, to_text))
translate_dic = {
    temp_text: to_map[num]
    for num, temp_text in zip(from_num, from_text)
    if num in to_map
}

print(f"Translating swf files...")
# Get a file list of swf folder
files = []
w = os.walk(dst_path)
for (dirpath, dirnames, filenames) in w:
    for f in filenames:
        files.append(os.path.join(dirpath, f))

def make_repl(factor: dict):
    def repl(match: re.Match) -> str:
        print(match.group(0))
        return str(factor[match.group(0)])
    return repl

counter = 0
for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        try:
            lines = f.readlines()
        except:
            continue
        new_lines = []
        for line in lines:
            currentLine = line.strip()
            if re.search(pattern_jp, currentLine):
                print(currentLine)
                translated = re.sub(pattern_jp, make_repl(translate_dic), currentLine)
                counter += 1
            else:
                translated = currentLine
            new_lines.append(translated + '\n')
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
print(counter)
