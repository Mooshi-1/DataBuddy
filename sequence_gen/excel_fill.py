import time
import pandas as pd # type: ignore # pandas
import os
import warnings
import openpyxl # type: ignore # openpyxl
import openpyxl.cell._writer # type: ignore # openpyxl
import win32com.client as win32 # type: ignore # win32com

def export_SCRNZ(samples):
    pass
    columns = ['Sample Name', 'Vial', 'Filenames']

    #create counter? every X * var add control
    # 0 * 20, 1* 20, etc

    #slicing handles out of index gracefully
        # for i in range(0, len(numbers), 20):
        #     new_list.extend(numbers[i:i + 20])
        #     new_list.append("S")
        # return new_list

    