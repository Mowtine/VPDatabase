@echo off
start "" http://localhost:8000
python SiteGenerator.py %*
pause
