# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 18:36:25 2024

@author: e314883
"""

import os
import fitz
import re

def Zrename(batch_dir):
    # Define case number patterns
    case_pattern = re.compile(r'(\d+-\d+_.+ [AB])')
    control_pattern = re.compile(r'\D+CTRL [0-99] [AB]')

    # Iterate through the directory defined by filepath
    for filename in os.listdir(batch_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(batch_dir, filename)
            
            doc = fitz.open(pdf_path)
            # Extract text from the first page
            page = doc[0]
            text = page.get_text()
            lines = text.split('\n')
            #print(lines)
            
            #iterate lines and search for case number
            #MH case numbers are .match()
            #AMDIS case numbers are .search()
            #elif statements so that the line cannot match to multiple criteria
            #search functions on bottom so matches happen first
            MH_case_number = None
            AM_case_number = None
            
            for line in lines:
                if case_pattern.match(line):
                    MH_case_number = case_pattern.match(line).group().strip()
                    print(f"matched MH {MH_case_number}")
                    break
                elif control_pattern.match(line):
                    MH_case_number = control_pattern.match(line).group().strip()
                    print(f"matched MH {MH_case_number}")
                    break                    
                elif case_pattern.search(line):
                    AM_case_number = case_pattern.search(line).group().strip()
                    print(f"matched AM {AM_case_number}")
                    break
                elif control_pattern.search(line):
                    AM_case_number = control_pattern.search(line).group().strip()
                    print(f"matched AM {AM_case_number}")
                    break
                    

            # Close the document
            doc.close()

            # Check if either case number was found
            if not MH_case_number and not AM_case_number:
                print(f"--error-- unable to locate case number for {filename}")
                continue  # Skip renaming if no case number is found

            # Define the new filename based on the case number found
            if MH_case_number:
                new_filename = f"{MH_case_number}-MH.pdf"
            if AM_case_number:
                new_filename = f"{AM_case_number}-AM.pdf"

            new_path = os.path.join(os.path.dirname(pdf_path), new_filename)

            # Rename the file
            try:
                os.rename(pdf_path, new_path)
                print(f"{filename} has been renamed to {new_filename}")

            except PermissionError as e:
                print(f"PermissionError: {e}")

def Zbinder(batch_dir, output_dir, batch_num):
    # Iterate through batch_dir for filenames
    for filename in os.listdir(batch_dir):
        # Check for B-MH.pdf files
        if filename.endswith(" B-MH.pdf"):
            sample = filename.rsplit(" B-MH.pdf", 1)[0]
            b_mh = filename
            b_am = f"{sample} B-AM.pdf"
            a_mh = f"{sample} A-MH.pdf"
            a_am = f"{sample} A-AM.pdf"

            # Bind the files in the specified order and save the file with batch number
            if b_mh in os.listdir(batch_dir) \
            and b_am in os.listdir(batch_dir) \
            and a_mh in os.listdir(batch_dir) \
            and a_am in os.listdir(batch_dir):
                b_mh_doc = fitz.open(os.path.join(batch_dir, b_mh))
                b_am_doc = fitz.open(os.path.join(batch_dir, b_am))
                a_mh_doc = fitz.open(os.path.join(batch_dir, a_mh))
                a_am_doc = fitz.open(os.path.join(batch_dir, a_am))
                
                # Insert PDFs in the specified order
                b_mh_doc.insert_pdf(b_am_doc)
                b_mh_doc.insert_pdf(a_mh_doc)
                b_mh_doc.insert_pdf(a_am_doc)
                
                # Save the final document
                b_mh_doc.save(os.path.join(output_dir, f"{sample}_{batch_num}.pdf"))
                print(f"Successfully bound {sample}")

            else:
                print(f"--error-- cannot locate all 4 documents for {filename}")
                
def Zcontrols(output_dir, batch_num):
    neg_ctrl = None
    pos_ctrls = []
    
    #separate neg and pos -- NOTE .startswith("STRING")
    for filename in os.listdir(output_dir):
        print(filename)
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
    merged_pdf.save(os.path.join(output_dir, f"SCRNZ_{batch_num}.pdf"))
    print("batch pack created")
        

batch_dir = r"C:\Users\e314883\Desktop\python pdf\raw_tests"
output_dir = r"C:\Users\e314883\Desktop\python pdf\op_tests"
batch_num = 12777

#r prefix makes it so python does not interpret backslashes as line breaks
Zrename(batch_dir)
Zbinder(batch_dir, output_dir, batch_num)
Zcontrols(output_dir, batch_num)







#delete pages
# doc = pymupdf.open("test.pdf") # open a document
# doc.delete_page(0) # delete the 1st page of the document
# doc.save("test-deleted-page-one.pdf") # save the document