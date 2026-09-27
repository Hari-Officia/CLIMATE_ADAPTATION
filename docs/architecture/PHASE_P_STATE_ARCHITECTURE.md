# Phase P State Management & Race-Condition Architecture

**Project:** Quantum Multi-Agent Decision Support System for Climate Adaptation  

---

## 1. State Segregation Model

| State Type | Scope | Manager / Storage | Purpose |
| :--- | :--- | :--- | :--- |
| **Server State** | Async Data | Axios API Clients + Local React Hooks | Fetched decision payload, risk matrices, evidence documents |
| **UI State** | Component | React `useState` & `useMemo` | Active tab, layer visibility, popup state, opacity sliders |
| **Session State**| Global App | `AuthContext.jsx` | User authentication token, role permissions, active session |
| **URL Query State**| Browser | React Router `useSearchParams` / Params | Deep links (`/district/TN-001/risk?hazard=FLOOD`) |

---

## 2. Request Cancellation & Race Condition Guard

To prevent out-of-order API responses when rapidly switching between districts (e.g. Chennai -> Madurai -> Coimbatore):
1. **Axios CancelToken / AbortController:** Every API request includes an active `AbortController` signal.
2. **District Request Keying:** Each incoming API response is validated against the currently active `selectedDistrictId`. If the response district ID does not match the active state key, the payload is discarded silently.
3. **Cross-District Data Isolation:** When switching districts, previous district state vectors (risk, priority, strategies, evidence) are reset to `null` before triggering new requests.
