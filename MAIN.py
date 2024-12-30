# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 12:21:22 2024

@author: e314883
"""

#export QC data to pdf
#handle reinjects
#integrate sequence generation from test batch
##export sequence as pdf


import sys
#import os
import SCGEN_OMNI
import SCRNZ_omni
import searcher
import SCLCMSMS_OMNI

def main(input_dir, batch_num, method):
    print(f"Input Directory: {input_dir}")
    print(f"Batch Number: {batch_num}")
    print(f"{method}")
    
#take it a step further, just ask for batch number
#need a way to point to batch pack data and get QC files

#need a way to move files back in after bind

    output_dir = searcher.binder_dir(input_dir)
    print(f"Output Directory: {output_dir}")
    searcher.Shuttle(input_dir)

    if method == "SCGEN":
        SCGEN_OMNI.GENrename(input_dir)
        SCGEN_OMNI.GENbinder(input_dir, output_dir, batch_num)
        SCGEN_OMNI.GENcontrols(output_dir, batch_num)

    if method == "SCRNZ":
        SCRNZ_omni.Zrename(input_dir)
        SCRNZ_omni.Zbinder(input_dir, output_dir, batch_num)
        SCRNZ_omni.Zcontrols(output_dir, batch_num)
    
    if method == "SCLCMSMS":
        SCLCMSMS_OMNI.LCMSrename(input_dir)

        
input_dir = r"C:\Users\e314883\Desktop\python pdf\raw_tests"
batch_num = 111
method = "SCGEN"
main(input_dir, batch_num, method)

if __name__ == "__main__":
    input_dir = sys.argv[1]
    batch_num = sys.argv[2]
    method = sys.argv[3]
    main(input_dir, batch_num, method)