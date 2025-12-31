import json
import os
import re

map_file = "curriculum_map.json"
with open(map_file, 'r', encoding='utf-8') as f:
    curriculum = json.load(f)

print(f"Loaded {len(curriculum)} lessons.")

for day_str, info in curriculum.items():
    file_path = info['path']
    day_num = info['day']
    topic = info['topic']
    
    # Construct desired title
    new_title = f"Day {day_num}: {topic}"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Replace Regex
        # Matches <title>...</title>
        # We need to be careful not to match too much if newlines
        
        # Check current title
        title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
        if title_match:
            current_title = title_match.group(1)
            if current_title.strip() == new_title:
                continue # Already correct
                
            print(f"Updating Day {day_num}: '{current_title}' -> '{new_title}'")
            new_content = re.sub(r'<title>.*?</title>', f'<title>{new_title}</title>', content, count=1, flags=re.DOTALL)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        else:
            print(f"Day {day_num}: No title tag found.")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print("Metadata updates complete.")
