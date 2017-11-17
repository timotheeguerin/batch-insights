# iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
# choco install -y python
# Write-Host "Python version:"
# python --version
# pip install psutil python-dateutil applicationinsights
# Write-Host "Downloading nodestats.py"
# Invoke-WebRequest https://raw.githubusercontent.com/timotheeguerin/batch-insights/master/nodestats.py -OutFile nodestats.py
# Write-Host "Starting background process in $env.AZ_BATCH_TASK_WORKING_DIR"

Start-Process python -ArgumentList .\nodestats.py -NoNewWindow  -RedirectStandardOutput .\node-stats.log -RedirectStandardError .\node-stats.err.log
