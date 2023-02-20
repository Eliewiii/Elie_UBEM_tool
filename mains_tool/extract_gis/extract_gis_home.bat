@echo off

rem Activate the virtual environment
set "VENV_SCRIPTS=D:\Documents\venv_tool\Scripts"

call "%VENV_SCRIPTS%\activate.bat"

rem Run the Python script with optional arguments
python D:\Documents\PhD\mains_tool\extract_gis/main_extract_gis.py %*

rem Deactivate the virtual environment
deactivate