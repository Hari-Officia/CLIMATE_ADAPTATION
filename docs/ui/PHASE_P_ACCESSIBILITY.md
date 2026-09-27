# Phase P Accessibility (WCAG 2.2 AA) Specification

**Project:** Quantum Multi-Agent Climate Adaptation Decision Support System  

---

## 1. Non-GIS Table / List Alternative

Because spatial maps can present accessibility barriers for screen-reader users or keyboard-only navigation:
- Every district risk layer, priority summary, and strategy matrix includes an accessible **Table / List View Toggle**.
- Screen readers can consume all 38 district names, risk scores, priority horizons, and selected strategies in structured semantic HTML tables (`<table>`, `<th>`, `<td>`, `<caption>`).

---

## 2. ARIA Labels & Focus Management

- **Interactive Elements:** Every map marker, button, tab, and search dropdown includes unique `id`, `aria-label`, `aria-expanded`, and `role` attributes.
- **Focus Rings:** Visible focus outlines (`focus:ring-2 focus:ring-emerald-400`) applied to all interactive controls.
- **Keyboard Traversal:** Users can navigate from Header -> District Selector -> Map Control -> Data Tabs -> Decision Export completely using `Tab`, `Arrow` keys, `Enter`, and `Escape`.

---

## 3. High Contrast & Text Sizing

- **Contrast Ratios:** Text against background satisfies minimum 4.5:1 ratio (e.g. `text-slate-100` on `bg-slate-950`).
- **Status Badges:** Text badges supplement color indicators (`HIGH RISK`, `MEDIUM RISK`, `LOW RISK`, `UNAVAILABLE`).
