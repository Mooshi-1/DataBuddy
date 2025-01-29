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