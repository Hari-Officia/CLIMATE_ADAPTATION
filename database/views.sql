-- All 11 Required Analytical Views for Phase 1 Foundation

CREATE OR REPLACE VIEW v_latest_climate_by_district AS
SELECT DISTINCT ON (district_id)
    district_id, observation_date, temp_max, temp_min, temp_mean, humidity, wind_speed, rainfall, soil_wetness
FROM climate_observations
ORDER BY district_id, observation_date DESC;

CREATE OR REPLACE VIEW v_daily_climate_by_district AS
SELECT district_id, observation_date, temp_max, temp_min, temp_mean, temp_range, humidity, wind_speed, rainfall, soil_wetness
FROM climate_observations;

CREATE OR REPLACE VIEW v_monthly_climate_by_district AS
SELECT 
    district_id,
    EXTRACT(YEAR FROM observation_date) AS year,
    EXTRACT(MONTH FROM observation_date) AS month,
    AVG(temp_max) AS temp_max_mean,
    AVG(temp_min) AS temp_min_mean,
    AVG(humidity) AS humidity_mean,
    SUM(rainfall) AS monthly_rainfall_sum
FROM climate_observations
GROUP BY district_id, EXTRACT(YEAR FROM observation_date), EXTRACT(MONTH FROM observation_date);

CREATE OR REPLACE VIEW v_hazard_events_by_district AS
SELECT district_id, hazard_type, COUNT(*) AS total_events, SUM(deaths) AS total_deaths, SUM(affected_population) AS total_affected
FROM hazard_events
GROUP BY district_id, hazard_type;

CREATE OR REPLACE VIEW v_population_exposure_by_district AS
SELECT d.district_id, d.district_name, d.population_2011, d.population_density, d.coastal, p.urban_percentage, p.vulnerability_index
FROM districts d
LEFT JOIN population_exposure p ON d.district_id = p.district_id;

CREATE OR REPLACE VIEW v_infrastructure_by_district AS
SELECT district_id, feature_type, COUNT(*) AS asset_count
FROM infrastructure_assets
GROUP BY district_id, feature_type;

CREATE OR REPLACE VIEW v_water_status_by_district AS
SELECT district_id, assessment_year, groundwater_status, groundwater_extraction_pct, reservoir_storage_pct
FROM water_resources;

CREATE OR REPLACE VIEW v_air_quality_by_district AS
SELECT district_id, DATE(observation_time) AS obs_date, AVG(pm25) AS pm25_mean, AVG(pm10) AS pm10_mean
FROM air_quality
GROUP BY district_id, DATE(observation_time);

CREATE OR REPLACE VIEW v_land_cover_by_district AS
SELECT district_id, year, built_up_percentage, vegetation_percentage, forest_percentage, water_percentage, wetland_percentage, agricultural_percentage
FROM land_cover;

CREATE OR REPLACE VIEW v_adaptation_strategy_eligibility AS
SELECT s.strategy_id, s.strategy_name, s.strategy_domain, s.primary_hazards, s.cost_level, s.effectiveness
FROM strategies s;

CREATE OR REPLACE VIEW v_district_data_completeness AS
SELECT district_id, district_name, coastal, area_km2, population_2011
FROM districts;
