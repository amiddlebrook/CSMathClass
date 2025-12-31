try {
    $audit = Import-Csv "day_audit.csv"
    Write-Host "Loaded $($audit.Count) rows."

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

    $destBase = Join-Path (Get-Location).Path "lessons_reorg"
    if (Test-Path $destBase) { Remove-Item $destBase -Recurse -Force }
    New-Item -ItemType Directory -Path $destBase | Out-Null
    Write-Host "Created $destBase"

    foreach ($row in $audit) {
        if ($row.Source -eq "None") { continue }
        $d = [int]$row.DayNum
        $word = $words[$d]
        if (-not $word) { continue }

        $folderName = "99-misc"
        if ($d -le 6) { $folderName = "01-operating-system" }
        elseif ($d -le 10) { $folderName = "02-precalculus" }
        elseif ($d -le 18) { $folderName = "03-calculus" }
        elseif ($d -le 27) { $folderName = "04-linear-algebra" }
        elseif ($d -le 37) { $folderName = "05-discrete-math" }
        elseif ($d -le 48) { $folderName = "06-algorithms" }
        elseif ($d -le 54) { $folderName = "07-probability-stats" }
        elseif ($d -le 63) { $folderName = "08-analysis" }
        elseif ($d -le 67) { $folderName = "09-numerical" }
        elseif ($d -le 76) { $folderName = "10-topology-measure" }
        elseif ($d -le 85) { $folderName = "11-functional-pde" }
        elseif ($d -le 91) { $folderName = "12-theoretical-cs" }
        elseif ($d -le 97) { $folderName = "13-optimization" }
        elseif ($d -eq 98) { $folderName = "98-review" }
        elseif ($d -ge 99) { $folderName = "99-tests" }

        $destDir = Join-Path $destBase $folderName
        if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir | Out-Null }

        $destFileName = "Day$($word).html"
        $destPath = Join-Path $destDir $destFileName

        if (Test-Path $destPath) {
            Write-Host "Duplicate Day $d from $($row.Path)"
            $destPath = Join-Path $destDir "Day$($word)_Duplicate.html"
        }

        Copy-Item -LiteralPath $row.Path -Destination $destPath
    }
    Write-Host "Done."
}
catch {
    Write-Error $_
}
