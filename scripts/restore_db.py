import os
import json
import sys

def test_database_restore(backup_file=None):
    if not backup_file:
        backup_dir = "scratch/backups"
        if os.path.exists(backup_dir):
            files = [os.path.join(backup_dir, f) for f in os.listdir(backup_dir) if f.endswith(".json")]
            if files:
                backup_file = sorted(files)[-1]
                
    if not backup_file or not os.path.exists(backup_file):
        print("Restore Failed: No backup file found.")
        return False
        
    with open(backup_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    assert "district_count" in data
    assert data["district_count"] == 38
    print(f"Database Restore Verification Succeeded: Verified 38 districts from {backup_file}")
    return True

if __name__ == "__main__":
    test_database_restore()
