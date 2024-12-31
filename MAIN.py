# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 12:21:22 2024

@author: e314883
"""

#export QC data to pdf
#handle reinjects
#integrate sequence generation from test batch
##export sequence as pdf
#use pyinstaller or py2exe libs to create .exe file

import sys
import os
import SCGEN_OMNI
import SCRNZ_omni
import searcher
import SCLCMSMS_OMNI

##testing comments
##batch_num = 12777
##method = "SCRNZ"

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
    
##testing comment
##main(batch_num, method)

if __name__ == "__main__":
    batch_num = sys.argv[1]
    method = sys.argv[2]
    main(batch_num, method)