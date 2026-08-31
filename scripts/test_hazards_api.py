import httpx

tok_r = httpx.post('http://127.0.0.1:8000/auth/login', json={'username': 'harish', 'password': 'user123'})
tok = tok_r.json()['access_token']
headers = {'Authorization': f'Bearer {tok}'}

print("\n--- 1. Testing Chennai (Coastal District) ---")
r = httpx.get('http://127.0.0.1:8000/risk/chennai/hazards?day=0', headers=headers)
print('Status:', r.status_code)
if r.status_code == 200:
    for k, v in r.json()['hazards'].items():
        print(f"  {k:18s} | {v['display_value']:26s} | {v['risk_level']:14s} | {v['engine_type']}")

print("\n--- 2. Testing Coimbatore (Inland District - Coastal should be NOT_APPLICABLE) ---")
r2 = httpx.get('http://127.0.0.1:8000/risk/coimbatore/hazards?day=0', headers=headers)
print('Status:', r2.status_code)
if r2.status_code == 200:
    coastal_h = r2.json()['hazards'].get('coastal')
    print('  Coastal in Coimbatore:', coastal_h['risk_level'], '|', coastal_h['display_value'], '| Reason:', coastal_h.get('reason'))

print("\n--- 3. Testing Admin Debug Endpoint ---")
admin_r = httpx.post('http://127.0.0.1:8000/auth/login', json={'username': 'admin', 'password': 'admin123'})
admin_tok = admin_r.json()['access_token']
dbg_r = httpx.get('http://127.0.0.1:8000/system/debug?district_id=chennai', headers={'Authorization': f'Bearer {admin_tok}'})
print('Debug status:', dbg_r.status_code)
if dbg_r.status_code == 200:
    dbg = dbg_r.json()
    print('Contracts:', dbg['contracts'])
    print('Comparison sample count:', len(dbg['features_comparison']))
