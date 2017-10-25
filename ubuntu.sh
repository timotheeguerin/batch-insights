set -e

apt-get install -y python-pip
pip install psutil python-dateutil applicationinsights
wget --no-cache https://raw.githubusercontent.com/timotheeguerin/batch-insights/master/nodestats.py
python nodestats.py &