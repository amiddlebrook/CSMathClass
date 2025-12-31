# reorg.ps1
$audit = Import-Csv "day_audit.csv"

# Function to convert number to word (1-100)
function Get-DayWord {
    param ([int]$num)
    $words = @{
        1 = "One"; 2 = "Two"; 3 = "Three"; 4 = "Four"; 5 = "Five"; 6 = "Six"; 7 = "Seven"; 8 = "Eight"; 9 = "Nine"; 10 = "Ten";
        11 = "Eleven"; 12 = "Twelve"; 13 = "Thirteen"; 14 = "Fourteen"; 15 = "Fifteen"; 16 = "Sixteen"; 17 = "Seventeen"; 18 = "Eighteen"; 19 = "Nineteen"; 20 = "Twenty";
        21 = "TwentyOne"; 22 = "TwentyTwo"; 23 = "TwentyThree"; 24 = "TwentyFour"; 25 = "TwentyFive"; 26 = "TwentySix"; 27 = "TwentySeven"; 28 = "TwentyEight"; 29 = "TwentyNine"; 30 = "Thirty";
        31 = "ThirtyOne"; 32 = "ThirtyTwo"; 33 = "ThirtyThree"; 34 = "ThirtyFour"; 35 = "ThirtyFive"; 36 = "ThirtySix"; 37 = "ThirtySeven"; 38 = "ThirtyEight"; 39 = "ThirtyNine"; 40 = "Forty";
        41 = "FortyOne"; 42 = "FortyTwo"; 43 = "FortyThree"; 44 = "FortyFour"; 45 = "FortyFive"; 46 = "FortySix"; 47 = "FortySeven"; 48 = "FortyEight"; 49 = "FortyNine"; 50 = "Fifty";
        51 = "FiftyOne"; 52 = "FiftyTwo"; 53 = "FiftyThree"; 54 = "FiftyFour"; 55 = "FiftyFive"; 56 = "FiftySix"; 57 = "FiftySeven"; 58 = "FiftyEight"; 59 = "FiftyNine"; 60 = "Sixty";
        61 = "SixtyOne"; 62 = "SixtyTwo"; 63 = "SixtyThree"; 64 = "SixtyFour"; 65 = "SixtyFive"; 66 = "SixtySix"; 67 = "SixtySeven"; 68 = "SixtyEight"; 69 = "SixtyNine"; 70 = "Seventy";
        71 = "SeventyOne"; 72 = "SeventyTwo"; 73 = "SeventyThree"; 74 = "SeventyFour"; 75 = "SeventyFive"; 76 = "SeventySix"; 77 = "SeventySeven"; 78 = "SeventyEight"; 79 = "SeventyNine"; 80 = "Eighty";
        81 = "EightyOne"; 82 = "EightyTwo"; 83 = "EightyThree"; 84 = "EightyFour"; 85 = "EightyFive"; 86 = "EightySix"; 87 = "EightySeven"; 88 = "EightyEight"; 89 = "EightyNine"; 90 = "Ninety";
        91 = "NinetyOne"; 92 = "NinetyTwo"; 93 = "NinetyThree"; 94 = "NinetyFour"; 95 = "NinetyFive"; 96 = "NinetySix"; 97 = "NinetySeven"; 98 = "NinetyEight"; 99 = "NinetyNine"; 100 = "OneHundred"
    }
    return $words[$num]
}

# Determine target folder based on Day Number (Standard Ranges)
function Get-TargetFolder {
    param ([int]$d)
    if ($d -le 6) { return "01-operating-system" }
    if ($d -le 10) { return "02-precalculus" }
    if ($d -le 18) { return "03-calculus" }
    if ($d -le 27) { return "04-linear-algebra" }
    if ($d -le 37) { return "05-discrete-math" }
    if ($d -le 48) { return "06-algorithms" }
    if ($d -le 54) { return "07-probability-stats" }
    if ($d -le 63) { return "08-analysis" }
    if ($d -le 67) { return "09-numerical" }
    if ($d -le 76) { return "10-topology-measure" }
    if ($d -le 85) { return "11-functional-pde" } # Adjusted logic?
    if ($d -le 91) { return "12-theoretical-cs" } # Using existing folders for now
    if ($d -le 97) { return "13-optimization" }
    if ($d -eq 98) { return "98-review" }
    if ($d -ge 99) { return "99-tests" }
    return "99-misc"
}

$destBase = Join-Path (Get-Location).Path "lessons_reorg"
Write-Host "Destination Base: $destBase"
if (Test-Path $destBase) { Remove-Item $destBase -Recurse -Force }
New-Item -ItemType Directory -Path $destBase | Out-Null

foreach ($row in $audit) {
    if ($row.Source -eq "None") { continue } # Skip unknown
    $d = [int]$row.DayNum
    $word = Get-DayWord $d
    if (-not $word) { Write-Host "Skipping unknown day $d"; continue }
    
    $folder = Get-TargetFolder $d
    $destDir = Join-Path $destBase $folder
    if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir | Out-Null }
    
    $destFile = Join-Path $destDir "Day$($word).html"
    
    # Handle Duplicates: If file exists, append _v2
    if (Test-Path $destFile) {
        Write-Host "Duplicate found for Day $d: $($row.Path)"
        $destFile = Join-Path $destDir "Day$($word)_Duplicate.html"
    }
    
    Copy-Item $row.Path -Destination $destFile
    Write-Host "Copied Day $d to $destFile"
}
