# Phase P Design System & Semantic Color Token Specification

**Project:** Quantum Multi-Agent Climate Adaptation Decision Support System  

---

## 1. Color Palette Tokens (Tailwind CSS Base)

- **Background Base:** `bg-slate-950` (#020617) - Deep dark mode enterprise standard.
- **Surface Elevation 1:** `bg-slate-900` (#0f172a) - Navigation sidebars & header bars.
- **Surface Elevation 2:** `bg-slate-800/80` - Dynamic analytical cards with glassmorphism backdrop blur.
- **Primary Accent:** `emerald-500` (#10b981) - Climate resilience, optimal portfolios, validated statuses.
- **Secondary Accent:** `cyan-500` (#06b6d4) - Quantum QAOA benchmarking & optimization metrics.
- **Warning / Review:** `amber-500` (#f59e0b) - Review-required strategies, conditional applicability, degraded backend mode.
- **Hazard Risk High / Critical:** `rose-500` (#f43f5e) - High risk, high hazard vulnerability.
- **Data Unavailable:** `slate-600` (#475569) - Grayed-out badge explicitly labelled `DATA UNAVAILABLE`.

---

## 2. Risk & Priority Semantic Governance

- **Color Alone Rule:** No risk or priority level is communicated purely by color. Every status indicator must feature explicit text, an icon, or ARIA label.
- **Distinct Terminology Rule:**
  - `HAZARD RISK` (Flood, Drought, Heatwave)
  - `ADAPTATION PRIORITY` (Immediate, Short-Term, Medium-Term, Long-Term)
  - `VULNERABILITY LEVEL` (High, Medium, Low)
  - Never conflate "Risk" with "Priority".

---

## 3. Typography & Micro-Animations

- **Font Family:** Inter / System Sans-Serif (`font-sans`).
- **Monospace Code/Data:** Fira Code / JetBrains Mono (`font-mono`) for variable IDs, SHA256 hashes, and bitstrings.
- **Transitions:** `transition-all duration-200 ease-in-out` for hover states and district selection transitions.
