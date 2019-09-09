@echo off
git pull
start "" http://localhost:8000
python SiteGenerator.py %*
pause
