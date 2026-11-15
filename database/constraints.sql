-- Database Referential & Value Constraints
ALTER TABLE districts ADD CONSTRAINT chk_area_positive CHECK (area_km2 > 0);
ALTER TABLE climate_observations ADD CONSTRAINT chk_humidity_range CHECK (humidity >= 0 AND humidity <= 100);
ALTER TABLE climate_observations ADD CONSTRAINT chk_soil_wetness CHECK (soil_wetness >= 0 AND soil_wetness <= 1);
ALTER TABLE land_cover ADD CONSTRAINT chk_land_pct_sum CHECK (built_up_percentage + vegetation_percentage + water_percentage <= 100);
