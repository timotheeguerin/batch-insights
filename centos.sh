set -e
yum -y install gcc python-pip python-wheels python-dev

echo "Python version:"
python --version
echo "Pip version:"
pip --version
pip install psutil python-dateutil applicationinsights

wget --no-cache https://raw.githubusercontent.com/timotheeguerin/batch-insights/master/nodestats.py
python nodestats.py > node-stats.log 2>&1 &