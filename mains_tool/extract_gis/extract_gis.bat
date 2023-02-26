@echo off

rem Set variables
set path_venv_script=%LOCALAPPDATA%\Building_urban_analysis\tool_venv\Scripts
set path_python_scripts=%LOCALAPPDATA%\Building_urban_analysis\Scripts"

echo Activate the virtual environment
call "%path_venv_script%\activate.bat"

echo Run the GIS extraction
python %path_python_scripts%\mains_tool\extract_gis/main_extract_gis.py %*

rem Deactivate the virtual environment
deactivate
pause