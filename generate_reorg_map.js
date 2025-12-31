const fs = require('fs');
const path = require('path');

// Number to Word mapping for 1-100
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

function getNewPath(dayNum, topic) {
    const dayWord = numToWord[dayNum];
    if (!dayWord) return null;

    // Normalize topic to folder name
    let folder = '99-misc';
    const t = topic.toLowerCase();

    if (dayNum <= 6) folder = '01-operating-system';
    else if (dayNum <= 10) folder = '02-precalculus';
    else if (dayNum <= 18) folder = '03-calculus';
    else if (dayNum <= 27) folder = '04-linear-algebra';
    else if (dayNum <= 37) folder = '05-discrete-math';
    else if (dayNum <= 48) folder = '06-algorithms';
    else if (dayNum <= 54) folder = '07-probability-stats';
    else if (dayNum <= 63) folder = '08-analysis';
    else if (dayNum <= 67) folder = '09-numerical'; // Merged Abstract Algebra + Numerical? Checking old structure...
    // Actually, user said: "whatever is in the lesson currently is how sections... will be named"
    // So we should map topics to folders carefully based on the NEW content.

    // Let's rely on the TOPIC string for folder assignment if possible, or fall back to ranges.
    if (t.includes('operating system')) folder = '01-operating-system';
    else if (t.includes('precalculus')) folder = '02-precalculus';
    else if (t.includes('calculus') && !t.includes('multivariable')) folder = '03-calculus'; // Simple heuristic
    else if (t.includes('linear algebra')) folder = '04-linear-algebra';
    else if (t.includes('discrete')) folder = '05-discrete-math';
    else if (t.includes('algorithm')) folder = '06-algorithms';
    else if (t.includes('probability') || t.includes('statistics')) folder = '07-probability-stats';
    else if (t.includes('analysis')) folder = '08-analysis';
    else if (t.includes('abstract algebra') || t.includes('numerical')) folder = '09-numerical';
    else if (t.includes('topology') || t.includes('measure')) folder = '10-topology-measure';
    else if (t.includes('functional') || t.includes('pde')) folder = '11-functional-pde';
    else if (t.includes('theoretical')) folder = '12-theoretical-cs';
    else if (t.includes('optimization')) folder = '13-optimization';
    else if (t.includes('specialize') || t.includes('specialization')) folder = '14-specialize';
    else if (t.includes('discipline')) folder = '15-discipline';
    else if (dayNum === 98) folder = '98-review';
    else if (dayNum === 99) folder = '99-tests';
    else if (dayNum === 100) folder = '100-exam';

    return `lessons/${folder}/Day${dayWord}.html`;
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
const moves = [];

allFiles.forEach(file => {
    try {
        const content = fs.readFileSync(file, 'utf8');
        // Regex to find "Day X"
        const dayMatch = content.match(/Day\s+(\d+)\s*[·:]\s*([^<]+)/);
        // Matches "Day 14 · Probability" or "Day 14: Probability"

        if (dayMatch) {
            const dayNum = parseInt(dayMatch[1]);
            const topic = dayMatch[2].trim();
            const newRelPath = getNewPath(dayNum, topic);

            if (newRelPath) {
                const newAbsPath = path.join(path.dirname(rootDir), newRelPath.replace('lessons/', 'CSMathClass/lessons/')); // Fix path join logic
                // Actually rootDir is .../lessons.
                // newRelPath is lessons/folder/file.
                // We want to verify exact paths.

                const targetPath = path.join("c:\\Users\\avery\\Desktop\\Free CS Math\\CSMathClass", newRelPath);

                // Only move if different
                if (file.toLowerCase() !== targetPath.toLowerCase()) {
                    moves.push({
                        from: file,
                        to: targetPath,
                        day: dayNum,
                        topic: topic
                    });
                }
            }
        } else {
            console.log("No Day match for:", file);
        }
    } catch (e) {
        console.error(`Error reading ${file}:`, e);
    }
});

// Sort by Day Number
moves.sort((a, b) => a.day - b.day);

console.log(JSON.stringify(moves, null, 2));
const outputPath = path.join("c:\\Users\\avery\\Desktop\\Free CS Math\\CSMathClass", 'reorg_moves.json');
try {
    fs.writeFileSync(outputPath, JSON.stringify(moves, null, 2));
    console.log(`Saved ${moves.length} moves to ${outputPath}`);
} catch (err) {
    console.error('Error writing file:', err);
}
