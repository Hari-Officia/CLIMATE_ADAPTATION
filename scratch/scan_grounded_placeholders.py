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
    # Check for [TEXT] where TEXT is not purely numeric or ranges like [1], [1]-[4], [1, 2]
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
            "has_bracket": has_placeholder_bracket,
            "has_keyword": has_keyword
        })

print(f"Total Placeholder / Value Annotation Lines Found: {len(found)}")
for item in found:
    print(f"L{item['index']:03d}: {item['line_text']}")

out_json = "scratch/grounded_placeholders.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(found, f, indent=2, ensure_ascii=False)
