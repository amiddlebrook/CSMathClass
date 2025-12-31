import subprocess
import re
import json
import os

def get_vids_from_commit(commit):
    try:
        res = subprocess.run(["git", "ls-tree", "-r", "--name-only", commit], capture_output=True, text=True, check=True)
        all_files = res.stdout.splitlines()
        day_files = [f for f in all_files if "Day" in f and f.endswith(".html")]
        
        mapping = {}
        # Relaxed regex to find objects with vid:
        pattern = re.compile(r"\{([^{}]*?vid:\s*[\"']([a-zA-Z0-9_-]{11})[\"'][^{}]*?)\}", re.DOTALL)
        
        for f in day_files:
            try:
                content = subprocess.run(["git", "show", f"{commit}:{f}"], capture_output=True, text=True, check=True).stdout
                matches = pattern.findall(content)
                if matches:
                    mapping[f] = []
                    for inner, vid in matches:
                        t_match = re.search(r"title:\s*[\"'](.*?)[\"']", inner)
                        mapping[f].append({
                            "title": t_match.group(1) if t_match else "Restored Video",
                            "vid": vid
                        })
            except Exception:
                continue
        return mapping
    except Exception:
        return {}

def get_vids_from_current():
    mapping = {}
    LESSONS_DIR = "lessons"
    pattern = re.compile(r"\{([^{}]*?vid:\s*[\"']([a-zA-Z0-9_-]{11})[\"'][^{}]*?)\}", re.DOTALL)
    
    for root, dirs, files in os.walk(LESSONS_DIR):
        for file in files:
            if file.endswith(".html") and file.startswith("Day"):
                rel_path = os.path.relpath(os.path.join(root, file), ".").replace("\\", "/")
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        content = f.read()
                    matches = pattern.findall(content)
                    if matches:
                        vids = []
                        for inner, vid in matches:
                            if "video_placeholder" in vid: continue
                            t_match = re.search(r"title:\s*[\"'](.*?)[\"']", inner)
                            vids.append({
                                "title": t_match.group(1) if t_match else "Current Video",
                                "vid": vid
                            })
                        if vids:
                            mapping[rel_path] = vids
                except Exception:
                    continue
    return mapping

if __name__ == "__main__":
    golden = get_vids_from_commit("e2b00c7")
    current = get_vids_from_current()
    
    # Merge
    master = {**golden}
    for k, v in current.items():
        if k not in master:
            master[k] = v
        else:
            # Prefer current if it has real IDs and maybe better titles
            # But golden is usually more "original"
            # We'll just take the one with MORE real videos
            if len(v) > len(master[k]):
                master[k] = v
                
    with open("master_video_mapping.json", "w") as f:
        json.dump(master, f, indent=2)
    
    print(f"Master mapping has {len(master)} files.")
