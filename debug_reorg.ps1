try {
    Write-Host "Reading CSV from day_audit.csv"
    $audit = Import-Csv "day_audit.csv"
    Write-Host "Count: $($audit.Count)"
    if ($audit.Count -gt 0) {
        $first = $audit[0]
        Write-Host "First Path: $($first.Path)"
        Write-Host "First Day: $($first.DayNum)"
    }
}
catch {
    Write-Error $_
}
