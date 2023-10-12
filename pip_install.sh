#!/bin/bash
python -m pip install --upgrade pip

pip install pygame
pip install pygame_gui
pip install pillow
pip install tcod
pip install numpy
pip install websocket
pip install websocket-client

# if your system does not find BLAS libray when you run this script,
# you can try to install: apt install python3-dev.
# you can try to install: apt install numpy (not with pip).
# you can try to install: apt install tcod (not with pip).
# you can try to install (via pip or apt) libopenblas-dev.
# if it does not work ..., sorry i can not help you furthermore.
