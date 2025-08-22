@echo off
:: Launch main.py with admin privileges
powershell -Command "Start-Process python -ArgumentList '\"%~dp0main.py\"' -Verb RunAs"
