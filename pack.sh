#!/bin/bash
name=HardCode
uv run pyinstaller --add-binary=assets:assets -i "assets\app.ico" -wF main.py -n $name --clean
dist/$name