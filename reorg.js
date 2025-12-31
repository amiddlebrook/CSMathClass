const fs = require('fs');
const path = require('path');
const csv = require('fs').readFileSync('day_audit.csv', 'utf8');

const rows = csv.split('\n').slice(1).map(line => {
    // Cleaner parsing for "Path","Name","Num","Source" structure
    const cleaned = line.replace(/^"|"$/g, ''); // Remove start/end quotes
    const parts = cleaned.split('","'); // Split by delimiter

    if (parts.length < 3) return null;

    return { Path: parts[0], FileName: parts[1], DayNum: parseInt(parts[2]) };
}).filter(r => r && r.DayNum);

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

function getTargetFolder(d) {
    if (d <= 6) return "01-operating-system";
    if (d <= 10) return "02-precalculus";
    if (d <= 18) return "03-calculus"; // Keep as generic bucket, even if mixed content
    if (d <= 27) return "04-linear-algebra";
    if (d <= 37) return "05-discrete-math";
    if (d <= 48) return "06-algorithms";
    if (d <= 54) return "07-probability-stats";
    if (d <= 63) return "08-analysis";
    if (d <= 67) return "09-numerical";
    if (d <= 76) return "10-topology-measure";
    if (d <= 85) return "11-functional-pde";
    if (d <= 91) return "12-theoretical-cs";
    if (d <= 97) return "13-optimization";
    if (d === 98) return "98-review";
    if (d >= 99) return "99-tests";
    return "99-misc";
}

const destBase = path.join(__dirname, 'lessons_reorg');
if (fs.existsSync(destBase)) fs.rmSync(destBase, { recursive: true, force: true });
fs.mkdirSync(destBase);

rows.forEach(row => {
    const d = row.DayNum;
    const word = numToWord[d];
    if (!word) {
        console.log(`Skipping unknown Day ${d}`);
        return;
    }

    // Determine Target
    const folder = getTargetFolder(d);
    const folderPath = path.join(destBase, folder);
    if (!fs.existsSync(folderPath)) fs.mkdirSync(folderPath);

    let destFile = path.join(folderPath, `Day${word}.html`);
    if (fs.existsSync(destFile)) {
        console.log(`Duplicate Day ${d}: ${row.Path}`);
        destFile = path.join(folderPath, `Day${word}_Duplicate.html`);
    }

    try {
        fs.copyFileSync(row.Path, destFile);
        console.log(`Copied Day ${d} to ${destFile}`);
    } catch (e) {
        console.error(`Error copying ${row.Path}: ${e.message}`);
    }
});
