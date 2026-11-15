import zipfile
import re
import json
import xml.etree.ElementTree as ET

DOCX_PATH = r"C:\Users\haris\Downloads\Quantum_Assisted_Climate_Adaptation_Survey.docx"

def extract_all(docx_path):
    with zipfile.ZipFile(docx_path, 'r') as zip_ref:
        xml_content = zip_ref.read('word/document.xml')
        tree = ET.fromstring(xml_content)
        
        elements = []
        for elem in tree.iter():
            if elem.tag.endswith('p'):
                p_text = ''.join([t.text for t in elem.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text])
                if p_text.strip():
                    elements.append(('PARAGRAPH', p_text.strip()))
            elif elem.tag.endswith('tbl'):
                # Process table
                rows = []
                for row in elem.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tr'):
                    cells = []
                    for cell in row.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tc'):
                        c_text = ''.join([t.text for t in cell.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text])
                        cells.append(c_text.strip())
                    if any(cells):
                        rows.append(cells)
                if rows:
                    elements.append(('TABLE', rows))
        return elements

elements = extract_all(DOCX_PATH)

out_lines = []
for idx, (kind, content) in enumerate(elements):
    if kind == 'PARAGRAPH':
        out_lines.append(f"P{idx}: {content}")
    elif kind == 'TABLE':
        out_lines.append(f"TABLE{idx}:")
        for row in content:
            out_lines.append("  | " + " | ".join(row) + " |")

with open("scratch/survey_full_dump.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))

print(f"Dumped {len(out_lines)} elements to scratch/survey_full_dump.txt")
