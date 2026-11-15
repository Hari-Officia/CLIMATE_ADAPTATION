import re

content = open('backend/db/models.py', encoding='utf-8').read()
matches = re.findall(r'class\s+(\w+)\(.*?\):[\s\S]*?__tablename__\s*=\s*["\'](\w+)["\']', content)
print("Found SQLAlchemy Models & Tables:")
for cls_name, tbl_name in matches:
    print(f"  Class: {cls_name:<25} -> Table: {tbl_name}")
