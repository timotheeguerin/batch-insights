# batch-insights

## Usage
Set an environment variable called `APP_INSIGHT_KEY` in your start task with your app insight instrumentation key

### Ubuntu
Add this command in your start task commandLine
```bash
/bin/bash -c 'wget  -O - https://raw.githubusercontent.com/timotheeguerin/batch-insights/master/ubuntu.sh | bash'
```