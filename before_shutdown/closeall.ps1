
# List the names of processes to be stopped
$processesToStop = Get-Process | Where-Object { 
    $_.MainWindowTitle -ne "" -and
    $_.MainWindowTitle -notlike "*closeall.ps1*" -and
    $_.MainWindowTitle -notlike "*BeforeShutdown*"
}

# Display the processes
Write-Output "Processes to be stopped:"
$processesToStop | ForEach-Object {
    Write-Output "Name: $($_.ProcessName), PID: $($_.Id), Title: $($_.MainWindowTitle)"
}

$processesToStop | Stop-Process -Force -ErrorAction SilentlyContinue

# Return success code
return 0