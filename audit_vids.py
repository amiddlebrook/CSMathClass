import json
import os

def audit_restoration():
    mapping_path = "master_video_mapping.json"
    if not os.path.exists(mapping_path):
        print("Mapping file not found.")
        return
        
    with open(mapping_path, "r", encoding="utf-8") as f:
        master_mapping = json.load(f)
    
    basename_map = {os.path.basename(k): v for k, v in master_mapping.items()}
    
    placeholders = []
    restored = []
    missing_from_mapping = []
    
    LESSONS_DIR = "lessons"
    for root, dirs, files in os.walk(LESSONS_DIR):
        for file in files:
            if not (file.endswith(".html") and file.startswith("Day")):
                continue
            
            abs_path = os.path.join(root, file)
            try:
                with open(abs_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except:
                continue
            
            if "video_placeholder" in content:
                placeholders.append(file)
                if file not in basename_map:
                    missing_from_mapping.append(file)
            else:
                restored.append(file)
                
    print(f"Summary:")
    print(f"  Restored: {len(restored)}")
    print(f"  Still Placeholders: {len(placeholders)}")
    print(f"  Missing from Mapping: {len(missing_from_mapping)}")
    if missing_from_mapping:
        print(f"  First few missing from mapping: {missing_from_mapping[:10]}")
    if placeholders and not missing_from_mapping:
        print("All remaining placeholders ARE in the mapping but weren't updated.")

if __name__ == "__main__":
    audit_restoration()
