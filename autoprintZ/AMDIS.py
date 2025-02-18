# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 16:15:00 2025

@author: ADG
"""
#attempting to print reports from AMDIS
import pynput
from pynput.keyboard import Controller, Key
import time
import win32gui

keyboard = Controller()

def print_report():
    # Activate menu and navigate to Print
    keyboard.press(Key.alt)
    keyboard.press('f')
    keyboard.release('f')
    keyboard.release(Key.alt)
    time.sleep(1)
    
    keyboard.press('p')
    keyboard.release('p')
    time.sleep(1)
    
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(5)  # Wait for the printing process to complete (adjust time as needed)

    # Bring the window with the data files back into focus by its title
    window_title = "Results of Last Batch Job"  # Replace with the actual title of your data files window
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(1)

        # Navigate within the window using the down arrow key
        keyboard.press(Key.down)
        keyboard.release(Key.down)
        time.sleep(1)
    else:
        print(f"Window with title '{window_title}' not found.")

# Run the function
time.sleep(10)
print_report()
