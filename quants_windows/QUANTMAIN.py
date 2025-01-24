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

import searcher
import shimadzu_init
import sample_sorter
import aux_func
import filler

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

Version 1.08 - 01/21/2025
"""

def main(batch, method):
    print(f"Batch Number: {batch}")
    print(f"Method: {method}")
    
    LF_directory = r'G:\LABORATORY OPERATIONS\06 - LABORATORY FORMS'
    TP_directory = r'G:\LABORATORY OPERATIONS\07 - TESTING PROCEDURES'
    data_dir = r"G:\PDF DATA"
    print(f"Starting in: {data_dir}")
    
    #call FindBatch function to locate directories
    case_dir, qc_dir = searcher.FindBatch(data_dir, batch)
    if case_dir is None and qc_dir is None:
        raise Exception("Unable to locate batch directory")                
    
        
    #move files from individual folders
    searcher.Shuttle(case_dir)

    #delete these later
    #case_dir = r'/mnt/c/Users/Mooshi/Desktop/work-locked/private/12786/CASE DATA'
    #qc_dir = r'/mnt/c/Users/Mooshi/Desktop/work-locked/private/12786/BATCH PACK DATA'
   
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

    if len(all_samples) == 0:
        print("unable to find data -- is it in the CASE DATA and/or BATCH PACK DATA folder?")


    aux_func.pdf_rename(all_samples)

    for sample in all_samples:
        sample.assign_type()
        #print(sample)
    
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
        sequence,
        serum_shooter,
        serum_neg,
        serum_controls,
        serum_dil_controls,
        serum_cal_curve
    ) = sample_sorter.sample_handler(all_samples)

    #grab ISAR from TP directory and put in output dir
    #then fill
    try:
        if len(controls) >= 4:
            print("getting blood ISAR")
            output_path = searcher.copy_file(aux_func.get_ISAR(method,TP_directory), output_dir, "ISAR_blood")
            filler.ISAR_fill(controls, batch, output_path)
            
        if len(serum_controls) >= 4:
            print("getting serum ISAR")
            output_path_s = searcher.copy_file(aux_func.get_ISAR(method,TP_directory), output_dir, "ISAR_serum")
            filler.ISAR_fill(controls, batch, output_path_s)
    except Exception as e:
        print(f"--error-- unable to retrieve/fill ISAR | {e}")

    #LJ output
    try:
        filler.output_LJ(controls, serum_controls, batch, output_dir)
        print("LJ excel sheet successfully created!")
    except Exception as e:
        print(f"--error-- unable to fill LJ | {e}")

    #send case-list to binder, bind duplicates -- return list of singles
    leftovers = aux_func.compare_and_bind_duplicates(cases, output_dir, batch)

    #singles handler
    if len(leftovers) > 0:
        aux_func.move_singles(leftovers, output_dir, batch)
   
    #MSA handler
    if len(MOA_cases) > 0:
        sliced_MOA = aux_func.MOA_slicer(MOA_cases)
        for case_list in sliced_MOA:
            positive_analytes = filler.interpret_MSA(case_list)
            for analyte in positive_analytes:
                MSA_path = searcher.copy_excel(aux_func.get_MSA(LF_directory), output_dir, f"{case_list[0].base}_{analyte}")
                #create excel file here using case_list
                filler.fill_MSA(case_list, batch, MSA_path, analyte)

            aux_func.list_binder(case_list, output_dir, batch)

    #SR case bind must come after compare_and_bind_duplicates otherwise will have name conflict
    if len(SR_cases) > 0:
        sliced_SR = aux_func.find_sr(cases, SR_cases)
        for case_list in sliced_SR:
            aux_func.list_binder(case_list, output_dir, batch)

    #organize batch pack
    if len(serum_controls) > 0:
        print("serum QC detected -- appending batch pack")
        batch_pack = aux_func.serum_batch_pack_handler(curve,shooter,neg_ctl,cal_curve,controls,sequence,dil_controls,
                             serum_shooter,serum_neg,serum_controls,serum_dil_controls,serum_cal_curve)
    else:
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
        input("Reminder: Unable to handle reinjects. Press Enter to continue...")
    else:
        # Use CLI provided arguments
        batch = sys.argv[1]
        method = sys.argv[2]

    # Call the main function with the provided or inputted arguments
    main(batch, method)

    input("Press Enter to exit...")
