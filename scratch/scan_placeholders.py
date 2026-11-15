import re
import json

with open("scratch/survey_full_dump.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines in survey dump: {len(lines)}")

placeholders = []
bracket_pattern = re.compile(r'\[([^\]]+)\]')

for line_idx, line in enumerate(lines):
    # Check for brackets
    for match in bracket_pattern.finditer(line):
        text = match.group(1).strip()
        # If it's a numeric citation like [1] or [1]-[4], note it as citation, otherwise as placeholder candidate
        if not re.match(r'^\d+(\s*[-,\u2013]\s*\d+)*$', text):
            placeholders.append({
                "line_index": line_idx,
                "context": line.strip()[:150],
                "placeholder_text": match.group(0)
            })
            
    # Check for explicit keywords without brackets
    for kw in ["INSERT", "VERIFIED", "TBD", "TODO", "NOT_VERIFIED", "NOT VERIFIED", "ACTUAL"]:
        if kw in line and not any(p["context"] == line.strip()[:150] for p in placeholders):
            placeholders.append({
                "line_index": line_idx,
                "context": line.strip()[:150],
                "placeholder_text": line.strip()
            })

print(f"Total Placeholders / Target Annotations Found: {len(placeholders)}")

out_path = "scratch/placeholders_found.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(placeholders, f, indent=2)

print(f"Saved placeholders to {out_path}")
for idx, p in enumerate(placeholders, 1):
    print(f"{idx}. [{p['line_index']}] {p['placeholder_text']} --> {p['context'][:100]}")
