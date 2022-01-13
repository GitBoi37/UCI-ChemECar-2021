@echo off
cd %localhost%
Title Building .exe...  
pyinstaller --onefile --console ".\simple_data_collection.py"
copy .\dist\simple_data_collection.exe
@RD /S /Q build , __pycache__ , dist
del .\simple_data_collection.spec
pause