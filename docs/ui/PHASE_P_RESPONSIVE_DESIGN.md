# Phase P Responsive Layout Specification

**Project:** Quantum Multi-Agent Climate Adaptation Decision Support System  

---

## 1. Breakpoint & Grid Layouts

- **Desktop (`lg`: 1024px+):** Dual-pane interface with persistent collapsable sidebar, central GIS map view / multi-tab analytical detail view, and right-side decision summary drawer.
- **Tablet (`md`: 768px - 1023px):** Stacked map container above analytical tabs with collapsible filter controls.
- **Mobile (`sm`: <768px):** Single-column layout with bottom sheet drawer for district profile details, full-width touch-friendly district dropdown, and responsive table scrolling.

---

## 2. Dynamic Component Behavior

- **Map Controls:** Layers panel collapses into a floating action button (FAB) on small screens.
- **Data Tables:** Horizontal scrolling wrapper with sticky strategy name column.
- **Charts (Recharts):** Wrapped in `ResponsiveContainer` to maintain 100% width fluid scaling.
