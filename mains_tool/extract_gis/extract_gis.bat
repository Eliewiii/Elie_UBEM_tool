@echo off

rem Activate the virtual environment
set "VENV_SCRIPTS=D:\Elie\PhD\tool_venv\Scripts"

call "%VENV_SCRIPTS%\activate.bat"

rem Run the Python script with optional arguments
python D:\Elie\PhD\Programming\Elie_UBEM_tool\mains_tool\extract_gis/main_extract_gis.py %*

rem Deactivate the virtual environment
deactivate