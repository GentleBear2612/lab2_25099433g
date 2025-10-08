$python = 'C:\Users\admin\AppData\Local\Programs\Python\Python313\python.exe'
$script = 'd:\lab2_25099433g\src\main.py'

Write-Host "Looking for running processes with main.py in command line..."
$procs = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -and ($_.CommandLine -like '*main.py*' -or $_.CommandLine -like '*src\\main.py*') }

if ($procs) {
    foreach ($p in $procs) {
        Write-Host "Stopping PID $($p.ProcessId) : $($p.CommandLine)"
        try { Stop-Process -Id $p.ProcessId -Force -ErrorAction Stop } catch { Write-Host "Failed to stop PID $($p.ProcessId): $_" }
    }
} else {
    Write-Host 'No running main.py processes found'
}

Write-Host "Starting Flask app with: $python $script"
Start-Process -FilePath $python -ArgumentList $script -WindowStyle Normal
Write-Host 'Started. Check new window or use tasklist/Get-NetTCPConnection to verify.'
