/**
 * Video Availability Audit Script
 * 
 * Checks all lesson files for video IDs and validates them by checking
 * if the YouTube thumbnail is accessible. A valid video ID should have
 * an accessible thumbnail at https://img.youtube.com/vi/{VIDEO_ID}/0.jpg
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const LESSONS_DIR = __dirname;

// Find all HTML lesson files
function findLessonFiles(dir) {
    const lessons = [];
    const entries = fs.readdirSync(dir, { withFileTypes: true });

    for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory() && !entry.name.startsWith('.')) {
            // Recursively search subdirectories
            const htmlFiles = fs.readdirSync(fullPath)
                .filter(f => f.endsWith('.html') && f.startsWith('Day'));
            for (const htmlFile of htmlFiles) {
                lessons.push({
                    dir: entry.name,
                    file: htmlFile,
                    path: path.join(fullPath, htmlFile)
                });
            }
        }
    }

    return lessons;
}

// Extract video IDs from an HTML file
function extractVideoIds(filePath) {
    const content = fs.readFileSync(filePath, 'utf-8');

    // Match video IDs in VIDEO_GROUPS array
    const vidMatches = content.matchAll(/vid:\s*["']([a-zA-Z0-9_-]{11})["']/g);
    const videoIds = [];

    for (const match of vidMatches) {
        videoIds.push(match[1]);
    }

    return videoIds;
}

// Check if a YouTube video is available by checking its thumbnail
function checkVideoAvailability(videoId) {
    return new Promise((resolve) => {
        const url = `https://img.youtube.com/vi/${videoId}/0.jpg`;

        https.get(url, (response) => {
            // Check if we got a valid thumbnail (not the "no video" placeholder)
            // YouTube returns a 120x90 gray placeholder for unavailable videos
            if (response.statusCode === 200) {
                let size = 0;
                response.on('data', (chunk) => {
                    size += chunk.length;
                });
                response.on('end', () => {
                    // Unavailable video thumbnails are typically very small (~1.5KB)
                    // Valid thumbnails are usually 10KB+
                    resolve({
                        id: videoId,
                        available: size > 5000,
                        size: size,
                        status: response.statusCode
                    });
                });
            } else {
                resolve({
                    id: videoId,
                    available: false,
                    size: 0,
                    status: response.statusCode
                });
            }
        }).on('error', (err) => {
            resolve({
                id: videoId,
                available: false,
                error: err.message
            });
        });
    });
}

// Main audit function
async function auditVideos() {
    console.log('=== VIDEO AVAILABILITY AUDIT ===\n');

    const lessons = findLessonFiles(LESSONS_DIR);
    console.log(`Found ${lessons.length} lesson files\n`);

    const results = [];
    const unavailableVideos = [];

    for (const lesson of lessons) {
        const videoIds = extractVideoIds(lesson.path);

        if (videoIds.length === 0) {
            results.push({
                ...lesson,
                videoCount: 0,
                videos: [],
                issues: ['NO_VIDEOS']
            });
            continue;
        }

        const lessonResult = {
            ...lesson,
            videoCount: videoIds.length,
            videos: [],
            issues: []
        };

        // Check each video
        for (const vid of videoIds) {
            const check = await checkVideoAvailability(vid);
            lessonResult.videos.push(check);

            if (!check.available) {
                unavailableVideos.push({
                    lesson: lesson.file,
                    dir: lesson.dir,
                    videoId: vid,
                    reason: check.error || 'Thumbnail too small (likely unavailable)'
                });
            }
        }

        const unavailableCount = lessonResult.videos.filter(v => !v.available).length;
        if (unavailableCount > 0) {
            lessonResult.issues.push(`UNAVAILABLE_VIDEOS: ${unavailableCount}/${videoIds.length}`);
        }

        results.push(lessonResult);
    }

    // Print summary
    console.log('\n=== SUMMARY ===\n');

    const lessonsWithIssues = results.filter(r => r.issues.length > 0);
    console.log(`Total lessons: ${results.length}`);
    console.log(`Lessons with video issues: ${lessonsWithIssues.length}`);
    console.log(`Total unavailable videos: ${unavailableVideos.length}\n`);

    if (unavailableVideos.length > 0) {
        console.log('=== UNAVAILABLE VIDEOS ===\n');
        for (const uv of unavailableVideos) {
            console.log(`${uv.dir}/${uv.lesson}:`);
            console.log(`  Video ID: ${uv.videoId}`);
            console.log(`  URL: https://www.youtube.com/watch?v=${uv.videoId}`);
            console.log(`  Reason: ${uv.reason}\n`);
        }
    }

    // Also save to JSON for reference
    const outputPath = path.join(LESSONS_DIR, 'video_audit_results.json');
    fs.writeFileSync(outputPath, JSON.stringify({
        timestamp: new Date().toISOString(),
        totalLessons: results.length,
        lessonsWithIssues: lessonsWithIssues.length,
        unavailableVideos: unavailableVideos,
        details: results.filter(r => r.issues.length > 0)
    }, null, 2));

    console.log(`\nDetailed results saved to: ${outputPath}`);

    return { results, unavailableVideos };
}

// Run the audit
auditVideos().catch(console.error);
