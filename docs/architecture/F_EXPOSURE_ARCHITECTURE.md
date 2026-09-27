# Phase F — Exposure Processing Architecture

## Overview
The Exposure Processing Engine (`backend/services/exposure_service.py`) calculates spatial and demographic exposure overlays for Tamil Nadu's 38 districts.

## Key Exposure Modules
1. **Population Exposure**: Total population, urban/rural distribution, vulnerable age group estimates (Census 2011 + WorldPop 2020).
2. **Built-Environment Exposure**: Total district area, built-up urban area, impervious surface fraction, urban density categories.
3. **Critical Infrastructure Exposure**: Hospitals, power substations, water treatment plants, transportation nodes.
4. **Risk-Exposure Profile Integration**: Combines Phase E XGBoost hazard risk predictions with spatial exposure metrics into a single traceable contract (`RiskExposureProfile`).
