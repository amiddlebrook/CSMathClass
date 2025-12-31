import json
import re

# Ranges Configuration (Inclusive)
# Order matters for the final index
SECTIONS = [
    {"title": "Mathematical Foundations", "range": range(1, 7)},
    {"title": "Precalculus", "range": range(7, 12)},
    {"title": "Linear Algebra", "range": range(19, 24)},
    {"title": "Calculus", "range": range(12, 19)},
    {"title": "Discrete Mathematics", "range": range(24, 32)},
    {"title": "Algorithms & Data Structures", "range": range(32, 39)},
    {"title": "Probability & Statistics", "range": range(39, 44)},
    {"title": "Optimization & Numerical Methods", "days": [51] + list(range(81, 86))},
    {"title": "Mathematical Analysis", "range": range(44, 51)},
    {"title": "Abstract Algebra", "range": range(52, 55)},
    {"title": "Topology & Measure Theory", "range": range(55, 62)},
    {"title": "Functional Analysis & PDE", "range": range(62, 69)},
    {"title": "Theoretical Computer Science", "range": range(69, 81)},
    {"title": "Advanced Specialization", "range": range(86, 92)},
    {"title": "Daily Discipline", "range": range(92, 98)},
    {"title": "Final Review & Exam", "range": range(98, 101)}
]

# Load Map
with open('curriculum_map.json', 'r', encoding='utf-8') as f:
    curriculum = json.load(f)

# Build JS Object
js_sections = []
processed_days = set()

for sec in SECTIONS:
    items = []
    days = []
    if "range" in sec:
        days = list(sec["range"])
    if "days" in sec:
        days = sec["days"]
        
    for d in days:
        d_str = str(d)
        if d_str in curriculum:
            info = curriculum[d_str]
            # Use Topic from map, Path relative to index
            # relPath in map is "lessons/01.../Day.html" which is correct for index.html
            item = {
                "text": info['topic'],
                "lesson": info['relPath']
            }
            items.append(item)
            processed_days.add(d)
        else:
            print(f"Warning: Day {d} not found in map.")
            
    js_sections.append({
        "title": sec["title"],
        "items": items
    })

# Verify all days covered
all_days = set(map(int, curriculum.keys()))
missing = all_days - processed_days
if missing:
    print(f"WARNING: Days not assigned to any section: {sorted(list(missing))}")

# Generate JS String
js_str = "    const curriculum = [\n"
for sec in js_sections:
    js_str += f'      {{ title: "{sec["title"]}", items: ['
    for item in sec["items"]:
        # Escape quotes in text just in case
        text = item["text"].replace('"', '\\"')
        js_str += f'{{ text: "{text}", lesson: "{item["lesson"]}" }}, '
    js_str += '] },\n'
js_str += "    ];"

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace curriculum const
# Regex to find "const curriculum = [ ... ];"
# Use DOTALL
new_content = re.sub(
    r'const curriculum = \[.*?\];', 
    js_str, 
    content, 
    flags=re.DOTALL
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("index.html updated.")
