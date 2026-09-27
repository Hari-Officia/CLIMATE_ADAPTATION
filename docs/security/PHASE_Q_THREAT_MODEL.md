# Phase Q Security Threat Model & Hardening Architecture

**Project:** Quantum Multi-Agent Climate Adaptation Decision Support System  

---

## 1. Threat Matrix & Defense Mechanisms

| Vulnerability Vector | Threat Scenario | Mitigation Strategy | Status |
| :--- | :--- | :--- | :--- |
| **SQL Injection** | Malicious input in district parameters | SQLAlchemy parameterized ORM queries | **VERIFIED** |
| **XSS / DOM Injection**| Unsanitized Markdown/LLM output | Client-side HTML entity escaping & DOM sanitization | **VERIFIED** |
| **Prompt Injection** | Adversarial text in retrieved RAG PDFs | Hierarchy enforcement (retrieved text treated strictly as DATA) | **VERIFIED** |
| **Secret Leakage** | API keys committed to repository | Pydantic BaseSettings + `scripts/scan_secrets.py` scanner | **VERIFIED** |
| **API Denial of Service**| Rapid request overloading | FastAPI rate-limiting middleware & request body size limits | **VERIFIED** |

---

## 2. Token Redaction Middleware

All application logs pass through `backend/utils/security.py` log filter which automatically redacts `Authorization`, `Bearer`, `password`, and `SECRET_KEY` string patterns.
