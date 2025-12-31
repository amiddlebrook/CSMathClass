import json
import os
import re

def apply_restoration():
    mapping_path = "master_video_mapping.json"
    if not os.path.exists(mapping_path):
        print("Mapping file not found.")
        return

    with open(mapping_path, "r", encoding="utf-8") as f:
        master_mapping = json.load(f)

    # Create a basename-to-data map for easier lookup
    basename_map = {os.path.basename(k): v for k, v in master_mapping.items()}

    updated_count = 0
    LESSONS_DIR = "lessons"
    
    for root, dirs, files in os.walk(LESSONS_DIR):
        for file in files:
            if not (file.endswith(".html") and file.startswith("Day")):
                continue
            
            if file not in basename_map:
                continue
            
            videos = basename_map[file]
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, ".")
            
            print(f"Updating {rel_path}...")
            try:
                with open(abs_path, "r", encoding="utf-8") as f:
                    content = f.read()

                videos_json = json.dumps([{
                    "title": "Lesson Videos",
                    "items": videos
                }], indent=8)
                
                # Try simple replacement first
                new_content = re.sub(
                    r"const VIDEO_GROUPS = \[.*?\];",
                    f"const VIDEO_GROUPS = {videos_json};",
                    content,
                    flags=re.DOTALL
                )
                
                if new_content == content:
                    # Try initLesson fallback
                    new_content = re.sub(
                        r"videos:\s*\[.*?\]",
                        f"videos: {videos_json}",
                        content,
                        flags=re.DOTALL
                    )
                
                if new_content != content:
                    with open(abs_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    updated_count += 1
                    print(f"  Success.")
                else:
                    print(f"  [WARNING] No replacement made in {rel_path}")

            except Exception as e:
                print(f"  [ERROR] Failed to update {rel_path}: {e}")

    print(f"Restoration complete. Updated {updated_count} files.")

if __name__ == "__main__":
    apply_restoration()
