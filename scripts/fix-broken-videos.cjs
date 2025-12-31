#!/usr/bin/env node
/**
 * Fix broken video IDs in lesson files.
 * Filters out obviously invalid YouTube IDs (like CSS class names that got mixed in).
 */

const fs = require('fs');
const path = require('path');
const glob = require('glob');

// Valid YouTube video ID pattern: 11 characters, alphanumeric + hyphen + underscore
const VALID_VID_REGEX = /^[a-zA-Z0-9_-]{10,12}$/;

// Obvious invalid IDs that got mixed in from HTML/CSS
const INVALID_IDS = [
    'btnCheckAll', 'btnRevealAll', 'btnClear', 'btnReset',
    'code-string', 'code-number', 'code-comment', 'code-keyword', 'code-function', 'code-header',
    'stats-label', 'stats-value', 'main-layout', 'themeToggle',
    'ytPlayer', 'videoTitle', 'videoMeta', 'videoList', 'quizContainer',
    'progressText', 'progressFill', 'statAttempted', 'statCorrect', 'statAccuracy',
    '3Blue1Brown', 'TrevTutor', 'Khan Academy' // Channel names are not IDs
];

function isValidVideoId(vid) {
    if (!vid || typeof vid !== 'string') return false;
    if (INVALID_IDS.includes(vid)) return false;
    if (!VALID_VID_REGEX.test(vid)) return false;
    // Additional heuristic: should not look like a CSS class
    if (vid.includes('-') && vid.length > 12) return false;
    return true;
}

function fixVideoGroups(content) {
    // Match VIDEO_GROUPS array
    const videoGroupsMatch = content.match(/const VIDEO_GROUPS = \[([\s\S]*?)\];/);
    if (!videoGroupsMatch) return { content, fixed: false };

    let groupsContent = videoGroupsMatch[1];
    let originalGroupsContent = groupsContent;

    // Find all vid: "xxx" entries
    const vidPattern = /\{\s*title:\s*"[^"]*",\s*channel:\s*"[^"]*",\s*vid:\s*"([^"]*)"\s*\}/g;

    let fixedItems = [];
    let removedCount = 0;
    let match;

    while ((match = vidPattern.exec(originalGroupsContent)) !== null) {
        const fullMatch = match[0];
        const vid = match[1];

        if (isValidVideoId(vid)) {
            fixedItems.push(fullMatch);
        } else {
            removedCount++;
            console.log(`  Removing invalid vid: "${vid}"`);
        }
    }

    if (removedCount === 0) return { content, fixed: false };

    // Rebuild the VIDEO_GROUPS with valid items only
    // This is a simplified approach - we'll just keep the first group with valid items
    const newContent = content.replace(
        /const VIDEO_GROUPS = \[([\s\S]*?)\];/,
        `const VIDEO_GROUPS = [
            {
                title: "Lesson Videos",
                items: [
                    ${fixedItems.slice(0, 6).join(',\n                    ')}
                ]
            }
        ];`
    );

    return { content: newContent, fixed: true, removedCount };
}

async function main() {
    const lessonsDir = path.join(__dirname, '..', 'lessons');
    const htmlFiles = glob.sync(path.join(lessonsDir, '**/*.html'));

    console.log(`Scanning ${htmlFiles.length} lesson files for broken video IDs...\n`);

    let totalFixed = 0;

    for (const file of htmlFiles) {
        const content = fs.readFileSync(file, 'utf-8');

        // Check if file has corrupted video IDs
        if (content.includes('vid: "btnCheckAll"') ||
            content.includes('vid: "code-string"') ||
            content.includes('vid: "stats-label"')) {

            console.log(`\nFixing: ${path.relative(lessonsDir, file)}`);
            const result = fixVideoGroups(content);

            if (result.fixed) {
                fs.writeFileSync(file, result.content);
                console.log(`  Removed ${result.removedCount} invalid video entries.`);
                totalFixed++;
            }
        }
    }

    console.log(`\n========================================`);
    console.log(`Fixed ${totalFixed} files with broken video IDs.`);
}

main().catch(console.error);
