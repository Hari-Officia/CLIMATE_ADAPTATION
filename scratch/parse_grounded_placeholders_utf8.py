import re
import json

with open("scratch/grounded_survey_dump.txt", "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines() if l.strip()]

keywords = [
    "INSERT", "VERIFIED", "VALUE", "ACTUAL", "EXACT", "VERSION",
    "TBD", "TODO", "NOT_VERIFIED", "DATABASES", "SEARCH PERIOD", "SEARCH TERMS",
    "SCREENING COUNTS", "SEEDS", "HASH"
]

found = []
for idx, line in enumerate(lines):
    bracket_matches = re.findall(r'\[([^\]]+)\]', line)
    has_placeholder_bracket = False
    for bm in bracket_matches:
        if not re.match(r'^\d+(\s*[-,\u2013\u2014]\s*\d+)*$', bm.strip()):
            has_placeholder_bracket = True
            break
            
    has_keyword = any(kw in line for kw in keywords)
    
    if has_placeholder_bracket or has_keyword:
        found.append({
            "index": idx,
            "line_text": line,
            "bracket_matches": [bm for bm in bracket_matches if not re.match(r'^\d+(\s*[-,\u2013\u2014]\s*\d+)*$', bm.strip())]
        })

print(f"Total Placeholder Lines: {len(found)}")

with open("scratch/grounded_placeholders_extracted.txt", "w", encoding="utf-8") as out:
    out.write(f"TOTAL PLACEHOLDER LINES: {len(found)}\n\n")
    for idx, item in enumerate(found, 1):
        out.write(f"--- ITEM {idx} (Line {item['index']}) ---\n")
        out.write(f"TEXT: {item['line_text']}\n")
        out.write(f"PLACEHOLDERS: {item['bracket_matches']}\n\n")

print("Saved to scratch/grounded_placeholders_extracted.txt")
