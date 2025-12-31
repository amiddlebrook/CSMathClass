$targets = @("9", "10", "18", "98", "99", "100")
$csv = Import-Csv "day_audit.csv"
foreach ($row in $csv) {
    if ($targets -contains $row.DayNum) {
        Write-Host "Found Day $($row.DayNum): $($row.Path)"
    }
}
