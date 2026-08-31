# Security & Role-Based Access Control (RBAC) — Review II

## 1. Overview
The security architecture enforces user authentication, password hashing, JSON Web Token (JWT) state management, and role-based permissions across system operations.

---

## 2. Roles & Permissions Matrix

| Capability | Anonymous / Public | `USER` Role (e.g. Harish) | `ADMIN` Role (e.g. System Admin) |
|---|---|---|---|
| View Public Root & API Docs | Allowed | Allowed | Allowed |
| User Login (`/auth/login`) | Allowed | Allowed | Allowed |
| Current User Info (`/auth/me`) | Restricted | Allowed | Allowed |
| View Districts & Profiles | Allowed | Allowed | Allowed |
| Location Search & Geocoding | Allowed | Allowed | Allowed |
| Fetch Weather Forecasts | Allowed | Allowed | Allowed |
| Run ML Hazard Predictions | Allowed | Allowed | Allowed |
| View System Health Status | Allowed | Allowed | Allowed |
| Purge Forecast Caches | Restricted | **Forbidden (403)** | **Allowed** |

---

## 3. Cryptographic Standards

- **Password Hashing**: Bcrypt with auto-adaptive salt rounds via `passlib.context.CryptContext`.
- **Token Signing**: HMAC-SHA256 (`HS256`) with secret key configured via environment variables (`JWT_SECRET_KEY`).
- **Token Expiration**: Configured to 24 hours with embedded `exp` and `iat` claims.
- **CORS Policy**: Configured to allow verified frontend origins with permissive preflight support for cross-origin development.
