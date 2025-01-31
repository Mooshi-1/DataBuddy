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
    excel_path = 'output.xlsx'

    df.to_excel(excel_path, index=False)


    print(f"Data written to {excel_path}")

def export_SCGEN(samples):
    print("starting export")
    # Create a DataFrame from the list of tuples
    df = pd.DataFrame(samples, columns=['Sample Name', 'Sample Description', 'Sample Position', 'Method Name', 'Volume'])    

    excel_path = 'output.xlsx'
    df.to_excel(excel_path, index=False)

    print(f"data written to {excel_path}")