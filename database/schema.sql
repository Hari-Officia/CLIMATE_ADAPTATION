-- ============================================================
-- TAMIL NADU CLIMATE ADAPTATION DATA FOUNDATION (PHASE 1)
-- PostgreSQL + PostGIS Schema Definition
-- ============================================================

CREATE EXTENSION IF NOT EXISTS postgis;

-- 1. DISTRICT MASTER TABLE
CREATE TABLE IF NOT EXISTS districts (
    district_id VARCHAR(50) PRIMARY KEY,
    district_name VARCHAR(100) NOT NULL,
    official_name VARCHAR(150) NOT NULL,
    state VARCHAR(50) NOT NULL DEFAULT 'Tamil Nadu',
    geometry GEOMETRY(MultiPolygon, 4326),
    area_km2 NUMERIC(10, 2),
    centroid_lat NUMERIC(9, 6),
    centroid_lon NUMERIC(9, 6),
    population_2011 INT,
    population_density NUMERIC(10, 2),
    coastal BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(200),
    source_reference VARCHAR(250)
);

-- 2. CLIMATE OBSERVATIONS (DAILY)
CREATE TABLE IF NOT EXISTS climate_observations (
    observation_id SERIAL PRIMARY KEY,
    district_id VARCHAR(50) REFERENCES districts(district_id) ON DELETE CASCADE,
    observation_date DATE NOT NULL,
    temp_max NUMERIC(5, 2),
    temp_min NUMERIC(5, 2),
    temp_mean NUMERIC(5, 2),
    temp_range NUMERIC(5, 2),
    humidity NUMERIC(5, 2),
    wind_speed NUMERIC(5, 2),
    surface_pressure NUMERIC(6, 2),
    solar_radiation NUMERIC(6, 2),
    soil_wetness NUMERIC(5, 4),
    rainfall NUMERIC(6, 2),
    source_id VARCHAR(50),
    quality_flag VARCHAR(50) DEFAULT 'PASSED_VERIFIED',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT idx_district_date UNIQUE(district_id, observation_date)
) PARTITION BY RANGE (observation_date);

-- 3. CLIMATE DERIVED FEATURES
CREATE TABLE IF NOT EXISTS climate_derived_features (
    feature_id SERIAL PRIMARY KEY,
    district_id VARCHAR(50) REFERENCES districts(district_id) ON DELETE CASCADE,
    feature_date DATE NOT NULL,
    rainfall_3d NUMERIC(7, 2),
    rainfall_7d NUMERIC(7, 2),
    rainfall_30d NUMERIC(7, 2),
    temp_anomaly NUMERIC(5, 2),
    rainfall_anomaly NUMERIC(6, 2),
    spi_3 NUMERIC(6, 3),
    spi_6 NUMERIC(6, 3),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT idx_derived_district_date UNIQUE(district_id, feature_date)
);

-- 4. HAZARD EVENTS
CREATE TABLE IF NOT EXISTS hazard_events (
    event_id VARCHAR(50) PRIMARY KEY,
    hazard_type VARCHAR(50) NOT NULL,
    event_name VARCHAR(150),
    district_id VARCHAR(50) REFERENCES districts(district_id),
    start_date DATE,
    end_date DATE,
    latitude NUMERIC(9, 6),
    longitude NUMERIC(9, 6),
    severity VARCHAR(50),
    deaths INT DEFAULT 0,
    affected_population INT DEFAULT 0,
    economic_damage_inr NUMERIC(15, 2),
    source_id VARCHAR(50),
    quality_flag VARCHAR(50) DEFAULT 'PASSED_VERIFIED'
);

-- 5. POPULATION EXPOSURE
CREATE TABLE IF NOT EXISTS population_exposure (
    exposure_id SERIAL PRIMARY KEY,
    district_id VARCHAR(50) REFERENCES districts(district_id),
    year INT NOT NULL,
    total_population INT,
    population_density NUMERIC(10, 2),
    urban_percentage NUMERIC(5, 2),
    children_population INT,
    elderly_population INT,
    vulnerability_index NUMERIC(5, 4),
    source VARCHAR(100)
);

-- 6. INFRASTRUCTURE ASSETS
CREATE TABLE IF NOT EXISTS infrastructure_assets (
    asset_id VARCHAR(100) PRIMARY KEY,
    district_id VARCHAR(50) REFERENCES districts(district_id),
    feature_type VARCHAR(50) NOT NULL,
    name VARCHAR(200),
    geometry GEOMETRY(Point, 4326),
    latitude NUMERIC(9, 6),
    longitude NUMERIC(9, 6),
    source VARCHAR(100),
    source_date DATE
);

-- 7. LAND COVER
CREATE TABLE IF NOT EXISTS land_cover (
    land_id SERIAL PRIMARY KEY,
    district_id VARCHAR(50) REFERENCES districts(district_id),
    year INT NOT NULL,
    built_up_percentage NUMERIC(5, 2),
    vegetation_percentage NUMERIC(5, 2),
    forest_percentage NUMERIC(5, 2),
    water_percentage NUMERIC(5, 2),
    wetland_percentage NUMERIC(5, 2),
    agricultural_percentage NUMERIC(5, 2),
    source VARCHAR(100)
);

-- 8. WATER & GROUNDWATER RESOURCES
CREATE TABLE IF NOT EXISTS water_resources (
    water_id SERIAL PRIMARY KEY,
    district_id VARCHAR(50) REFERENCES districts(district_id),
    assessment_year INT NOT NULL,
    groundwater_status VARCHAR(50),
    groundwater_extraction_pct NUMERIC(5, 2),
    reservoir_capacity_mcm NUMERIC(10, 2),
    reservoir_storage_pct NUMERIC(5, 2),
    source VARCHAR(100)
);

-- 9. AIR QUALITY OBSERVATIONS
CREATE TABLE IF NOT EXISTS air_quality (
    aq_id SERIAL PRIMARY KEY,
    district_id VARCHAR(50) REFERENCES districts(district_id),
    station_id VARCHAR(50),
    observation_time TIMESTAMP WITH TIME ZONE,
    pm25 NUMERIC(6, 2),
    pm10 NUMERIC(6, 2),
    no2 NUMERIC(6, 2),
    so2 NUMERIC(6, 2),
    co NUMERIC(6, 2),
    o3 NUMERIC(6, 2),
    source VARCHAR(100)
);

-- 10. ADAPTATION STRATEGIES
CREATE TABLE IF NOT EXISTS strategies (
    strategy_id VARCHAR(50) PRIMARY KEY,
    strategy_name VARCHAR(200) NOT NULL,
    strategy_domain VARCHAR(100) NOT NULL,
    strategy_type VARCHAR(50) NOT NULL,
    description TEXT,
    primary_hazards VARCHAR(100),
    secondary_hazards VARCHAR(100),
    cost_level VARCHAR(20),
    effectiveness VARCHAR(20),
    implementation_horizon VARCHAR(30),
    evidence_strength VARCHAR(30)
);

-- 11. SOURCE REGISTRY & PROVENANCE
CREATE TABLE IF NOT EXISTS sources (
    source_id VARCHAR(50) PRIMARY KEY,
    organization VARCHAR(150),
    dataset VARCHAR(150),
    category VARCHAR(50),
    tier VARCHAR(20),
    url_reference VARCHAR(250),
    access_method VARCHAR(50),
    license VARCHAR(50),
    temporal_resolution VARCHAR(50),
    spatial_resolution VARCHAR(50),
    retrieval_status VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS provenance (
    record_id VARCHAR(50) PRIMARY KEY,
    source_id VARCHAR(50) REFERENCES sources(source_id),
    dataset_id VARCHAR(100),
    retrieval_timestamp TIMESTAMP WITH TIME ZONE,
    transformation TEXT,
    quality_flag VARCHAR(50)
);
