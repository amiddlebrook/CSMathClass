import os
import re

LESSONS_DIR = r"C:\Users\avery\Desktop\Free CS Math\CSMathClass\lessons"

def audit_lessons():
    results = []
    for root, dirs, files in os.walk(LESSONS_DIR):
        for file in files:
            if file.startswith("Day") and file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for placeholders
                has_placeholders = "video_placeholder" in content
                
                # Check for initLesson
                has_init = "initLesson(" in content
                
                # Check for VIDEOS_REAL vs VIDEO_GROUPS
                has_videos_real = "VIDEOS_REAL" in content
                
                # Get Day number from Hero
                hero_match = re.search(r'Day (\d+) ·', content)
                hero_day = hero_match.group(1) if hero_match else "Unknown"
                
                # Get Day number from Title
                title_match = re.search(r'<title>Day (\d+):', content)
                title_day = title_match.group(1) if title_match else "Unknown"
                
                results.append({
                    "file": file,
                    "rel_path": os.path.relpath(path, LESSONS_DIR),
                    "has_init": has_init,
                    "has_placeholders": has_placeholders,
                    "has_videos_real": has_videos_real,
                    "hero_day": hero_day,
                    "title_day": title_day
                })
    return results

if __name__ == "__main__":
    audit_data = audit_lessons()
    print("File | Hero Day | Title Day | Init? | Placeholders? | Real Array?")
    print("---|---|---|---|---|---")
    for r in sorted(audit_data, key=lambda x: x['file']):
        print(f"{r['file']} | {r['hero_day']} | {r['title_day']} | {r['has_init']} | {r['has_placeholders']} | {r['has_videos_real']}")
