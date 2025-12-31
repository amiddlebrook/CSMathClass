import json

# Expected range: 1 to 100
ALL_DAYS = set(range(1, 101))

try:
    with open('curriculum_map.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    present_days = set(int(k) for k in data.keys())
    missing = sorted(list(ALL_DAYS - present_days))
    
    print(f"Present: {len(present_days)}")
    print(f"Missing ({len(missing)}): {missing}")
    
except Exception as e:
    print(f"Error: {e}")
