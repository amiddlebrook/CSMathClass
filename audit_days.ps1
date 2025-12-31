$files = Get-ChildItem -Recurse -Filter "*.html" -Path ".\lessons"
$results = @()

foreach ($file in $files) {
    if ($file.Name -like "*index.html*" -or $file.Name -like "*analytics.html*" -or $file.Name -like "*compare.html*") { continue }
    
    $content = Get-Content $file.FullName -Raw
    # Match "Day X" inside the hero label or title. 
    # Logic: Look for "Day X" followed by a dot, colon, or just a space/tab.
    # Stricter match: Only allow the interpunct "·" which is used in the Hero Label.
    # The Title uses ":" (e.g. "Day 12: Limits"), which is stale.
    if ($content -match "Day\s+(\d+)\s*·") {
        $dayNum = $matches[1]
        $results += [PSCustomObject]@{
            Path = $file.FullName
            FileName = $file.Name
            DayNum = [int]$dayNum
            Source = "Hero"
        }
    } else {
        # Fallback: If no Hero match, log it but don't trust title blindly.
        $results += [PSCustomObject]@{
            Path = $file.FullName
            FileName = $file.Name
            DayNum = "Unknown"
            Source = "None"
        }
    }
}

$results | Sort-Object DayNum | Export-Csv -Path "day_audit.csv" -NoTypeInformation
Write-Host "Audit saved to day_audit.csv"
