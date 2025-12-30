
import os
import shutil
import re

# Base paths
BASE_DIR = r"c:\Users\avery\Desktop\CSMathClass\CSMathClass\lessons"
ARCHIVE_DIR = os.path.join(BASE_DIR, "_archive")

# Mapping: New_Path -> Source_Path
# Note: Source paths are relative to BASE_DIR/
# New paths are relative to BASE_DIR/
MAPPING = {
    # Section 01: Mathematical Maturity (Days 1-6)
    "01-mathematical-maturity/DayOne.html": "01-operating-system/DayOne.html", # To be merged with 2 & 3
    "01-mathematical-maturity/DayTwo.html": "01-operating-system/DayFour.html", # Logic
    "01-mathematical-maturity/DayThree.html": "01-operating-system/DaySeven.html", # Set Theory
    "01-mathematical-maturity/DayFour.html": "01-operating-system/DayFive.html", # Proofs I
    "01-mathematical-maturity/DayFive.html": "01-operating-system/DaySix.html", # Proofs II
    "01-mathematical-maturity/DaySix.html": "01-operating-system/DayEight.html", # Checkpoint

    # Section 02: Calculus (Days 7-18)
    "02-calculus/DaySeven.html": "03-calculus/DayFourteen.html", # Limits (Base for Limits+Growth)
    "02-calculus/DayEight.html": "02-precalculus/DayTen.html", # Trig (Base for Trig+Complex)
    "02-calculus/DayNine.html": "03-calculus/DayFifteen.html", # Derivatives I
    "02-calculus/DayTen.html": "03-calculus/DaySixteen.html", # Derivatives II
    "02-calculus/DayEleven.html": "03-calculus/DaySeventeen.html", # Apps
    "02-calculus/DayTwelve.html": "03-calculus/DayEighteen.html", # Integrals I
    "02-calculus/DayThirteen.html": "03-calculus/DayNineteen.html", # Integrals II
    "02-calculus/DayFourteen.html": "03-calculus/DayTwenty.html", # ODEs (Base for ODEs+Series)
    "02-calculus/DayFifteen.html": "08-analysis/DaySixtyThree.html", # Multivariable (From Analysis)
    "02-calculus/DaySixteen.html": "08-analysis/DaySixtyThree.html", # COPY AGAIN for splitting? No, create placeholder.
    # Day 16, 17, 18 will be created manually or placeholders for now.
}

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def update_day_title(content, new_day_num, new_section_name):
    # Regex to replace <title>Day X: ...</title>
    # and "Day X · SectionName" in hero
    
    # 1. Update Title Tag
    # Look for <title>Day [word/num]: Title</title>
    # We'll just replace "Day [OldNum]" with "Day [NewNum]"
    # This is a bit loose, but sufficient for a rough pass.
    
    # Simple integer map for words
    words = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", 
             "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen", "Twenty"]
    
    new_day_word = words[new_day_num] if new_day_num < len(words) else str(new_day_num)
    
    # Replace in <title>
    content = re.sub(r'<title>Day \w+:', f'<title>Day {new_day_num}:', content)
    content = re.sub(r'<title>Day \d+:', f'<title>Day {new_day_num}:', content)
    
    # Replace in Hero Label
    # Day X · OldSection -> Day X · NewSection
    content = re.sub(r'Day \d+ · [\w\s]+', f'Day {new_day_num} · {new_section_name}', content)
    
    return content

def migrate():
    print("Starting migration...")
    
    for new_rel, src_rel in MAPPING.items():
        src_path = os.path.join(BASE_DIR, src_rel)
        dest_path = os.path.join(BASE_DIR, new_rel)
        
        print(f"Migrating {src_rel} -> {new_rel}")
        
        if not os.path.exists(src_path):
            print(f"!! Source not found: {src_path}")
            continue
            
        ensure_dir(dest_path)
        
        with open(src_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract day number from new filename (simplistic)
        # 02-calculus/DaySeven.html -> 7
        filename = os.path.basename(new_rel)
        # This part is tricky to automate perfectly without a map of "DaySeven"->7.
        # For now, I'll just copy the file. The Agent (Me) will do the fine-tuning edits.
        # But I SHOULD try to update the Section Name in the Hero at least.
        
        section_slug = new_rel.split('/')[0] # 01-mathematical-maturity
        section_name_map = {
            "01-mathematical-maturity": "Mathematical Maturity",
            "02-calculus": "Calculus",
            "03-linear-algebra": "Linear Algebra"
        }
        section_clean = section_name_map.get(section_slug, "Curriculum")
        
        # Perform replacements
        # We can't easily guess the Day Number from "DaySeven.html" programmatically without a dictionary.
        # I will leave the detailed content editing to the Agent steps.
        # The script's job is just to PLACE the files correctly.
        
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
