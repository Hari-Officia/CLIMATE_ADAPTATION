import re
import json

with open("scratch/literature_27A28.txt", "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines() if l.strip()]

entries = []
curr_num = None
curr_lines = []

for line in lines:
    m = re.match(r'^(\d+)\.$', line)
    if m:
        if curr_num is not None:
            entries.append((curr_num, curr_lines))
        curr_num = int(m.group(1))
        curr_lines = []
    elif curr_num is not None:
        curr_lines.append(line)

if curr_num is not None:
    entries.append((curr_num, curr_lines))

parsed_data = []
for num, elines in entries:
    parsed_data.append({
        "entry_number": num,
        "citation_line": elines[0] if len(elines) > 0 else "",
        "focus": elines[1] if len(elines) > 1 else "",
        "findings": elines[2] if len(elines) > 2 else "",
        "future_work": elines[3] if len(elines) > 3 else "",
        "all_raw_lines": elines
    })

with open("scratch/literature_20_parsed.json", "w", encoding="utf-8") as f:
    json.dump(parsed_data, f, indent=2, ensure_ascii=False)

print(f"Successfully parsed {len(parsed_data)} literature entries into scratch/literature_20_parsed.json")
