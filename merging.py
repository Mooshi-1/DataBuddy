# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 13:15:41 2024

@author: e314883
"""

import pymupdf

doc_a = pymupdf.open("a.pdf") # open the 1st document
doc_b = pymupdf.open("b.pdf") # open the 2nd document

doc_a.insert_pdf(doc_b) # merge the docs
doc_a.save("a+b.pdf") # save the merged document with a new filename