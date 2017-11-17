# iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
# choco install -y python
# Write-Host "Python version:"
# python --version
# pip install psutil python-dateutil applicationinsights
# Write-Host "Downloading nodestats.py"
Invoke-WebRequest https://raw.githubusercontent.com/timotheeguerin/batch-insights/master/nodestats.py -OutFile nodestats.py
Write-Host "Starting background process in $env:AZ_BATCH_TASK_WORKING_DIR"

Start-Process python -ArgumentList .\nodestats.py  -RedirectStandardOutput .\node-stats.log -RedirectStandardError .\node-stats.err.log -WindowStyle Hidden -Credential 'NT AUTHORITY\SYSTEM'
# start cmd /C "python .\nodestats.py > .\node-stats.log 2>&1"

# python .\nodestats.py *>> .\node-stats.log
# $action = New-ScheduledTaskAction -WorkingDirectory $env:AZ_BATCH_TASK_WORKING_DIR -Execute 'Powershell.exe' -Argument "python .\nodestats.py > .\node-stats.log 2>&1" ; 
# $principal = New-ScheduledTaskPrincipal -UserID 'NT AUTHORITY\SYSTEM' -LogonType ServiceAccount -RunLevel Highest ; 
# Register-ScheduledTask -Action $action -Principal $principal -TaskName "batchappinsights" -Force ; 
# Start-ScheduledTask -TaskName "batchappinsights"; 
# Get-ScheduledTask -TaskName "batchappinsights";