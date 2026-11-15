import zipfile
import re
import json
import xml.etree.ElementTree as ET

DOCX_PATH = r"C:\Users\haris\Downloads\Quantum_Assisted_Climate_Adaptation_Survey.docx"

def extract_paragraphs_and_tables(docx_path):
    with zipfile.ZipFile(docx_path, 'r') as zip_ref:
        xml_content = zip_ref.read('word/document.xml')
        tree = ET.fromstring(xml_content)
        
        paragraphs = []
        for p in tree.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            p_text = ''.join([t.text for t in p.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text])
            if p_text.strip():
                paragraphs.append(p_text.strip())
                
        table_cells = []
        for cell in tree.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tc'):
            c_text = ''.join([t.text for t in cell.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text])
            if c_text.strip():
                table_cells.append(c_text.strip())
                
        return paragraphs, table_cells

paragraphs, table_cells = extract_paragraphs_and_tables(DOCX_PATH)
full_text = "\n".join(paragraphs + table_cells)

print(f"Total Paragraphs: {len(paragraphs)}")
print(f"Total Table Cells: {len(table_cells)}")

# Print bracketed items
brackets = re.findall(r'\[[^\]\n]{2,100}\]', full_text)
print("\n--- ALL BRACKET MATCHES ---")
for b in sorted(set(brackets)):
    print(f"  {b}")

# Print lines with target placeholder words
target_words = ["INSERT", "VERIFIED", "VALUE", "ACTUAL", "EXACT", "VERSION", "DATABASES", "SEARCH", "SCREENING", "RECORDS"]
print("\n--- LINES WITH PLACEHOLDER KEYWORDS ---")
for line in paragraphs + table_cells:
    if any(w in line for w in target_words):
        print(f"  > {line[:120]}")
