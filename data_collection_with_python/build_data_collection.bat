@echo off
cd %localhost%
Title Building .exe...  
pyinstaller --onefile --console ".\data_collection.py"
copy .\dist\data_collection.exe
@RD /S /Q build , __pycache__ , dist
del .\data_collection.spec
pause