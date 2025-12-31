import subprocess
import re
import json

COMMIT = "e2b00c7"

def get_data():
    try:
        res = subprocess.run(["git", "ls-tree", "-r", "--name-only", COMMIT], capture_output=True, text=True, check=True)
        files = res.stdout.splitlines()
        day_files = [f for f in files if "Day" in f and f.endswith(".html")]
        
        mapping = {}
        # Relaxed regex to find objects with vid: and capture everything inside { ... }
        # Then we'll parse the inside.
        pattern = re.compile(r"\{([^{}]*?vid:\s*[\"'][a-zA-Z0-9_-]{11}[\"'][^{}]*?)\}", re.DOTALL)
        
        for f in day_files:
            try:
                content = subprocess.run(["git", "show", f"{COMMIT}:{f}"], capture_output=True, text=True, check=True).stdout
                matches = pattern.findall(content)
                if matches:
                    mapping[f] = []
                    for inner in matches:
                        # Extract title and vid from the inner content
                        t_match = re.search(r"title:\s*[\"'](.*?)[\"']", inner)
                        v_match = re.search(r"vid:\s*[\"']([a-zA-Z0-9_-]{11})[\"']", inner)
                        if v_match:
                            mapping[f].append({
                                "title": t_match.group(1) if t_match else "Restored Video",
                                "vid": v_match.group(1)
                            })
                    print(f"  Extracted {len(mapping[f])} videos from {f}")
            except Exception:
                continue
        
        return mapping
    except Exception as e:
        print(f"Error: {e}")
        return {}

if __name__ == "__main__":
    data = get_data()
    with open("final_vids_data_refined.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"Done. Extracted data for {len(data)} files.")
