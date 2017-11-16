Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
choco install -y python
Write-Host "Python version:"
python --version
pip install psutil python-dateutil applicationinsights
Write-Host "Downloading nodestats.py"
Invoke-WebRequest https://raw.githubusercontent.com/timotheeguerin/batch-insights/master/nodestats.py -OutFile nodestats.py
start-job { python nodestats.py > node-stats.log 2>&1 }