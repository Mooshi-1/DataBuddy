import time
import pandas as pd # type: ignore # pandas
import os
import warnings
import openpyxl # type: ignore # openpyxl
import openpyxl.cell._writer # type: ignore # openpyxl


#probably needs a path....
def export_SCRNZ(samples, path, batch_num):
    print("starting export")
    # Create a DataFrame from the list of tuples
    df = pd.DataFrame(samples, columns=['Sample Name', 'Vial', 'Filenames'])

    # Write the DataFrame to an Excel file
    excel_path = os.path.join(path, f'{batch_num}.csv')

    df.to_csv(excel_path, index=False, encoding='utf-8')

    print(f"Data written to {excel_path}")


def export_SCGEN(samples, path, batch_num):
    print("starting export")
    # Create a DataFrame from the list of tuples
    df = pd.DataFrame(samples, columns=['Sample Name', 'Sample Description', 'Sample Position', 'Method Name', 'Volume'])    

    excel_path = os.path.join(path, f'{batch_num}.csv')
    df.to_csv(excel_path, index=False, encoding='utf-8')

    print(f"data written to {excel_path}")

def export_LCMSMS(samples, path, batch_num):
    print('starting export')
    df = pd.DataFrame(samples, columns=['Batch #', 'Tray', 'Vial#', 'Sample Name'])

    excel_path = os.path.join(path, f'{batch_num}.csv')
    
    df.to_csv(excel_path, index=False, encoding='utf-8')
    print(f"Data written to {excel_path}")

def export_SQVOL(samples, path, batch_num):
    print('starting export')
    df = pd.DataFrame(samples, columns=['Batch #', 'Tray Name', 'Vial#', 'Sample Name', 'Sample ID', 'barcode'])

    excel_path = os.path.join(path, f'{batch_num}.xlsx')
    df.to_excel(excel_path, index=False)
    print(f'data written to {excel_path}')


def export_quants(samples, path, batch_num):
    print('starting export')
    df = pd.DataFrame(samples, columns=['Batch #', 'Tray', 'Vial#', 'Sample Name'])

    excel_path = os.path.join(path, f'{batch_num}.xlsx')
    df.to_excel(excel_path, index=False)
    print(f'data written to {excel_path}')