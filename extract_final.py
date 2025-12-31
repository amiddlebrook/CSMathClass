import subprocess
import re
import json

COMMIT = "e2b00c7"

def get_data():
    try:
        # List all files in the commit
        res = subprocess.run(["git", "ls-tree", "-r", "--name-only", COMMIT], capture_output=True, text=True, check=True)
        files = res.stdout.splitlines()
        
        # Filter for Day lessons
        day_files = [f for f in files if "Day" in f and f.endswith(".html")]
        print(f"Checking {len(day_files)} files in {COMMIT}...")
        
        mapping = {}
        # Pattern to catch { title: "...", vid: "..." }
        pattern = re.compile(r"\{\s*title:\s*[\"'](.*?)[\"'].*?vid:\s*[\"']([a-zA-Z0-9_-]{11})[\"'].*?\}", re.IGNORECASE | re.DOTALL)
        
        for f in day_files:
            try:
                content = subprocess.run(["git", "show", f"{COMMIT}:{f}"], capture_output=True, text=True, check=True).stdout
                matches = pattern.findall(content)
                if matches:
                    mapping[f] = [{"title": t, "vid": v} for t, v in matches]
                    print(f"  Found {len(matches)} vids in {f}")
            except Exception:
                continue
        
        return mapping
    except Exception as e:
        print(f"Error: {e}")
        return {}

if __name__ == "__main__":
    data = get_data()
    with open("final_vids_data.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"Done. Extracted data for {len(data)} files.")
