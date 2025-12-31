import json
import os
import subprocess
import re

# Load extracted IDs
with open("extracted_vids.json", "r") as f:
    extracted = json.load(f)

# Get current lesson files
LESSONS_DIR = "lessons"
all_lessons = []
for root, dirs, files in os.walk(LESSONS_DIR):
    for file in files:
        if file.endswith(".html") and file.startswith("Day"):
            rel_path = os.path.relpath(os.path.join(root, file), ".").replace("\\", "/")
            all_lessons.append(rel_path)

missing = [l for l in all_lessons if l not in extracted]

print(f"Total lessons found: {len(all_lessons)}")
print(f"Lessons missing from e2b00c7: {len(missing)}")

# Search history for each missing lesson
def search_history(file_path):
    print(f"Searching history for {file_path}...")
    try:
        # Search for any string that looks like a YouTube ID (11 chars in quotes)
        # and has been added or removed in history
        cmd = ["git", "log", "-S", "'", "--oneline", "--all", "--", file_path] # Greedy search
        # Actually better to use git log -p and search diffs
        cmd = ["git", "log", "-p", "--all", "--", file_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        content = result.stdout
        
        # Regex for YouTube IDs in quotes
        vids = re.findall(r"[\"']([a-zA-Z0-9_-]{11})[\"']", content)
        # Filter out common false positives if any, or just take unique
        unique_vids = list(set(vids))
        # Filter out placeholders
        unique_vids = [v for v in unique_vids if not v.startswith("video_placeholder")]
        # Filter out 'shared-styles' etc (though 11 chars is specific)
        
        return unique_vids
    except Exception as e:
        return []

history_mapping = {}
for m in missing:
    vids = search_history(m)
    if vids:
        history_mapping[m] = vids
        print(f"  Found {len(vids)} potential IDs in history.")

# Combine with extracted
total_mapping = {**extracted}
for k, v in history_mapping.items():
    if k not in total_mapping:
        total_mapping[k] = v
    else:
        # Merge unique
        total_mapping[k] = list(set(total_mapping[k] + v))

with open("total_vids_mapping.json", "w") as f:
    json.dump(total_mapping, f, indent=2)

print(f"Total mapping now has {len(total_mapping)} files.")
missing_still = [l for l in all_lessons if l not in total_mapping]
print(f"Still missing: {len(missing_still)}")
print(missing_still)
