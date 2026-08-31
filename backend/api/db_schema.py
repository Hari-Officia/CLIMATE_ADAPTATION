from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry

DATABASE_URL = "postgresql://climate_user:climate_password@localhost:5432/climate_risk_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class District(Base):
    __tablename__ = "districts"
    id = Column(Integer, primary_key=True)
    district_name = Column(String, unique=True, index=True)
    geometry = Column(Geometry('MULTIPOLYGON'))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String, default="USER")

# ... (Additional tables like Forecasts, RiskResults will follow)
