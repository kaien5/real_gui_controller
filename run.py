#!/usr/bin/env python
# Use the code below to convert the .ui file to a .py file
# pyuic5 -x real_gui.ui -o real_gui.py

import controller

if __name__ == '__main__':
    runner = controller.Controller()
