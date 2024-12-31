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

batch_dir = r"C:\Users\e314883\Desktop\python pdf\PDF DATA\2024"

def LCQUANTrename(batch_dir):
    #iterate through directory defined by filepath
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
            case_number_2 = None
            new_filename = None
            quant_method = None
            
            quant_method = lines[3]
            #currently storing "ABUSE PANEL QUANTITATION BY LC-MS/MS"

            #find case number using sample name index + 1
            if quant_method in lines:
                sample_name_index = lines.index("Sample Name")
                case_number_1 = lines[sample_name_index + 1]
                print(f"{case_number_1}")
                #': DILN BLOOD 1:1'
                #current string
                #need to trim
            elif "Insight MTS Report - Detail" in lines:
                sample_name_index = lines.index("Sample Name")
                case_number_2 = lines[sample_name_index + 1]
                print(f"{case_number_2}")
            elif "Shimadzu 8060NX LCMS Batch Table" in lines:
                if new_filename == None:
                    new_filename = "Sequence_1.pdf"
                else:
                    new_filename = "Sequence_2.pdf"
            else:
                print("case number not found for {filename}")

            # Close the document
            doc.close()

LCQUANTrename(batch_dir)

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