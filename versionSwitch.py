import argparse
import os
import re
from pathlib import Path
import shutil

# python versionSwitch.py "en_translate_0.97.13/myEN" "en_translate_0.97.13/translateFrom" "014en"

pattern = r'"([^"\n]+)"'

parser = argparse.ArgumentParser()
parser.add_argument("translated_filename")
parser.add_argument("origin_filename")
parser.add_argument("to_translate_filename")

args = parser.parse_args()

# Read origin version and translated version
with open(f"./{str(args.origin_filename)}.txt", "r", encoding="utf-8") as f:
    origin_lines = f.read().splitlines()
with open(f"./{str(args.translated_filename)}.txt", "r", encoding="utf-8") as f:
    translated_lines = f.read().splitlines()
with open(f"./{str(args.to_translate_filename)}.txt", "r", encoding="utf-8") as f:
    to_translate_lines = f.read().splitlines()

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

def make_repl(factor: dict):
    def repl(match: re.Match) -> str:
        if match.group(0) in factor:
            return str(factor[match.group(0)])
        else:
            print("Not found: " + match.group(0))
            return match.group(0)
    return repl

counter = 0
new_lines = []
for line in to_translate_lines:
    currentLine = line.strip()
    if re.search(pattern, currentLine):
        translated = re.sub(pattern, make_repl(translate_dic), currentLine)
        counter += 1
    else:
        translated = currentLine
    new_lines.append(translated)

print(counter)
with open(f"./{str(args.to_translate_filename)}.txt", "w", encoding="utf-8") as f:
    for line in new_lines:
        f.write(line + "\n")
