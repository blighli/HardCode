# HardCode

Hardware Development Code Base

note:

install uv: 

powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

install pyinstaller (in venv!!!):

uv pip install pyinstaller 

run application:

uv run main.py

pack application in exe:

pack.bat

(uv run pyinstaller --add-binary "assets;assets" -i "assets\app.ico" -wF main.py -n %name% --clean)



