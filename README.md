# HardCode Overview

Hardware Development Code Base

# Note: Run and Pack

## install uv: 
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## install pyinstaller (in venv!!!):
```
uv pip install pyinstaller 
```

## run application:
```
uv run main.py
```

## pack application in exe:

pack.bat
```
uv run pyinstaller --add-binary "assets;assets" --add-binary "config;config" -i "assets\app.ico" -wF main.py -n %name% --clean
```

# Linux:

serial port open failed: Permission denied
```
Solution: sudo usermod -a -G dialout <username>
groups ${USER}
sudo gpasswd --add ${USER} dialout
newgrp dialout
```
!!Important!!
reboot

# memo:
##小米微电机串口控制指令,波特率921600
```
先要运行AT+AT进入AT模式，即：41 54 2b 41 54 0d 0a
jog+：41 54 90 07 eb fc 08 05 70 00 00 07 01 95 54 0d 0a
jog停止：41 54 90 07 eb fc 08 05 70 00 00 07 00 7f ff 0d 0a
jog-：41 54 90 07 eb fc 08 05 70 00 00 07 01 6a aa 0d 0a
```


##CANable 2.0

https://github.com/normaldotcom/canable2-fw

大小写敏感，命令结尾加<CR>，即'\r'

O<CR> - Open channel

C<CR> - Close channel

V<CR> - Returns firmware version and remote path as a string