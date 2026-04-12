import argparse
import os
import re
from pathlib import Path

pattern = r'"[^"\n]*[\u3040-\u30FF\u4E00-\u9FFF][^"\n]*"'

parser = argparse.ArgumentParser(description="Extract all JP lines")
parser.add_argument("filename", help="The filename for you translate file(without extension)")
args = parser.parse_args()

# Get a file list of swf folder
files = []
w = os.walk(r"./air/pxl-0")
for (dirpath, dirnames, filenames) in w:
    for f in filenames:
        files.append(os.path.join(dirpath, f))

if len(files) == 0:
    raise ValueError(f"Unable to find any files in ./air/pxl-0. Have you run step1 ?")
else:
    print(f"{len(files)} files found.")

# Gather all texts which include JP characters
msg1 = r"For translators:"
msg2 = r""
msg3 = (r"Due to technical reasons(I can only get reverse machine code instead of source code), " +
        r"current version can not show parameters or variables in a full sentence.")
msg4 = r"Therefore, sentences with variables in the middle will be split out. I am sorry for the trouble."
msg5 = r""
msg6 = "Also, please only modify contents inside quote(\"), NEVER modify numbers at start of each line."
msg7 = r"NEVER add or remove quote itself."
msg8 = r""
msg9 = r"About indexes: index = actual number means this str is unique. index = XXXXXX means it has appeared before."
msg10 = r"You do not need to translate them, and can safely delete them if needed. They are for better understanding of overall sentence."
msg11 = ""

rows = []

for filename in files:
    try:
        with open(filename, 'r', encoding='utf-8') as handle:
            for i, line in enumerate(handle):
                try:
                    currentLine = line.strip()
                    if re.search(pattern, currentLine):
                        for m in re.finditer(pattern, currentLine):
                            sentence = m.group()
                            rows.append(sentence)
                        # print()
                except Exception as e:
                    print("Unable to read line "+ str(i) + "in " + filename)
                    print(e)
    except Exception as e2:
        # These are probably sprites or other shits, no need to worry
        pass

not_showed = list(set(rows))
line_num = len(not_showed)
result = []
index = 0
for i, text in enumerate(rows):
    if text in not_showed:
        result.append(str(index).zfill(6) + "    " + rows[i])
        index += 1
        not_showed.remove(text)
    else:
        result.append("XXXXXX" + "    " + rows[i])

result = [msg1,msg2,msg3,msg4,msg5,msg6,msg7,msg8, msg9, msg10, msg11] + result
print(len(not_showed))
if len(files) <= 100:
    raise ValueError(f"Unable to find any lines. This is not an expected error.")
else:
    print(f"{str(line_num)} lines extracted.")

# Hide origin indexes in air file in case somebody modify it
origin_path = Path("./air/doNotModify/")
origin_path.mkdir(parents=True, exist_ok=True)
with open("./air/doNotModify/translateFrom.txt", "w", encoding="utf-8") as f:
    for line in result:
        f.write(line + "\n")

with open(f"./{str(args.filename)}.txt", "w", encoding="utf-8") as f:
    for line in result:
        f.write(line + "\n")

print(f"File for translate: ./{str(args.filename)}.txt. Exiting...")