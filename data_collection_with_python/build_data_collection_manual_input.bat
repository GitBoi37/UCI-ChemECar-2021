@echo off
cd %localhost%
Title Building .exe...  
pyinstaller --onefile --console ".\data_collection_manual_input.py"
copy .\dist\data_collection_manual_input.exe
@RD /S /Q build , __pycache__ , dist
del .\data_collection_manual_input.spec
pause