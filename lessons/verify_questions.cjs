// Simple verification script for questions-data.js
const path = require('path');

try {
    // Test if we can load the questions data
    const dataPath = path.join(__dirname, 'questions-data.js');
    const questionsData = require(dataPath);

    // Check day9 and day10
    const day9 = questionsData.day9 || [];
    const day10 = questionsData.day10 || [];

    console.log('=== Questions Data Verification ===');
    console.log(`Day 9: ${day9.length} questions`);
    console.log(`Day 10: ${day10.length} questions`);

    // Count generate functions
    const day9Gen = day9.filter(q => typeof q.generate === 'function').length;
    const day10Gen = day10.filter(q => typeof q.generate === 'function').length;

    console.log(`Day 9 with generate: ${day9Gen}/${day9.length}`);
    console.log(`Day 10 with generate: ${day10Gen}/${day10.length}`);

    // Test a generate function
    if (day9[12] && typeof day9[12].generate === 'function') {
        console.log('\nTest Day 9 Q13 generate:');
        const result = day9[12].generate();
        console.log('  Prompt:', result.prompt);
        console.log('  Answer:', result.answer);
    }

    console.log('\n✅ questions-data.js is valid!');
} catch (e) {
    console.error('❌ Error:', e.message);
    console.error(e.stack);
    process.exit(1);
}
