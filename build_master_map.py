import os
import re
import json

root_dir = r"c:\Users\avery\Desktop\Free CS Math\CSMathClass\lessons"
output_file = "curriculum_map.json"

num_to_word = {
    1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten',
    11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen', 15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen', 19: 'Nineteen', 20: 'Twenty',
    21: 'TwentyOne', 22: 'TwentyTwo', 23: 'TwentyThree', 24: 'TwentyFour', 25: 'TwentyFive', 26: 'TwentySix', 27: 'TwentySeven', 28: 'TwentyEight', 29: 'TwentyNine', 30: 'Thirty',
    31: 'ThirtyOne', 32: 'ThirtyTwo', 33: 'ThirtyThree', 34: 'ThirtyFour', 35: 'ThirtyFive', 36: 'ThirtySix', 37: 'ThirtySeven', 38: 'ThirtyEight', 39: 'ThirtyNine', 40: 'Forty',
    41: 'FortyOne', 42: 'FortyTwo', 43: 'FortyThree', 44: 'FortyFour', 45: 'FortyFive', 46: 'FortySix', 47: 'FortySeven', 48: 'FortyEight', 49: 'FortyNine', 50: 'Fifty',
    51: 'FiftyOne', 52: 'FiftyTwo', 53: 'FiftyThree', 54: 'FiftyFour', 55: 'FiftyFive', 56: 'FiftySix', 57: 'FiftySeven', 58: 'FiftyEight', 59: 'FiftyNine', 60: 'Sixty',
    61: 'SixtyOne', 62: 'SixtyTwo', 63: 'SixtyThree', 64: 'SixtyFour', 65: 'SixtyFive', 66: 'SixtySix', 67: 'SixtySeven', 68: 'SixtyEight', 69: 'SixtyNine', 70: 'Seventy',
    71: 'SeventyOne', 72: 'SeventyTwo', 73: 'SeventyThree', 74: 'SeventyFour', 75: 'SeventyFive', 76: 'SeventySix', 77: 'SeventySeven', 78: 'SeventyEight', 79: 'SeventyNine', 80: 'Eighty',
    81: 'EightyOne', 82: 'EightyTwo', 83: 'EightyThree', 84: 'EightyFour', 85: 'EightyFive', 86: 'EightySix', 87: 'EightySeven', 88: 'EightyEight', 89: 'EightyNine', 90: 'Ninety',
    91: 'NinetyOne', 92: 'NinetyTwo', 93: 'NinetyThree', 94: 'NinetyFour', 95: 'NinetyFive', 96: 'NinetySix', 97: 'NinetySeven', 98: 'NinetyEight', 99: 'NinetyNine', 100: 'OneHundred'
}
word_to_num = {v: k for k, v in num_to_word.items()}

curriculum = {}

print("Scanning lessons...")
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".html") and "index.html" not in file and "_Duplicate" not in file:
            full_path = os.path.join(root, file)
            
            # Parse Day Number from filename
            name_part = file.replace("Day", "").replace(".html", "")
            day_num = word_to_num.get(name_part)
            
            if day_num:
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Extract Topic from Hero
                    # Match: Day 12 · Topic Name
                    hero_match = re.search(r'Day\s+(\d+)\s*[·:]\s*([^<]+)', content)
                    topic = "Unknown"
                    if hero_match:
                        topic = hero_match.group(2).strip()
                        
                    # Extract Title
                    title_match = re.search(r'<title>(.*?)</title>', content)
                    title = "Unknown"
                    if title_match:
                        title = title_match.group(1).strip()

                    rel_path = os.path.relpath(full_path, r"c:\Users\avery\Desktop\Free CS Math\CSMathClass").replace("\\", "/")
                    
                    curriculum[day_num] = {
                        "day": day_num,
                        "path": full_path,
                        "relPath": rel_path,
                        "topic": topic,
                        "title": title,
                        "filename": file
                    }
                except Exception as e:
                    with open("error_log.txt", "a") as ef:
                        ef.write(f"Error reading {full_path}: {e}\n")
            else:
                with open("error_log.txt", "a") as ef:
                    ef.write(f"Skipping {file}: Could not parse day number from '{name_part}'\n")


# Save
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(curriculum, f, indent=4)

print(f"Mapped {len(curriculum)} lessons to {output_file}")
