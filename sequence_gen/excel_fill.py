import time
import pandas as pd # type: ignore # pandas
import os
import warnings
import openpyxl # type: ignore # openpyxl
import openpyxl.cell._writer # type: ignore # openpyxl
import win32com.client as win32 # type: ignore # win32com

#probably needs a path....
def export_SCRNZ(samples):
    print("starting export")
    # Create a DataFrame from the list of tuples
    df = pd.DataFrame(samples, columns=['Sample Name', 'Vial', 'Filenames'])

    # Write the DataFrame to an Excel file
    excel_path = 'output.csv'

    df.to_csv(excel_path, index=False, encoding='utf-8')


    print(f"Data written to {excel_path}")


def export_SCGEN(samples):
    print("starting export")
    # Create a DataFrame from the list of tuples
    df = pd.DataFrame(samples, columns=['Sample Name', 'Sample Description', 'Sample Position', 'Method Name', 'Volume'])    

    excel_path = 'output.csv'
    df.to_csv(excel_path, index=False, encoding='utf-8')

    print(f"data written to {excel_path}")

def export_LCMSMS(samples):
    print('starting export')
    df = pd.DataFrame(samples, columns=['Batch #', 'Tray', 'Vial#', 'Sample Name'])

    excel_path = 'output.csv'
    
    df.to_csv(excel_path, index=False, encoding='utf-8')
    print(f"Data written to {excel_path}")

def export_SQVOL(samples):
    print('starting export')
    df = pd.DataFrame(samples, columns=['Batch #', 'Tray Name', 'Vial#', 'Sample Name', 'Sample ID'])

    excel_path = 'output.csv'
    df.to_csv(excel_path, index=False, encoding='utf-8')
    print(f'data written to {excel_path}')

