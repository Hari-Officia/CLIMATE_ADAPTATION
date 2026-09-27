# District Data Catalog Summary

## 🗺️ Overview
The **District Data Catalog** establishes the unified geographical, climatological, and demographic baseline for all **38 administrative districts** of Tamil Nadu. It powers feature engineering, geospatial maps, and benchmark verification across classical and quantum solvers.

---

## 📌 District Typology & Classification

| Categorization | Number of Districts | Key Characteristics & Example Districts | Primary Hazards |
|---|---|---|---|
| **Coastal Districts** | 14 | Low elevation, high storm surge vulnerability (e.g. Chennai, Nagapattinam, Cuddalore, Ramanathapuram, Kanniyakumari) | Cyclone, Sea Surge, Flood |
| **Inland Agricultural** | 18 | Delta and river basin farming hubs (e.g. Thanjavur, Tiruvarur, Madurai, Tiruchirappalli, Ariyalur) | Flood, Drought |
| **Hilly / Western Ghats** | 6 | High elevation, steep terrain (e.g. Nilgiris, Dindigul, Theni, Tenkasi) | Landslide, Flash Flood |

---

## 📊 Complete List of 38 Tamil Nadu Districts

```
1. Ariyalur          11. Kanniyakumari   21. Ramanathapuram   31. Tirupathur
2. Chengalpattu      12. Karur           22. Ranipet          32. Tiruppur
3. Chennai           13. Krishnagiri     23. Salem            33. Tiruvallur
4. Coimbatore        14. Madurai         24. Sivaganga        34. Tiruvannamalai
5. Cuddalore         15. Mayiladuthurai  25. Tenkasi          35. Tiruvarur
6. Dharmapuri        16. Nagapattinam    26. Thanjavur        36. Vellore
7. Dindigul          17. Namakkal        27. Theni            37. Viluppuram
8. Erode             18. Nilgiris        28. Thoothukudi      38. Virudhunagar
9. Kallakurichi      19. Perambalur      29. Tiruchirappalli
10. Kancheepuram     20. Pudukkottai     30. Tirunelveli
```

---

## 📑 Verification Benchmarks CSV Files

The system maintains validated CSV benchmark datasets for cross-layer verification:
* `38_DISTRICT_FRONTEND_VERIFICATION.csv`: Frontend API payload sanity check.
* `38_DISTRICT_QUANTUM_RESEARCH_GATE.csv`: Quantum feasibility & scale vs gap metrics.
* `EXACT_MILP_QUBO_EQUIVALENCE.csv`: Mathematical zero-gap equivalence proof between classical MILP and QUBO.

---

## 💻 Minimal Code Example

```python
# backend/db/district_loader.py
import json
import pandas as pd
from typing import Dict, Any, List

def load_district_catalog(climatology_json_path: str) -> Dict[str, Any]:
    """Loads district climatology baseline dictionary."""
    with open(climatology_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    districts = list(data.keys())
    return {
        "total_districts": len(districts),
        "district_names": sorted(districts),
        "sample_baseline": data[districts[0]] if districts else {}
    }

def verify_district_csv_benchmark(csv_path: str) -> pd.DataFrame:
    """Loads and validates district verification benchmark CSV."""
    df = pd.read_csv(csv_path)
    assert len(df) == 38, f"Expected 38 district rows, got {len(df)}"
    return df
```
