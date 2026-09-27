import os
import re
import json

PATTERNS = {
    "AWS_KEY": r"(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}",
    "GENERIC_SECRET": r"(?i)(api_key|secret_key|auth_token|bearer)\s*[:=]\s*['\"](?![^'\"]*example)[^'\"]{16,}['\"]",
    "PRIVATE_KEY": r"-----BEGIN (?:RSA |EC |PGP )?PRIVATE KEY-----"
}

IGNORE_DIRS = {".git", ".pytest_cache", "node_modules", "dist", "venv", "__pycache__"}

def scan_repository():
    findings = []
    for root, dirs, files in os.walk(os.getcwd()):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            if file.endswith((".py", ".js", ".jsx", ".json", ".yml", ".yaml", ".env")):
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, os.getcwd())
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        for p_name, regex in PATTERNS.items():
                            matches = re.finditer(regex, content)
                            for m in matches:
                                findings.append({
                                    "file": rel_path,
                                    "pattern": p_name,
                                    "match_snippet": m.group(0)[:20] + "..."
                                })
                except Exception as e:
                    pass
    return findings

if __name__ == "__main__":
    findings = scan_repository()
    print(f"Secret Scanner Completed: Found {len(findings)} potential hardcoded secrets.")
    with open("AUDIT/PHASE_Q/secret_scan_results.json", "w") as f:
        json.dump(findings, f, indent=2)
