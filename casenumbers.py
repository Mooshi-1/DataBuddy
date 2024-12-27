# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 12:32:52 2024

@author: e314883
"""

import fitz  # PyMuPDF
import os
import time

batch_dir = r"G:\PDF DATA\2024\12\12756\CASE DATA"
output_dir = r"C:\Users\e314883\Desktop\python pdf\op_tests"
batch_num = 12756

def GENrename(batch_dir):
    #iterate through directory defined by filepath
    for filename in os.listdir(batch_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(batch_dir, filename)
            
            doc = fitz.open(pdf_path)

            # Extract text from the first page
            page = doc[0]
            text = page.get_text()
            lines = text.split('\n')

            # Extract the case number from the third line
            case_number = lines[2].strip()
            #print(case_number)

            # Close the document
            doc.close()

            # Define the new filename
            new_filename = f"{case_number}.pdf"
            new_path = os.path.join(os.path.dirname(pdf_path), new_filename)

            # Rename the file
            try:
                os.rename(pdf_path, new_path)
                print(f"{filename} has been renamed to {new_filename}")
            except PermissionError as e:
                print(f"PermissionError: {e}")
        
def GENbinder(batch_dir, output_dir, batch_num):
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
                
def GENcontrols(output_dir, batch_num):
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
        with fitz.open(os.path.join(output_dir, pdf)) as pdf_document:
            merged_pdf.insert_pdf(pdf_document)
    
    #save
    merged_pdf.save(os.path.join(output_dir, f"SCGEN_{batch_num}.pdf"))
    print("batch pack created")
        


#r prefix makes it so python does not interpret backslashes as line breaks
#GENrename(batch_dir)
#GENbinder(batch_dir, output_dir, batch_num)
GENcontrols(output_dir, batch_num)






#delete pages
# doc = pymupdf.open("test.pdf") # open a document
# doc.delete_page(0) # delete the 1st page of the document
# doc.save("test-deleted-page-one.pdf") # save the document