# Phase F — Enterprise Security Architecture

## Principles
1. **Least Privilege Database Access**: Application connects via configured non-superuser database roles.
2. **SQL Parameterization**: All database queries use SQLAlchemy ORM parameter binding to prevent SQL injection.
3. **GIS Input Validation**: Uploaded GeoJSON features validated for coordinate range, geometry structure, and CRS.
4. **Secret Management**: Passwords and connection strings managed strictly via `.env` environment variables.
