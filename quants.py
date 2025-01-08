# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 16:20:55 2024

@author: e314883
"""

#quants
#exceptions to think about
#name casefiles 1 and 2 like LCMSMS
#sometimes single injections

#spiked recovery (3 files, +%R pdf)
#L0 - L6 on 

import fitz  # PyMuPDF
import os
import re

from objects import QCTYPE, QC, Sample


def LCQUANTrename(batch_dir):
    # Iterate through directory defined by filepath
    for filename in os.listdir(batch_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(batch_dir, filename)        
            doc = fitz.open(pdf_path)

            # Extract text from the first page
            page = doc[0]
            text = page.get_text()
            #print(text)
            lines = text.split('\n')
            
            case_number_1 = None
            
            quant_method = lines[3]
            # Currently storing "ABUSE PANEL QUANTITATION BY LC-MS/MS"
            try:
                # Find case number using sample name index + 1
                sample_name_index = lines.index("Sample Name")
                case_number_1 = lines[sample_name_index + 1]
                # Trim characters off case number string
                case_number_1 = case_number_1[2:]
                print(f"{case_number_1}")

                # Extract table data
                table_data = []
                capture = False
                for line in lines:
                    if "Quantitative Results: ISTDs" in line or "Quantitative Results: Analytes" in line:
                        capture = True
                    elif capture and line.strip() == "":
                        capture = False
                    elif capture:
                        table_data.append(line.strip())
                print(f"Extracted table data: {table_data}")

                # Create Sample object and assign QCTYPE
                if "CTRL" in lines:
                    sample = Sample(case_number_1, QCTYPE.CTL, table_data, pdf_path)
                elif "SR" in lines:
                    sample = Sample(case_number_1, QCTYPE.SR, table_data, pdf_path)
                else:
                    sample = Sample(case_number_1, None, table_data, pdf_path)
                print(f"Created sample: {sample}")

            except Exception as e:
                print(f"Error finding case number or extracting table data: {e}")
# class Sample:
#     def __init__(self, ID, type, results, path):
#         self.ID = ID
#         self.type = type
#         self.results = results
#         self.path = path

            # Close the document
            doc.close()


""""
            # Define the new filename
            if case_number_1:
                new_filename = f"{case_number_1}_1.pdf"
            if case_number_2:
                new_filename = f"{case_number_2}_2.pdf"
            new_path = os.path.join(os.path.dirname(pdf_path), new_filename)

            # Rename the file
            try:
                os.rename(pdf_path, new_path)
                print(f"{filename} has been renamed to {new_filename}")

            except PermissionError as e:
                print(f"PermissionError: {e}")
                continue
            except FileExistsError as e:
                print(f"File Exists Error: {e}")
                continue
            except FileNotFoundError as e:
                print(f"File Not Found Error: {e}")
                continue
"""

if __name__ == "__main__":
    batch_dir = r"C:\Users\e314883\Desktop\python pdf\PDF DATA\2024"
    LCQUANTrename(batch_dir)