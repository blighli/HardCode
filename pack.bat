:设置exe文件名称
set name=HardCode

:执行打包命令生成exe文件
uv run pyinstaller --add-binary "assets;assets" --add-binary "config;config" -i "assets\app.ico" -wF main.py -n %name% --clean

:运行生成的exe程序
dist\%name%.exe
