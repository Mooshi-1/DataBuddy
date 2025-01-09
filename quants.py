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


def SHIMADZU_SAMPLEINIT(batch_dir):
    samples = [] #will hold sample objects created here
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
            
            case_number = None
            
            quant_method = lines[3]
            # Currently storing "ABUSE PANEL QUANTITATION BY LC-MS/MS"
            try:
                # Find case number using sample name index + 1
                sample_name_index = lines.index("Sample Name")
                case_number = lines[sample_name_index + 1]
                # Trim characters off case number string
                case_number = case_number[2:]
                print(f"{case_number}")

                # Extract table data
                # maybe try to sort the table data?? needs work. self.values is a mess
                table_data = []
                capture = False
                for line in lines:
                    #start collecting here
                    if "Quantitative Results: ISTDs" in line or "Quantitative Results: Analytes" in line:
                        capture = True
                    #stop collecting here
                    elif capture and line.strip() == "":
                        capture = False
                    #if capture = true, append the data
                    elif capture:
                        table_data.append(line.strip())
                print(f"Extracted table data: {len(table_data)} characters")


                case_number = Sample(case_number, pdf_path, None, table_data)
                print(f"Created sample: {case_number}")
                if case_number in samples:
                    case_number.name += "_duplicate"
                    print(f"recognized duplicate")
                samples.append(case_number)

            except Exception as e:
                print(f"FAILED TO INIT SAMPLE {filename}: {e}")
            doc.close()  

    #return list of sample objects        
    return samples
            
# class Sample:
#     def __init__(self, ID, type, results, path):
#         self.ID = ID
#         self.type = type
#         self.results = results
#         self.path = path

            


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
    SHIMADZU_SAMPLEINIT(batch_dir)