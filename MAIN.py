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
    
    print("finding batch...")
    for year in os.listdir(data_dir):
        year_dir = os.path.join(data_dir, year)
        if not os.path.isdir(year_dir):
            continue
        
        for month in os.listdir(year_dir):
            month_dir = os.path.join(year_dir, month)
            if not os.path.isdir(month_dir):
                continue
            
            for batch in os.listdir(month_dir):
                if batch == str(batch_num):
                    print(f"found batch {batch_num}")
                    
                    case_dir = os.path.join(month_dir, batch, "CASE DATA")
                    print(f"Case Directory = {case_dir}")
                    qc_dir = os.path.join(month_dir, batch, "BATCH PACK DATA")
                    print(f"QC Directory = {qc_dir}")
                    
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