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
import os

import searcher
import SCRNZ_omni
import SCGEN_OMNI
import SCLCMSMS_OMNI


ascii_art = """
 .
 ooo        ooooo oooooooooo.   ooo        ooooo oooooooooooo      ooooooooooooo   .oooooo.   ooooooo  ooooo 
 `88.       .888' `888'   `Y8b  `88.       .888' `888'     `8      8'   888   `8  d8P'  `Y8b   `8888    d8'  
  888b     d'888   888      888  888b     d'888   888                   888      888      888    Y888..8P    
  8 Y88. .P  888   888      888  8 Y88. .P  888   888oooo8              888      888      888     `8888'     
  8  `888'   888   888      888  8  `888'   888   888    "              888      888      888    .8PY888.    
  8    Y     888   888     d88'  8    Y     888   888       o           888      `88b    d88'   d8'  `888b   
 o8o        o888o o888bood8P'   o8o        o888o o888ooooood8          o888o      `Y8bood8P'  o888o  o88888o 
 
 oooooooooo.                 .                  oooooooooo.   o8o                    .o8                     
 `888'   `Y8b              .o8                  `888'   `Y8b  `"'                   "888                     
  888      888  .oooo.   .o888oo  .oooo.         888     888 oooo  ooo. .oo.    .oooo888   .ooooo.  oooo d8b 
  888      888 `P  )88b    888   `P  )88b        888oooo888' `888  `888P"Y88b  d88' `888  d88' `88b `888""8P 
  888      888  .oP"888    888    .oP"888        888    `88b  888   888   888  888   888  888ooo888  888     
  888     d88' d8(  888    888 . d8(  888        888    .88P  888   888   888  888   888  888    .o  888     
 o888bood8P'   `Y888""8o   "888" `Y888""8o      o888bood8P'  o888o o888o o888o `Y8bod88P" `Y8bod8P' d888b    
 .
Version 1.05 - 01/09/2025
"""

def main(batch_num, method):
    print(f"Batch Number: {batch_num}")
    print(f"Method: {method}")
    
    data_dir = r"G:\PDF DATA"
    print(f"Starting in: {data_dir}")
    
    #call FindBatch function to locate directories
    case_dir, qc_dir = searcher.FindBatch(data_dir, batch_num)
    if case_dir and qc_dir == None:
        raise Exception("Unable to locate batch directory")                
    
    #create binder output
    output_dir = searcher.binder_dir(case_dir)
    print(f"Output Directory: {output_dir}")
    
    #move files from individual folders
    searcher.Shuttle(case_dir)

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
            
    #return files to individual directory
    searcher.ShuttleHome(case_dir)
    
if __name__ == "__main__":
    print(ascii_art)
    # Check if the required arguments are passed via sys.argv
    if len(sys.argv) < 3:
        batch_num = input("Enter the batch number: ")
        method = input("Enter the method (SCGEN, SCRNZ, SCLCMSMS): ")
        input("Reminder: Unable to handle reinjects. Bind your sequence manually. Press Enter to continue...")
    else:
        # Use CLI provided arguments
        batch_num = sys.argv[1]
        method = sys.argv[2]

    # Call the main function with the provided or inputted arguments
    main(batch_num, method)

    input("Press Enter to exit...")
