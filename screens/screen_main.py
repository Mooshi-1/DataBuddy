# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 12:21:22 2024

@author: e314883
"""
#pyinstaller main.py -- to package .exe file
#make shortcut from dist folder
#export QC data to pdf
#handle reinjects
#integrate sequence generation from test batch
##export sequence as pdf
#use pyinstaller or py2exe libs to create .exe file

import sys
import logging

import searcher
import SCRNZ_omni
import SCGEN_OMNI
import SCLCMSMS_OMNI


ascii_art = """
███████╗ ██████╗██████╗ ███████╗███████╗███╗   ██╗
██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝████╗  ██║
███████╗██║     ██████╔╝█████╗  █████╗  ██╔██╗ ██║
╚════██║██║     ██╔══██╗██╔══╝  ██╔══╝  ██║╚██╗██║
███████║╚██████╗██║  ██║███████╗███████╗██║ ╚████║
╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝
                                                  
██████╗ ██╗███╗   ██╗██████╗ ███████╗██████╗      
██╔══██╗██║████╗  ██║██╔══██╗██╔════╝██╔══██╗     
██████╔╝██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝     
██╔══██╗██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗     
██████╔╝██║██║ ╚████║██████╔╝███████╗██║  ██║     
╚═════╝ ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝     
                                                 
Version 1.10 - 02/06/2025
"""

def main(batch_num, method, flag=None):
    print(f"Batch Number: {batch_num}")
    print(f"Method: {method}")
    
    data_dir = r"G:\PDF DATA"
    print(f"Starting in: {data_dir}")
    
    #call FindBatch function to locate directories
    case_dir, qc_dir = searcher.FindBatch(data_dir, batch_num)
    if case_dir is None and qc_dir is None:
        raise Exception("Unable to locate batch directory")

    def renamer_mode(case_dir, qc_dir, method):
        try:
            while True:
                print("Options:")
                print("r = Run method renamer in BATCH PACK DATA/CASE DATA")
                print("e = move files from individual folders and place in CASE DATA")
                print("p = move files from CASE DATA into individual folders")
                print("q = Quit")
                print("bind = exit rename mode and continue immediately to binder")

                choice = input("Enter your choice: ").strip().lower()

                if choice == "r":
                    print("Renaming files in BATCH PACK DATA and CASE DATA")
                    if method == "SCGEN":
                        SCGEN_OMNI.GENrename(case_dir);SCGEN_OMNI.GENrename(qc_dir)
                    if method == "SCRNZ":
                        SCRNZ_omni.Zrename(case_dir);SCRNZ_omni.Zrename(qc_dir)
                    if method == "SCLCMSMS":
                        SCLCMSMS_OMNI.LCMSrename(case_dir);SCLCMSMS_OMNI.LCMSrename(qc_dir)
                elif choice == "e":
                    print("Running searcher.Shuttle...")
                    searcher.Shuttle(case_dir)
                elif choice == "p":
                    print("Running searcher.ShuttleHome...")
                    searcher.ShuttleHome(case_dir)
                elif choice == "q":
                    print("Exiting Renamer Mode.")
                    sys.exit()
                elif choice == "bind":
                    break
                else:
                    print("Invalid choice. Please try again.")
        except Exception as e:
            print(f'theres been an error. please save screenshot/copy this to adg | {e}')
            print(f'-----------restarting renamer mode-------------')
            renamer_mode(case_dir, qc_dir, method)

    if flag == "-r" or flag == "-R":
        input("Entering Renamer Mode, press Enter to continue")
        renamer_mode(case_dir, qc_dir, method)
    
    #create binder output
    output_dir = searcher.binder_dir(case_dir)
    print(f"Output Directory: {output_dir}")
    
    #move files from individual folders
    searcher.Shuttle(case_dir)

    try:
        if method == "SCGEN":
            SCGEN_OMNI.GENrename(case_dir)
            SCGEN_OMNI.GENbinder(case_dir, output_dir, batch_num)
            SCGEN_OMNI.GENrename(qc_dir)
            SCGEN_OMNI.GENbinder(qc_dir, output_dir, batch_num)        
            SCGEN_OMNI.GENcontrols(output_dir, batch_num)

        if method == "SCRNZ":
            SCRNZ_omni.Zrename(case_dir)
            SCRNZ_omni.Zbinder(case_dir, output_dir, batch_num)
            SCRNZ_omni.Zrename(qc_dir)
            SCRNZ_omni.Zbinder(qc_dir, output_dir, batch_num)
            SCRNZ_omni.Zcontrols(output_dir, batch_num)
        
        if method == "SCLCMSMS":
            SCLCMSMS_OMNI.LCMSrename(case_dir)
            SCLCMSMS_OMNI.LCMSbinder(case_dir, output_dir, batch_num)
            SCLCMSMS_OMNI.LCMSrename(qc_dir)
            SCLCMSMS_OMNI.LCMSbinder(qc_dir, output_dir, batch_num)
            SCLCMSMS_OMNI.LCMScontrols(output_dir, batch_num)
    except Exception as e:
        print(f'theres been an error. please save screenshot/copy this to adg | {e}')
            
    #return files to individual directory
    searcher.ShuttleHome(case_dir)
    
if __name__ == "__main__":
    print(ascii_art)
    print(f"sys.argv: {sys.argv}")
    logger = logging.getLogger(__name__)

    # Check if the required arguments are passed via sys.argv
    if len(sys.argv) < 4:
        batch_num = input("Enter the batch number: ")
        method = input("Enter the method (SCGEN, SCRNZ, SCLCMSMS): ").upper()
        flag = input("Reminder: Unable to handle reinjects. Bind your sequence manually. Press Enter to continue... or -r to enter naming mode")
    else:
        # Use CLI provided arguments
        batch_num = sys.argv[1]
        method = sys.argv[2].upper()
        flag = sys.argv[3]

    try:
        logger.info("Starting screen batch %s",batch_num)
        main(batch_num, method, flag)
        logger.info("Completed batch %s",batch_num)
    except Exception as e:
        logger.error("Could not run batch %s: %s", batch_num, e)