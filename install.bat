@ECHO OFF
python3 --version 2>NUL
if errorlevel 1 goto errorNoPython3
python3 -m pip install sqlalchemy
python3 -m pip install sqlalchemy_utils
python3 -m pip install flask
exit

:errorNoPython3
py --version 2>NUL
if errorlevel 1 goto errorNoPy
py -m pip install sqlalchemy
py -m pip install sqlalchemy_utils
py -m pip install flask
exit

:errorNoPy
python --version 2>NUL
if errorlevel 1 goto errorNoPython
python -m pip install sqlalchemy
python -m pip install sqlalchemy_utils
python -m pip install flask
exit

:errorNoPython
@ECHO ON
echo.
echo Error: Python not installed!

pause