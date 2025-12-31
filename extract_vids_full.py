import subprocess
import re
import json

COMMIT = "e2b00c7"

def get_video_data():
    try:
        # Get list of files in the commit
        cmd = ["git", "ls-tree", "-r", "--name-only", COMMIT]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        all_files = result.stdout.splitlines()
        
        mapping = {}
        # Regex to capture the whole object or just vid/title
        obj_pattern = re.compile(r"\{\s*title:\s*[\"'](.*?)[\"'].*?vid:\s*[\"']([a-zA-Z0-9_-]{11})[\"'].*?\}", re.IGNORECASE | re.DOTALL)
        
        for file_path in all_files:
            if not file_path.endswith(".html") or not "Day" in file_path:
                continue
            
            show_cmd = ["git", "show", f"{COMMIT}:{file_path}"]
            show_result = subprocess.run(show_cmd, capture_output=True, text=True)
            if show_result.returncode != 0:
                continue
                
            content = show_result.stdout
            matches = obj_pattern.findall(content)
            if matches:
                mapping[file_path] = []
                for title, vid in matches:
                    mapping[file_path].append({"title": title, "vid": vid})
                print(f"Extracted {len(matches)} videos from {file_path}")
        
        return mapping
    except Exception as e:
        print(f"Error: {e}")
        return {}

if __name__ == "__main__":
    mapping = get_video_data()
    with open("full_video_data.json", "w") as f:
        json.dump(mapping, f, indent=2)
    print(f"Extracted data for {len(mapping)} files.")
