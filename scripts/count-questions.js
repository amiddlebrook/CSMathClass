const fs = require('fs');
const path = require('path');

const questionsDataPath = path.resolve('c:/Users/avery/Desktop/Free CS Math/CSMathClass/lessons/questions-data.js');

console.log('Reading file: ' + questionsDataPath);

try {
    const content = fs.readFileSync(questionsDataPath, 'utf8');
    console.log('File read successfully. Size: ' + content.length);

    const counts = {};
    for (let i = 1; i <= 100; i++) {
        const dayKey = 'day' + i;
        const startMarker = "'" + dayKey + "': [";
        const startMarkerAlt = '"' + dayKey + '": [';

        let startIdx = content.indexOf(startMarker);
        if (startIdx === -1) startIdx = content.indexOf(startMarkerAlt);

        if (startIdx !== -1) {
            let pos = startIdx + startMarker.length;
            let bracketCount = 1;
            let questionCount = 0;
            let inObject = false;

            while (bracketCount > 0 && pos < content.length) {
                if (content[pos] === '{' && !inObject) {
                    inObject = true;
                    questionCount++;
                } else if (content[pos] === '}') {
                    inObject = false;
                } else if (content[pos] === '[') {
                    bracketCount++;
                } else if (content[pos] === ']') {
                    bracketCount--;
                }
                pos++;
            }
            counts[i] = questionCount;
        } else {
            counts[i] = 0;
        }
    }

    console.log('Day,Count');
    for (let i = 1; i <= 100; i++) {
        console.log(i + ',' + counts[i]);
    }
} catch (err) {
    console.error('ERROR:');
    console.error(err);
}
