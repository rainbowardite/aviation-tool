@echo off

::python -m PyInstaller --noconsole--onefile .\aviation-tool.py

python -m PyInstaller .\aviation-tool.spec

pause
