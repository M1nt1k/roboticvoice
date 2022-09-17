@echo off
echo start setup python packages
py -m pip install --upgrade pip
py -m pip install -r .venv\req.txt
echo complete
pause