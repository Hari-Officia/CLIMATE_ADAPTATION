from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="USER", nullable=False)  # 'USER' or 'ADMIN'
    full_name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class District(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(String(50), unique=True, index=True, nullable=False) # e.g. "chennai"
    district_name = Column(String(100), unique=True, nullable=False)         # e.g. "Chennai"
    district_code = Column(String(20), nullable=True)                         # e.g. "IND-TN-CHE"
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    geojson_properties = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    profile = relationship("DistrictProfile", back_populates="district", uselist=False)
    forecasts = relationship("ForecastData", back_populates="district")
    risks = relationship("RiskResult", back_populates="district")

class DistrictProfile(Base):
    __tablename__ = "district_profiles"

    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(String(50), ForeignKey("districts.district_id"), unique=True, nullable=False)
    district_name = Column(String(100), nullable=False)
    population = Column(Integer, nullable=False)
    area_km2 = Column(Float, nullable=False)
    population_density = Column(Float, nullable=False)
    urban_percentage = Column(Float, nullable=False)
    coastal = Column(Boolean, default=False)
    elevation_m = Column(Float, nullable=True)
    source = Column(String(200), default="Census of India & Tamil Nadu DES")
    source_year = Column(Integer, default=2021)
    updated_at = Column(DateTime, default=datetime.utcnow)

    district = relationship("District", back_populates="profile")

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    district_id = Column(String(50), ForeignKey("districts.district_id"), nullable=True)
    category = Column(String(50), default="landmark")  # 'landmark', 'town', 'station'
    created_at = Column(DateTime, default=datetime.utcnow)

class ForecastRun(Base):
    __tablename__ = "forecast_runs"

    id = Column(Integer, primary_key=True, index=True)
    run_timestamp = Column(DateTime, default=datetime.utcnow)
    source = Column(String(50), default="Open-Meteo API")
    status = Column(String(20), default="SUCCESS")  # 'SUCCESS', 'FAILED'
    districts_updated = Column(Integer, default=0)
    details = Column(JSON, nullable=True)

class ForecastData(Base):
    __tablename__ = "forecast_data"

    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(String(50), ForeignKey("districts.district_id"), index=True, nullable=False)
    date = Column(String(20), index=True, nullable=False)  # 'YYYY-MM-DD'
    temp_max = Column(Float, nullable=True)
    temp_min = Column(Float, nullable=True)
    rainfall = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)
    soil_wetness = Column(Float, nullable=True)
    hourly_payload = Column(JSON, nullable=True)
    daily_payload = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    district = relationship("District", back_populates="forecasts")

class RiskResult(Base):
    __tablename__ = "risk_results"

    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(String(50), ForeignKey("districts.district_id"), index=True, nullable=False)
    date = Column(String(20), index=True, nullable=False)  # 'YYYY-MM-DD'
    
    flood_prob = Column(Float, nullable=False)
    flood_risk = Column(String(10), nullable=False)  # 'LOW', 'MEDIUM', 'HIGH'
    
    heatwave_prob = Column(Float, nullable=False)
    heatwave_risk = Column(String(10), nullable=False)
    
    drought_prob = Column(Float, nullable=False)
    drought_risk = Column(String(10), nullable=False)
    
    features_json = Column(JSON, nullable=True)  # Snapshot of 53 features used
    data_quality = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    district = relationship("District", back_populates="risks")

class ModelRegistryRecord(Base):
    __tablename__ = "model_registry"

    id = Column(Integer, primary_key=True, index=True)
    hazard = Column(String(50), unique=True, nullable=False)  # 'flood', 'drought', 'heatwave'
    model_name = Column(String(100), nullable=False)
    model_path = Column(String(255), nullable=False)
    framework = Column(String(50), default="XGBoost")
    n_features = Column(Integer, default=53)
    roc_auc = Column(Float, nullable=True)
    pr_auc = Column(Float, nullable=True)
    status = Column(String(20), default="ACTIVE")
    loaded_at = Column(DateTime, default=datetime.utcnow)

class SystemLog(Base):
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    level = Column(String(20), default="INFO")  # 'INFO', 'WARN', 'ERROR'
    component = Column(String(50), nullable=False) # 'ClimateAgent', 'RiskAgent', 'Auth', etc.
    message = Column(Text, nullable=False)
    details_json = Column(JSON, nullable=True)
