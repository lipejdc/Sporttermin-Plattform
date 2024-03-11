cd Backend

python3 --version 2>NUL
if errorlevel 1 goto errorNoPython3
python3 API.py
pause
exit

:errorNoPython3
py --version 2>NUL
if errorlevel 1 goto errorNoPy
py API.py
pause
exit

:errorNoPy
python --version 2>NUL
if errorlevel 1 goto errorNoPython
python API.py
pause
exit

:errorNoPython
echo.
echo Error: Python not installed!

pause