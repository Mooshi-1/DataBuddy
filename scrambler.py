# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 14:41:10 2024

@author: e314883
"""
import os

input_dir = r"C:\Users\e314883\Desktop\python pdf\raw_tests"

def scrambler(input_dir):
    counter = 000
    
    for filename in os.listdir(input_dir):
        #os.rename(old-file, new-file)
        os.rename(os.path.join(input_dir, filename), os.path.join(input_dir, f"reset-{counter:03d}.pdf"))
        print(f"renamed {filename} to reset-{counter:03d}")
        counter += 1
        
scrambler(input_dir)