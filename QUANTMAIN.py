# -*- coding: utf-8 -*-
"""
Created on Thurs 01/09/2025

@author: Giachetti
"""
#pyinstaller main.py -- to package .exe file
#make shortcut from dist folder
#export QC data to pdf
#handle reinjects
#integrate sequence generation from test batch
##export sequence as pdf
#use pyinstaller or py2exe libs to create .exe file

import sys
import os

import searcher
import quants
import qc


ascii_art = """
 .
 ooo        ooooo oooooooooo.   ooo        ooooo oooooooooooo      ooooooooooooo   .oooooo.   ooooooo  ooooo 
 `88.       .888' `888'   `Y8b  `88.       .888' `888'     `8      8'   888   `8  d8P'  `Y8b   `8888    d8'  
  888b     d'888   888      888  888b     d'888   888                   888      888      888    Y888..8P    
  8 Y88. .P  888   888      888  8 Y88. .P  888   888oooo8              888      888      888     `8888'     
  8  `888'   888   888      888  8  `888'   888   888    "              888      888      888    .8PY888.    
  8    Y     888   888     d88'  8    Y     888   888       o           888      `88b    d88'   d8'  `888b   
 o8o        o888o o888bood8P'   o8o        o888o o888ooooood8          o888o      `Y8bood8P'  o888o  o88888o 
 
(((((((QUANTS -- PRELIM TESTING))))))) 

Version 1.05 - 01/09/2025
"""

def main(batch, method):
    print(f"Batch Number: {batch}")
    print(f"Method: {method}")
    
    # data_dir = r"G:\PDF DATA"
    # print(f"Starting in: {data_dir}")
    
    #call FindBatch function to locate directories
    # case_dir, qc_dir = searcher.FindBatch(data_dir, batch)
    # if case_dir and qc_dir == None:
    #     raise Exception("Unable to locate batch directory")                
    
    #create binder output
    case_dir = r'C:\Users\e314883\Desktop\locked_git_repo\12786\CASE DATA'
    batch_dir = r'C:\Users\e314883\Desktop\locked_git_repo\12786\BATCH PACK DATA'

    output_dir = searcher.binder_dir(case_dir)
    print(f"Output Directory: {output_dir}")


    batch_dirs = [batch_dir, case_dir]

    all_samples = []

    for dirs in batch_dirs:
        print(f"checking {dirs}")
        samples = quants.SHIMADZU_SAMPLEINIT(dirs)
        all_samples.extend(samples)


    quants.pdf_rename(all_samples)

    for sample in all_samples:
        sample.assign_type()
    
    print(len(all_samples))
    cal_curve, neg_ctl, shooter, controls, dil_controls, SR_cases, cases, curve, MOA_cases, sequence = qc.QC_handler(all_samples)

    #anything I want to do with lists here? export??

    
    batch_pack = qc.batch_pack_handler(curve,shooter,neg_ctl,cal_curve,controls,sequence,dil_controls)
    quants.list_binder(batch_pack, output_dir, batch)
    #make sure this is at the end
    #changes self.path of a single repeat and may cause issues for other references
    quants.compare_and_bind_duplicates(cases, output_dir, batch)

    print("complete")

    
    #move files from individual folders
    # searcher.Shuttle(case_dir)

            
    #return files to individual directory
    #searcher.ShuttleHome(case_dir)
    
if __name__ == "__main__":
    print(ascii_art)
    # Check if the required arguments are passed via sys.argv
    if len(sys.argv) < 3:
        batch = input("Enter the batch number: ")
        method = input("Enter the method (SHIMADZU): ")
        input("Reminder: Unable to handle reinjects. Bind your sequence manually. Existing bound files will be overwritten. Press Enter to continue...")
    else:
        # Use CLI provided arguments
        batch_num = sys.argv[1]
        method = sys.argv[2]

    # Call the main function with the provided or inputted arguments
    main(batch, method)

    input("Press Enter to exit...")
