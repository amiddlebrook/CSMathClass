const fs = require('fs');
const path = require('path');
// Cheerio removed to avoid dependency issues

// If cheerio isn't available, we'll try-catch or just use regex.
// Regex is safer for a standard environment without checking package.json
function extractInfo(content) {
    const titleMatch = content.match(/<title>(.*?)<\/title>/);
    const title = titleMatch ? titleMatch[1] : 'No Title';

    // Hero label often has "Day X · Topic"
    // <div class="hero-label">...Day 14 · Probability...</div>
    const heroLabelMatch = content.match(/<div class="hero-label">([\s\S]*?)<\/div>/);
    let heroLabel = 'No Hero Label';
    if (heroLabelMatch) {
        // strip tags if any nested
        heroLabel = heroLabelMatch[1].replace(/<[^>]*>/g, '').trim().replace(/\s+/g, ' ');
    }

    const sectionMatch = content.match(/<h2 class="section-title">(.*?)<\/h2>/);
    const firstSection = sectionMatch ? sectionMatch[1] : 'No Section';

    return { title, heroLabel, firstSection };
}

function scanDir(dir, fileList = []) {
    const files = fs.readdirSync(dir);

    files.forEach(file => {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);

        if (stat.isDirectory()) {
            if (file !== 'node_modules' && file !== '.git') {
                scanDir(filePath, fileList);
            }
        } else if (file.endsWith('.html') && !file.includes('index.html') && !file.includes('analytics.html') && !file.includes('compare.html')) {
            fileList.push(filePath);
        }
    });

    return fileList;
}

const rootDir = "c:\\Users\\avery\\Desktop\\Free CS Math\\CSMathClass\\lessons";
const allFiles = scanDir(rootDir);

const results = [];

allFiles.forEach(file => {
    try {
        const content = fs.readFileSync(file, 'utf8');
        const info = extractInfo(content);
        results.push({
            path: file,
            fileName: path.basename(file),
            ...info
        });
    } catch (e) {
        console.error(`Error reading ${file}:`, e);
    }
});

// Sort by path for readability
results.sort((a, b) => a.path.localeCompare(b.path));

console.log(JSON.stringify(results, null, 2));

const outputPath = path.join(__dirname, 'curriculum_audit.json');
fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
console.log(`Saved audit to ${outputPath}`);
