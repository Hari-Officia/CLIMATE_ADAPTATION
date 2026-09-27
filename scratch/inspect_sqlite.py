import sqlite3

conn = sqlite3.connect("backend/data/climate_risk.db")
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
tables = [r[0] for r in cur.fetchall()]

print("Found tables in SQLite:")
for t in tables:
    count = cur.execute(f"SELECT COUNT(*) FROM \"{t}\"").fetchone()[0]
    print(f" - {t}: {count} rows")

conn.close()
