const fs = require('fs');
const path = require('path');

const rootDir = "c:\\Users\\avery\\Desktop\\Free CS Math\\CSMathClass\\lessons";
const files = [];

function scan(dir) {
    if (!fs.existsSync(dir)) return;
    const items = fs.readdirSync(dir);
    items.forEach(item => {
        const fullPath = path.join(dir, item);
        const stat = fs.statSync(fullPath);
        if (stat.isDirectory()) {
            if (item !== 'node_modules' && item !== '.git') scan(fullPath);
        } else if (item.endsWith('.html') && !item.includes('index.html')) {
            files.push(fullPath);
        }
    });
}

scan(rootDir);

// Map: DayNum -> { path, title, topic }
const curriculum = {};
const numToWord = {
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
};

// Inverse map
const wordToNum = {};
for (let n in numToWord) wordToNum[numToWord[n]] = parseInt(n);

try {
    console.log("Starting map generation...");
    scan(rootDir);
    console.log(`Scanned ${files.length} files.`);

    files.forEach(f => {
        const filename = path.basename(f); // DayOne.html
        const namePart = filename.replace('Day', '').replace('.html', '').replace('_Duplicate', '');
        const num = wordToNum[namePart];

        if (num) {
            // Read content to get Title Topic
            const content = fs.readFileSync(f, 'utf8');
            // Extract strictly from Hero Label as truth
            const heroMatch = content.match(/Day\s+(\d+)\s*[·:]\s*([^<]+)/);
            let topic = "Unknown";
            if (heroMatch) {
                topic = heroMatch[2].trim();
            }

            curriculum[num] = {
                day: num,
                path: f,
                relPath: path.relative("c:\\Users\\avery\\Desktop\\Free CS Math\\CSMathClass", f).replace(/\\/g, '/'),
                topic: topic,
                filename: filename
            };
        }
    });

    fs.writeFileSync('curriculum_map.json', JSON.stringify(curriculum, null, 2));
    console.log(`Mapped ${Object.keys(curriculum).length} lessons.`);
} catch (err) {
    console.error("FATAL ERROR:", err.message);
    console.error(err.stack);
}
