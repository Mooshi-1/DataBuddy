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

def main(input_dir, output_dir, batch_num, method):
    print(f"Input Directory: {input_dir}")
    print(f"Output Directory: {output_dir}")
    print(f"Batch Number: {batch_num}")
    print(f"{method}")
    
    if method == "SCGEN":
        SCGEN_OMNI.GENrename(input_dir)
        SCGEN_OMNI.GENbinder(input_dir, output_dir, batch_num)
        SCGEN_OMNI.GENcontrols(output_dir, batch_num)

    if method == "SCRNZ":
        SCRNZ_omni.Zrename(input_dir)
        SCRNZ_omni.Zbinder(input_dir, output_dir, batch_num)
        SCRNZ_omni.Zcontrols(output_dir, batch_num)
        
input_dir = r"C:\Users\e314883\Desktop\python pdf\raw_tests"
output_dir = r"C:\Users\e314883\Desktop\python pdf\op_tests"
batch_num = 111
method = "SCGEN"
main(input_dir, output_dir, batch_num, method)

if __name__ == "__main__":
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    batch_num = sys.argv[3]
    method = sys.argv[4]
    main(input_dir, output_dir, batch_num, method)