import os
import re
from bs4 import BeautifulSoup
import csv

LESSONS_DIR = r"c:\Users\avery\Desktop\CSMathClass\CSMathClass\lessons"

def analyze_lesson(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Get text content from main content area only to avoid nav/sidebar noise
            main_content = soup.find('main', class_='content')
            if main_content:
                text = main_content.get_text(separator=' ', strip=True)
                word_count = len(text.split())
            else:
                word_count = 0
            
            # Math blocks (both div.math-block and inline `...`)
            # Note: BeautifulSoup get_text might strip some delimiters, so we look at raw html for regex
            math_blocks = len(soup.find_all(class_='math-block'))
            inline_math = len(re.findall(r'`[^`]+`', content))
            
            # Code blocks
            code_blocks = len(soup.find_all('pre'))
            
            # Sections
            sections = len(soup.find_all('section'))
            
            # Quiz Questions (Looking for JS array)
            quiz_count = 0
            script_content = ""
            for script in soup.find_all('script'):
                if script.string:
                    script_content += script.string
            
            # Regex to find JSON-like array size for QUESTIONS
            matches = re.findall(r'const\s+QUESTIONS\s*=\s*(\[.*?\]);', script_content, re.DOTALL)
            if matches:
                # Rough estimate of items in the array string
                quiz_count = matches[0].count('{')

            return {
                "file": os.path.basename(file_path),
                "path": file_path,
                "word_count": word_count,
                "math_blocks": math_blocks,
                "inline_math": inline_math,
                "code_blocks": code_blocks,
                "sections": sections,
                "quiz_count": quiz_count
            }
    except Exception as e:
        return {"file": os.path.basename(file_path), "error": str(e)}

results = []
for root, dirs, files in os.walk(LESSONS_DIR):
    for file in files:
        if file.endswith(".html") and "Day" in file:
            full_path = os.path.join(root, file)
            results.append(analyze_lesson(full_path))

# Sort by Day number? Or just Section?
# Let's simple print the "Thin" ones first (low word count)

import json

# ... (keep existing analysis logic) ...

with open('audit_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"Exported {len(results)} records to audit_results.json")

# Print summary to console
thin_lessons = [r for r in results if r.get('word_count', 0) < 600]
print(f"Found {len(thin_lessons)} lessons under 600 words.")

