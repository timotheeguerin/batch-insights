set -e
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python get-pip.py
echo "Python version:"
python --version
echo "Pip version:"
pip --version

wget --no-cache https://raw.githubusercontent.com/timotheeguerin/batch-insights/master/nodestats.py
python nodestats.py > node-stats.log 2>&1 &