# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 17:49:56 2024

@author: e314883
"""

import fitz  # PyMuPDF
import os
import re
#import time

def LCMSrename(batch_dir):
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
            #print(lines)

            case_number_1 = None
            case_number_2 = None
            new_filename = None
            
            #find case number using sample name index + 1
            if "Insight MTS Report - Summary" in lines:
                sample_name_index = lines.index("Sample Name")
                case_number_1 = lines[sample_name_index + 1]
                print(f"{case_number_1}")
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
        
def LCMSbinder(batch_dir, output_dir, batch_num):
    #iterate thrugh batch_dir for filenames
    for filename in os.listdir(batch_dir):
        #check _1 _2 pair
        if filename.endswith("_1.pdf"):
            #cuts off "_1" and defines that as sample - comes back in save file
            sample = filename.rsplit("_1.pdf", 1)[0]
            top_sheet = filename
            bot_sheet = f"{sample}_2.pdf"
            
            #combine and save file with batch number
            if top_sheet in os.listdir(batch_dir) \
            and bot_sheet in os.listdir(batch_dir):
                top_doc = fitz.open(os.path.join(batch_dir,top_sheet))
                bot_doc = fitz.open(os.path.join(batch_dir,bot_sheet))
                top_doc.insert_pdf(bot_doc)
                top_doc.save(os.path.join(output_dir, f"{sample}_{batch_num}.pdf"))
                print(f"successfully bound {sample}")
            else:
                print(f"--error-- cannot locate all documents for {filename}")
                
def LCMScontrols(output_dir, batch_num):
    neg_ctrl = None
    pos_ctrls = []
    
    #separate neg and pos -- NOTE .startswith("STRING")
    for filename in os.listdir(output_dir):
        if filename.startswith("NEG"):
            neg_ctrl = filename
        elif filename.startswith("POS"):
            pos_ctrls.append(filename)

    #sort pos controls 
    pos_ctrls.sort(key=lambda x: int(x.split()[2].split("_")[0]))
    
    #prepare lists for merge
    files_to_merge = [neg_ctrl] + pos_ctrls
    merged_pdf = fitz.open()
    
    #merge
    for pdf in files_to_merge:
        if pdf is not None:
            with fitz.open(os.path.join(output_dir, pdf)) as pdf_document:
                merged_pdf.insert_pdf(pdf_document)
    #save
    try:
        merged_pdf.save(os.path.join(output_dir, f"SCLCMSMS_{batch_num}.pdf"))
        print("batch pack created")
    except ValueError:
        print("--error-- could not find control data")
        
if __name__ == "__main__":
    batch_dir = r"C:\Users\e314883\Desktop\python pdf\PDF DATA\2024\12\12773\CASE DATA"
    output_dir = r"C:\Users\e314883\Desktop\python pdf\PDF DATA\2024\12\12773\CASE DATA\--binder files--"
    batch_num = 12756

    LCMSrename(batch_dir)
    LCMSbinder(batch_dir, output_dir, batch_num)
    LCMScontrols(output_dir, batch_num)
