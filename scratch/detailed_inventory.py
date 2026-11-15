import os
import glob
import json
import re

ROOT = r"c:\Users\haris\OneDrive\Desktop\PROJECT_DATA"

def find(pattern):
    return [os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, pattern), recursive=True) if not os.path.isdir(p)]

print("=== API ROUTERS ===")
routers = find("backend/api/**/*.py")
for r in sorted(routers):
    print(" ", r)

print("\n=== BACKEND SERVICES ===")
services = find("backend/services/**/*.py")
for s in sorted(services):
    print(" ", s)

print("\n=== HAZARD MODULES ===")
hazards = find("backend/hazards/**/*.py")
for h in sorted(hazards):
    print(" ", h)

print("\n=== AGENTS ===")
agents = find("backend/agents/**/*.py")
for a in sorted(agents):
    print(" ", a)

print("\n=== MODELS DIRECTORY ===")
models = find("Models/**/*") + find("models/**/*")
for m in sorted(models):
    print(" ", m)

print("\n=== FRONTEND PAGES ===")
pages = find("frontend/src/pages/**/*")
for p in sorted(pages):
    print(" ", p)

print("\n=== FRONTEND COMPONENTS ===")
comp = find("frontend/src/components/**/*")
for c in sorted(comp):
    print(" ", c)

print("\n=== SCHEMAS ===")
schemas = find("schemas/**/*") + find("backend/schemas/**/*")
for sc in sorted(schemas):
    print(" ", sc)

