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
            print(text)
            lines = text.split('\n')
            print(lines)
            
            def get top sheet:
            def get bottom sheet:
            def define controls:
            
            
            #get case number
            try: 
                if "Insight MTS Report - Summary" in lines:
                    sample_name_index = lines.index("Sample Name")
                    case_number = lines[sample_index + 1]
                    print(f"{filename}")

            # # Extract the case number from the third line
            # case_number = lines[2].strip()
            # #print(case_number)
            # #handle exceptions -- regex string for hyphenated case num
            # pattern = re.compile(r"^.+-.+ [AB]$")
            # if not pattern.match(case_number):
            #     if not case_number.startswith("NEG") \
            #     and not case_number.startswith("POS"):    
            #         print(f"--error--skipping {filename} due to invalid case num")
            #         continue

            # # Close the document
            # doc.close()

            # # Define the new filename
            # new_filename = f"{case_number}.pdf"
            # new_path = os.path.join(os.path.dirname(pdf_path), new_filename)

            # # Rename the file
            # try:
            #     os.rename(pdf_path, new_path)
            #     print(f"{filename} has been renamed to {new_filename}")
            # except PermissionError as e:
            #     print(f"--PermissionError--: {e}")
        
def LCMSbinder(batch_dir, output_dir, batch_num):
    #iterate thrugh batch_dir for filenames
    for filename in os.listdir(batch_dir):
        #check base-acid pairs -- do nothing if base-acid pair does not exist
        if filename.endswith(" B.pdf"):
            #cuts off " B" and defines that as sample - comes back in save file
            sample = filename.rsplit(" B.pdf", 1)[0]
            base = filename
            acid = f"{sample} A.pdf"
            
            #bind acid into base and save file with batch number
            if base in os.listdir(batch_dir) \
            and acid in os.listdir(batch_dir):
                base_doc = fitz.open(os.path.join(batch_dir,base))
                acid_doc = fitz.open(os.path.join(batch_dir,acid))
                base_doc.insert_pdf(acid_doc)
                base_doc.save(os.path.join(output_dir, f"{sample}_{batch_num}.pdf"))
                print(f"successfully bound {sample}")
                
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
    try:
        for pdf in files_to_merge:
            if pdf is not None:
                with fitz.open(os.path.join(output_dir, pdf)) as pdf_document:
                    merged_pdf.insert_pdf(pdf_document)
            else:
                raise TypeError("PDF file is None")
    except TypeError as e:
        print(f"No controls found in {output_dir} - rerun program in batch pack data")
        print(f"Error details: {e}")
    
    #save
    merged_pdf.save(os.path.join(output_dir, f"SCGEN_{batch_num}.pdf"))
    print("batch pack created")
        


batch_dir = r"C:\Users\e314883\Desktop\python pdf\raw_tests"
#output_dir = r"C:\Users\e314883\Desktop\python pdf\op_tests"
#batch_num = 12756

#r prefix makes it so python does not interpret backslashes as line breaks
LCMSrename(batch_dir)
#LCMSbinder(batch_dir, output_dir, batch_num)
#LCMScontrols(output_dir, batch_num)

