#grrr dealing with problems

import pandas as pd
from openpyxl import Workbook

# Create a sample DataFrame
d = {"ISTD Peak Area": ['993915', '998488', '1077438', '1069731', '1060323', '954421'],
     "Analyte Peak Area": ['1520767', '1814234', '1886632', '2246658', '2459623', '3586997']}
df = pd.DataFrame(d)

# Specify a new Excel file path
new_excel_path = r'G:\PDF DATA\2025\1\999\CASE DATA\test_book1.xlsx'

try:
    # Create a new workbook and add a sheet
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Visible Sheet"
    
    # Save the workbook
    workbook.save(new_excel_path)

    # Write the DataFrame to the new workbook
    with pd.ExcelWriter(new_excel_path, engine='openpyxl', mode='a') as writer:
        df.to_excel(writer, index=False, sheet_name="LF-10 MSA Worksheet")
    print(f"DataFrame written to: {new_excel_path}")

except Exception as e:
    print(f"An error occurred: {e}")
