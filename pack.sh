#!/bin/bash
name=HardCode
uv run pyinstaller --add-binary=assets:assets --add-binary=config:config -i "assets\app.ico" -wF main.py -n $name --clean
dist/$name