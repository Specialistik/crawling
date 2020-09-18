pyinstaller -F main.py
move dist\main.exe .
rd /S /Q __pycache__
rd /S /Q build
rd /S /Q dist
del /S /Q main.spec