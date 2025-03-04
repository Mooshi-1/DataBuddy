# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 16:15:00 2025

@author: ADG
"""
#attempting to print reports from AMDIS
import pyautogui
import time
import pygetwindow as gw

def main():
    counter = 0
    input('Ensure that your AMDIS processing list window named:\n[Results of Last Batch Job] is open and highlighted on the first sample. \nPress enter to continue')

    all_windows = gw.getAllTitles()
    target_windows = [w for w in all_windows if w.startswith("AMDIS Chromatogram")]
    if target_windows:
        AMDIS_program = gw.getWindowsWithTitle(target_windows[0])[0]
        AMDIS_program.minimize()
        time.sleep(1)
        AMDIS_program.restore()
        time.sleep(1)
        AMDIS_program.resizeTo(600, 600)
        time.sleep(1)

        print('initialization successful, starting loop... do not operate the computer')
        print_report(counter)
    else:
        input('Unable to find AMDIS window. Press enter to exit')


def print_report(counter):
    counter += 1

    all_windows = gw.getAllTitles()
    target_windows = [w for w in all_windows if w.startswith("AMDIS Chromatogram")]
    sample_name = target_windows[0].split(' - ')[2].strip()
    print(f'printing report #{counter} - {sample_name}')
    #active = target_windows[0].activate()

    pyautogui.press('alt')
    time.sleep(0.3)
    pyautogui.press('m')
    time.sleep(0.3)
    pyautogui.press('t')
    time.sleep(0.3)
    pyautogui.press('alt')
    time.sleep(0.3)
    pyautogui.press('f')
    time.sleep(0.3)
    pyautogui.press('p')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3) 

    window = gw.getWindowsWithTitle("Results of Last Batch Job")[0]
    time.sleep(1)
    window.activate()
    time.sleep(1)
    pyautogui.press('down')
    time.sleep(4)

    active_window = gw.getActiveWindow()

    if active_window == window:
        print(f'printed {counter} reports')
        input('Out of reports to print... Press enter to exit')
        return
    else:
        print_report(counter)


if __name__ == '__main__':

    main()