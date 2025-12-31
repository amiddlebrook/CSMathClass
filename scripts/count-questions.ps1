$filePath = "c:\Users\avery\Desktop\Free CS Math\CSMathClass\lessons\questions-data.js"
$lines = Get-Content -Path $filePath

$currentDay = $null
$dayCounts = @{}

foreach ($line in $lines) {
    if ($line -match '"day(\d+)": \[') {
        $currentDay = $Matches[1]
        $dayCounts[$currentDay] = 0
    }
    elseif ($currentDay -ne $null -and $line -match '"prompt":') {
        $dayCounts[$currentDay]++
    }
}

Write-Host "Day,Count"
for ($i = 1; $i -le 100; $i++) {
    $count = $dayCounts["$i"]
    if ($null -eq $count) { $count = 0 }
    Write-Host "$i,$count"
}
