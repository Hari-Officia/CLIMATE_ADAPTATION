import os
import glob
import json
import re

ROOT = r"c:\Users\haris\OneDrive\Desktop\PROJECT_DATA"

def find_files(pattern):
    return glob.glob(os.path.join(ROOT, pattern), recursive=True)

print("--- DEEP AUDIT SEARCH ---")

# 1. Models & ML Loaders
models = find_files("models/**/*") + find_files("Models/**/*") + find_files("backend/models/**/*")
print("ML Model files:", models)

# 2. Risk Engine & Hazards
hazards = find_files("backend/hazards/**/*") + find_files("backend/risk/**/*")
print("Hazard/Risk files:", hazards)

# 3. Agents
agents = find_files("backend/agents/**/*")
print("Agent files:", agents)

# 4. Optimization (MILP, QUBO, QAOA)
opt = find_files("backend/services/optimization/**/*")
print("Optimization files:", opt)

# 5. GIS API & Services
gis = find_files("backend/api/gis.py") + find_files("backend/services/spatial_service.py")
print("GIS files:", gis)

# 6. Database models & DB init
db = find_files("backend/db/**/*") + find_files("database/**/*")
print("Database files:", db)

# 7. Frontend Pages & Components
fe_pages = find_files("frontend/src/pages/**/*")
fe_comp = find_files("frontend/src/components/**/*")
fe_services = find_files("frontend/src/services/**/*")
print("Frontend pages count:", len(fe_pages))
print("Frontend components count:", len(fe_comp))
print("Frontend services:", fe_services)

# 8. RAG & LLM
rag = find_files("backend/api/rag.py") + find_files("backend/services/rag_service.py") + find_files("backend/services/llm_service.py") + find_files("backend/api/explanation.py")
print("RAG / LLM files:", rag)

