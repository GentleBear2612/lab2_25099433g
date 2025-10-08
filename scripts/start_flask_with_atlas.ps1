# Set Atlas URI in this PowerShell session and restart Flask, then run checks
$env:MONGO_URI = 'mongodb+srv://zmhlele:zmhlele@cluster0.kskvhe8.mongodb.net/?retryWrites=true&w=majority'
$env:MONGO_DB_NAME = 'notetaker_db'
Write-Host 'Session env set: MONGO_URI and MONGO_DB_NAME'

# Stop any running main.py processes
$procs = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -and ($_.CommandLine -like '*main.py*' -or $_.CommandLine -like '*src\\main.py*') }
if ($procs) {
    foreach ($p in $procs) {
        Write-Host "Stopping PID $($p.ProcessId) : $($p.CommandLine)"
        try { Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue } catch { Write-Host "Failed to stop $($p.ProcessId): $_" }
    }
} else {
    Write-Host 'No running main.py processes found'
}

# Start Flask in a child process that inherits this session's env
$python = 'C:\\Users\\admin\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
$script = 'd:\\lab2_25099433g\\src\\main.py'
Write-Host "Starting Flask with $python $script"
$proc = Start-Process -FilePath $python -ArgumentList $script -PassThru
Write-Host "Started Flask PID: $($proc.Id)"

Start-Sleep -Seconds 3

# Run check scripts
Write-Host 'Running check_mongo_uri.py'
& $python 'd:/lab2_25099433g/scripts/check_mongo_uri.py'
Write-Host 'Running list_mongo_notes.py'
& $python 'd:/lab2_25099433g/scripts/list_mongo_notes.py'
