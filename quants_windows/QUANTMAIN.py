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
import shimadzu_init
import sample_sorter
import aux_func


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

Version 1.0 - 01/13/2025
"""

def main(batch, method):
    print(f"Batch Number: {batch}")
    print(f"Method: {method}")
    
    data_dir = r"G:\PDF DATA"
    print(f"Starting in: {data_dir}")
    
    #call FindBatch function to locate directories
    case_dir, qc_dir = searcher.FindBatch(data_dir, batch)
    if case_dir is None and qc_dir is None:
        raise Exception("Unable to locate batch directory")                
    
        
    #move files from individual folders
    searcher.Shuttle(case_dir)

    #delete these later
    #case_dir = r'C:\Users\e314883\Desktop\locked_git_repo\12786\CASE DATA'
    #batch_dir = r'C:\Users\e314883\Desktop\locked_git_repo\12786\BATCH PACK DATA'
   
    #create binder output
    output_dir = searcher.binder_dir(case_dir)
    print(f"Output Directory: {output_dir}")


    batch_dirs = [case_dir, qc_dir]

    #init list to store sample class
    all_samples = []
    #check CASE DATA and BATCH PACK DATA
    for dirs in batch_dirs:
        print(f"checking {dirs}")
        samples = shimadzu_init.LC_quant_init(dirs)
        all_samples.extend(samples)

    aux_func.pdf_rename(all_samples)

    for sample in all_samples:
        sample.assign_type()
    
    print(f"{len(all_samples)} total pdf files -- QC assigned -- proceeding to sort/bind")

    #convert all samples into individual lists. len(all samples) == len(all lists)
    (
        cal_curve,
        neg_ctl,
        shooter,
        controls,
        dil_controls,
        SR_cases,
        cases,
        curve,
        MOA_cases,
        sequence
    ) = sample_sorter.sample_handler(all_samples)

    #send case-list to binder, bind duplicates -- return list of singles
    leftovers = aux_func.compare_and_bind_duplicates(cases, output_dir, batch)

    #need something to change the name of leftovers and move it to the binder folder
    if len(leftovers) > 0:
        aux_func.move_singles(leftovers, output_dir, batch)

    if len(MOA_cases) > 0:
        sliced_MOA = aux_func.MOA_slicer(MOA_cases)
        for case_list in sliced_MOA:
            aux_func.list_binder(case_list, output_dir, batch)

    #unable to pass dynamic name parameter through  here... make sure this runs after compare_and_bind_duplicates unless changed
    #otherwise likely will have an issue where compare_and_bind and list_binder will output the same name here 
    if len(SR_cases) > 0:
        sliced_SR = aux_func.find_sr(cases, SR_cases)
        for case_list in sliced_SR:
            aux_func.list_binder(case_list, output_dir, batch)

    #organize batch pack
    batch_pack = aux_func.batch_pack_handler(curve,shooter,neg_ctl,cal_curve,controls,sequence,dil_controls)
    #send batch pack to binder
    aux_func.list_binder(batch_pack, output_dir, batch, method)


    print("complete")

    #return files to individual directory
    searcher.ShuttleHome(case_dir)
    
if __name__ == "__main__":
    print(ascii_art)
    # Check if the required arguments are passed via sys.argv
    if len(sys.argv) < 3:
        batch = input("Enter the batch number: ")
        method = input("Enter the shimadzu quant (QTABUSE, QTSTIM, etc): ")
        input("Reminder: Unable to handle reinjects. Remove other forms/ICARS from main directories. Press Enter to continue...")
    else:
        # Use CLI provided arguments
        batch = sys.argv[1]
        method = sys.argv[2]

    # Call the main function with the provided or inputted arguments
    main(batch, method)

    input("Press Enter to exit...")
