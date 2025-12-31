import subprocess
import re
import json

COMMIT = "e2b00c7"

def get_video_ids():
    try:
        # Run git grep to find lines with vid: or id: followed by a 11-char string in quotes
        cmd = ["git", "grep", "-E", "vid: [\"'][a-zA-Z0-9_-]{11}[\"']|id: [\"'][a-zA-Z0-9_-]{11}[\"']", COMMIT, "--", "*.html"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = result.stdout.splitlines()
        
        mapping = {}
        # Regex to capture file path and the ID
        # Example line: e2b00c7:lessons/05-discrete-math/DayTwentyFour.html:            { title: "Propositional Logic", channel: "TrevTutor", vid: "f5oFz2O5tQM" },
        pattern = re.compile(rf"{COMMIT}:(.*?html):.*?(?:vid|id):\s*[\"']([a-zA-Z0-9_-]{{11}})[\"']")
        
        for line in lines:
            match = pattern.search(line)
            if match:
                file_path = match.group(1)
                vid_id = match.group(2)
                if file_path not in mapping:
                    mapping[file_path] = []
                mapping[file_path].append(vid_id)
        
        return mapping
    except subprocess.CalledProcessError as e:
        print(f"Error running git grep: {e}")
        return {}

if __name__ == "__main__":
    mapping = get_video_ids()
    with open("extracted_vids.json", "w") as f:
        json.dump(mapping, f, indent=2)
    print(f"Extracted IDs for {len(mapping)} files.")
