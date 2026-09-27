# PostgreSQL & PostGIS Schema Summary

## 🗄️ Overview
The **PostgreSQL Subsystem** provides persistent relational and spatial storage for the platform. Using **PostGIS** spatial extensions and **SQLAlchemy ORM**, it manages district geographic records, historical hazard observations, adaptation strategy catalogs, and audit logs of quantum QUBO executions.

---

## 📐 Database Schema & Entity Relationship

```
+------------------+         +-------------------+         +------------------------+
|    districts     |         |   hazard_records  |         | adaptation_strategies  |
+------------------+         +-------------------+         +------------------------+
| PK district_id   |<-------+| PK id             |         | PK strategy_id         |
|    district_name | 1     N | FK district_id    |         |    strategy_name       |
|    latitude      |         |    hazard_type    |         |    sector              |
|    longitude     |         |    probability    |         |    cost_inr_lakhs      |
|    svi_score     |         |    recorded_at    |         |    risk_reduction_pct  |
+--------+---------+         +-------------------+         +-----------+------------+
         |                                                             |
         | 1                                                           |
         |                                                             | N
         v N                                                           v
+------------------+                                       +------------------------+
| qubo_model_recs  |                                       | portfolio_executions   |
+------------------+                                       +------------------------+
| PK qubo_id       |                                       | PK execution_id        |
| FK district_id   |                                       | FK district_id         |
|    model_hash    |                                       |    solver_type         |
|    linear_terms  |                                       |    selected_strategies |
|    quad_terms    |                                       |    objective_value     |
+------------------+                                       +------------------------+
```

---

## 📋 Table Descriptions

| Table Name | Description | Key Indexes / Constraints |
|---|---|---|
| `districts` | Catalog of 38 Tamil Nadu districts, population, centroid coordinates, and vulnerability scores | Primary Key (`district_id`) |
| `hazard_records` | Time-series of predicted and historical hazard instances per district | Index on (`district_id`, `recorded_at`) |
| `adaptation_strategies` | Library of resilience interventions with cost, sector, and efficiency bounds | Primary Key (`strategy_id`) |
| `portfolio_executions` | Execution log comparing Classical MILP vs Quantum QAOA solver outcomes | Foreign Keys to `districts` |
| `qubo_models` | Serialized QUBO matrices, variable mappings, SHA-256 hashes, and penalty values | Unique index on (`model_hash`) |

---

## 💻 Minimal Code Example

```python
# backend/db/models.py
from sqlalchemy import Column, String, Float, Integer, JSON, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class District(Base):
    __tablename__ = "districts"

    district_id = Column(String(50), primary_key=True)
    district_name = Column(String(100), nullable=False, unique=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    population = Column(Integer, nullable=True)
    is_coastal = Column(Boolean, default=False)
    svi_score = Column(Float, default=0.5)

class PortfolioExecutionRecord(Base):
    __tablename__ = "portfolio_executions"

    execution_id = Column(String(64), primary_key=True)
    district_id = Column(String(50), ForeignKey("districts.district_id"), nullable=False)
    solver_type = Column(String(20), nullable=False) # "MILP" or "QAOA"
    budget_limit = Column(Float, nullable=False)
    selected_strategies = Column(JSON, nullable=False) # List of strategy_ids
    objective_value = Column(Float, nullable=False)
    execution_time_ms = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```
