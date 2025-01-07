# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 14:41:10 2024

@author: e314883
"""
import os

input_dir = r"G:\PDF DATA\2024\12\12757\CASE DATA"

def scrambler(input_dir):
    counter = 000
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            try:
                #os.rename(old-file, new-file)
                os.rename(os.path.join(input_dir, filename), os.path.join(input_dir, f"reset-{counter:03d}.pdf"))
                print(f"renamed {filename} to reset-{counter:03d}")
                counter += 1
            except:
                continue
scrambler(input_dir)