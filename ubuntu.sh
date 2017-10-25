set -e

apt-get update
apt-get -y install python-pip
pip install psutil python-dateutil applicationinsights
wget --no-cache https://raw.githubusercontent.com/timotheeguerin/batch-insights/master/nodestats.py
python nodestats.py > node-stats.log &