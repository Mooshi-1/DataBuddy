# -*- coding: utf-8 -*-
"""
Created on Thurs 01/09/2025

@author: Giachetti
"""
#handle reinjects
#integrate sequence generation from test batch
##export sequence as pdf
import sys
import searcher
import shimadzu_init
import sample_sorter
import aux_func
import filler
import sqvol_init
import logging
import os
import scion_init

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
import audit
sys.path.remove(parent_dir)

ascii_art = """
 ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗████████╗
██╔═══██╗██║   ██║██╔══██╗████╗  ██║╚══██╔══╝
██║   ██║██║   ██║███████║██╔██╗ ██║   ██║   
██║▄▄ ██║██║   ██║██╔══██║██║╚██╗██║   ██║   
╚██████╔╝╚██████╔╝██║  ██║██║ ╚████║   ██║   
 ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   
                                             
██████╗ ██╗███╗   ██╗██████╗ ███████╗██████╗ 
██╔══██╗██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
██████╔╝██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝
██╔══██╗██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
██████╔╝██║██║ ╚████║██████╔╝███████╗██║  ██║
╚═════╝ ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                            
Version 1.11 - 03/07/2025
"""

def main(batch, method, extraction_date=None, initials=None):
    print(f"Batch Number: {batch}")
    print(f"Method: {method}")
    
    LF_directory = r'G:\LABORATORY OPERATIONS\06 - LABORATORY FORMS'
    TP_directory = r'G:\LABORATORY OPERATIONS\07 - TESTING PROCEDURES'
    data_dir = r"G:\PDF DATA"
    print(f"Starting in: {data_dir}", flush=True)
    
    #call FindBatch function to locate directories
    case_dir, qc_dir = searcher.FindBatch(data_dir, batch)
    if case_dir is None and qc_dir is None:
        raise Exception("Unable to locate batch directory")                
    
        
    #move files from individual folders
    searcher.Shuttle(case_dir)

    #create binder output
    output_dir = searcher.binder_dir(case_dir)
    print(f"Output Directory: {output_dir}")

    batch_dirs = [case_dir, qc_dir]

    GCQUANTMETHODS = ['COTHC', 'SQGHB', 'SQETGLYCOL', 'QTTRAMADOL', 'QTZOLPIDEM', 'QTOPIATE']
    #init list to store sample class
    all_samples = []
    #check CASE DATA and BATCH PACK DATA
    for dirs in batch_dirs:
        print(f"checking {dirs}")
        if method == 'SQVOL':
            samples = sqvol_init.sqvol_init(dirs)
        elif method in GCQUANTMETHODS:
            print('starting scion init')
            samples = scion_init.GC_quant_init(dirs)
        else:
            samples = shimadzu_init.LC_quant_init(dirs)
        all_samples.extend(samples)

    if len(all_samples) == 0:
        print("CRITICAL ERROR - unable to find data -- is it in the CASE DATA and/or BATCH PACK DATA folder?")


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
        print('starting ISAR fill', flush=True)
        if len(controls) >= 4:
            print("getting blood ISAR")
            output_path = searcher.copy_file(aux_func.get_ISAR(method,TP_directory), output_dir, "ISAR_blood")
            filler.ISAR_fill(controls, batch, output_path)
            
        if len(serum_controls) >= 4:
            print("getting serum ISAR")
            output_path_s = searcher.copy_file(aux_func.get_ISAR(method,TP_directory), output_dir, "ISAR_serum")
            filler.ISAR_fill(serum_controls, batch, output_path_s)
    except Exception as e:
        print(f"--error-- unable to retrieve/fill ISAR | {e}")

    #LJ output
    try:
        LJ_path = filler.output_LJ_2(controls, serum_controls, batch, output_dir, extraction_date)
        print("LJ excel sheet successfully created! - Filled CTL data")
    except Exception as e:
        print(f"--error-- unable to fill LJ - CTL ISSUE | {e}")
    # try:
    #     #print(curve)
    #     LJ_path = filler.append_LJ_curve(curve, batch, output_dir, extraction_date, initials)
    #     print("LJ excel sheet successfully appended! - Filled Curve data")
    # except Exception as e:
    #     print(f"--error-- unable to fill LJ - CURVE ISSUE | {e}")
    try:
        searcher.copy_excel(LJ_path, qc_dir, 'LJ')
    except Exception as e:
        print(f"--error moving LJ-- | {e}")

    #send case-list to binder, bind duplicates -- return list of singles
    try:
        leftovers = aux_func.compare_and_bind_duplicates(cases, output_dir, batch)
        #singles handler
        if len(leftovers) > 0:
            aux_func.move_singles(leftovers, output_dir, batch)
    except Exception as e:
        print(f'error finding/binding duplicates | {e}')
   
    #MSA handler
    if len(MOA_cases) > 0:
        sliced_MOA = aux_func.MOA_slicer(MOA_cases)
        for case_list in sliced_MOA:
            positive_analytes = filler.interpret_MSA(case_list)
            try:
                for analyte in positive_analytes:
                    MSA_path = searcher.copy_excel(aux_func.get_MSA(LF_directory), output_dir, f"{case_list[0].base}_{analyte}")
                    #create excel file here using case_list
                    filler.fill_MSA(case_list, batch, MSA_path, analyte, method)
            except Exception as e:
                print(f"--error-- filling MSA | {e}")   

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

    #return files to individual directory
    searcher.ShuttleHome(case_dir)
    
    print("END SCRIPT", flush=True)

if __name__ == "__main__":
    #print(ascii_art)
    print(f"sys.argv: {sys.argv}")
    print('hit start')

    logger = logging.getLogger("quants")

    # Use CLI provided arguments
    batch = sys.argv[1]
    method = sys.argv[2].upper()

    print('start main')
    # Call the main function with the provided or inputted arguments
    main(batch, method)
    logger.info("Completed batch %s", batch)

