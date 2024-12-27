# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 14:41:10 2024

@author: e314883
"""
import os

def scrambler(input_dir):
    counter = 00
    
    for filename in os.listdir(input_dir):
        print(filename)
        filename.save(os.path.join(input_dir, f"reset-{counter}.pdf"))
        print("renamed {filename} to reset-{counter}")
        counter += 1