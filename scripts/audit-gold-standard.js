const fs = require('fs');
const path = require('path');

const lessonsDir = 'c:\\Users\\avery\\Desktop\\Free CS Math\\CSMathClass\\lessons';

// Find all HTML files
function findHtmlFiles(dir, files = []) {
    const items = fs.readdirSync(dir);
    for (const item of items) {
        const fullPath = path.join(dir, item);
        const stat = fs.statSync(fullPath);
        if (stat.isDirectory() && !item.startsWith('.')) {
            findHtmlFiles(fullPath, files);
        } else if (item.endsWith('.html') && item.startsWith('Day')) {
            files.push(fullPath);
        }
    }
    return files;
}

const htmlFiles = findHtmlFiles(lessonsDir);

console.log('File,Lines,HasHeroMeta,HasTOC,InfoBlocks,CodeBlocks,VideoCount,HasQuizSection');

htmlFiles.forEach(file => {
    try {
        const content = fs.readFileSync(file, 'utf8');
        const lines = content.split('\n').length;

        // Check for hero-meta
        const hasHeroMeta = content.includes('hero-meta') || content.includes('meta-item');

        // Check for TOC
        const hasTOC = content.includes('toc-list') || content.includes('toc-link');

        // Count info blocks (analogies)
        const infoBlocks = (content.match(/<div class="info">/g) || []).length;

        // Count code blocks
        const codeBlocks = (content.match(/<pre class="code-block">/g) || []).length +
            (content.match(/<code class/g) || []).length;

        // Count video references
        const videoCount = (content.match(/vid:\s*["'][^"']+["']/g) || []).length +
            (content.match(/youtube\.com/g) || []).length;

        // Has quiz section
        const hasQuiz = content.includes('quizContainer') || content.includes('initQuiz');

        const basename = path.basename(file);
        console.log(`${basename},${lines},${hasHeroMeta},${hasTOC},${infoBlocks},${codeBlocks},${videoCount},${hasQuiz}`);
    } catch (err) {
        console.error(`Error reading ${file}: ${err.message}`);
    }
});
