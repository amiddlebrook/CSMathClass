import json
import os
import subprocess
import re

# Load extracted IDs from the "golden" commit
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

# Known false positives from previous run
FALSE_POSITIVES = {
    "btnCheckAll", "btnRevealAll", "stats-label", "main-layout", "themeToggle", 
    "stats-value", "code-number", "code-header", "video-title", "statCorrect",
    "main-content", "hero-label", "formula-box", "formula-main", "equivalence",
    "composition", "polynomials", "math-inline", "Numberphile", "CrashCourse",
    "3Blue1Brown", "btnReset", "statAttempted", "statAccuracy", "progressFill"
}

def is_likely_youtube_id(s):
    if s in FALSE_POSITIVES:
        return False
    if len(s) != 11:
        return False
    # YouTube IDs usually have a mix of character types or at least don't look like common English/code words
    # But some might be all lowercase.
    # We'll use a heuristic: if it's purely lowercase and contains common words, skip?
    # Actually, the best way is to see where it occurs.
    return True

# Refine extracted mapping (remove false positives)
refined_extracted = {}
for path, vids in extracted.items():
    vids = [v for v in vids if is_likely_youtube_id(v)]
    if vids:
        refined_extracted[path] = vids

# Search history for missing lessons with better filtering
def search_history(file_path):
    try:
        cmd = ["git", "log", "-p", "--all", "--", file_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        content = result.stdout
        
        # Look for vid: "..." or id: "..." specifically
        raw_vids = re.findall(r"(?:vid|id):\s*[\"']([a-zA-Z0-9_-]{11})[\"']", content)
        
        vids = [v for v in raw_vids if is_likely_youtube_id(v)]
        return list(set(vids))
    except Exception:
        return []

missing = [l for l in all_lessons if l not in refined_extracted]
history_mapping = {}
for m in missing:
    vids = search_history(m)
    if vids:
        history_mapping[m] = vids

# Combine
total_mapping = {**refined_extracted}
for k, v in history_mapping.items():
    if k not in total_mapping:
        total_mapping[k] = v
    else:
        total_mapping[k] = list(set(total_mapping[k] + v))

with open("refined_vids_mapping.json", "w") as f:
    json.dump(total_mapping, f, indent=2)

print(f"Refined mapping has {len(total_mapping)} files.")
missing_still = [l for l in all_lessons if l not in total_mapping]
print(f"Still missing: {len(missing_still)}")
print(missing_still)
