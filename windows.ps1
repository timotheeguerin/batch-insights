Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
choco install -y python
python --version
pip install psutil python-dateutil applicationinsights
Invoke-WebRequest --no-cache https://raw.githubusercontent.com/timotheeguerin/batch-insights/master/nodestats.py
start-job { python nodestats.py > node-stats.log 2>&1 }