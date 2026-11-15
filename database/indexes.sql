-- Database Performance Indexes
CREATE INDEX IF NOT EXISTS idx_districts_geom ON districts USING GIST(geometry);
CREATE INDEX IF NOT EXISTS idx_climate_obs_date ON climate_observations(observation_date);
CREATE INDEX IF NOT EXISTS idx_climate_obs_dist ON climate_observations(district_id);
CREATE INDEX IF NOT EXISTS idx_hazard_dist ON hazard_events(district_id);
CREATE INDEX IF NOT EXISTS idx_hazard_type ON hazard_events(hazard_type);
CREATE INDEX IF NOT EXISTS idx_infra_geom ON infrastructure_assets USING GIST(geometry);
CREATE INDEX IF NOT EXISTS idx_infra_type ON infrastructure_assets(feature_type);
CREATE INDEX IF NOT EXISTS idx_water_dist ON water_resources(district_id);
