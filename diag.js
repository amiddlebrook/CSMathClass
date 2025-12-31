const fs = require('fs');
const path = require('path');
console.log("Starting diag...");
try {
    const root = "c:\\Users\\avery\\Desktop\\Free CS Math\\CSMathClass\\lessons";
    console.log("Checking root:", root);
    if (fs.existsSync(root)) {
        console.log("Root exists.");
        const files = fs.readdirSync(root);
        console.log("Files:", files.slice(0, 5));
    } else {
        console.error("Root does not exist!");
    }
} catch (e) {
    console.error("Error:", e);
}
