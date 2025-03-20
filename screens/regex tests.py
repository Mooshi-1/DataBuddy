# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 12:48:59 2024

@author: e314883
"""
import re

def main(string):
    pattern = re.compile(r'(\d+-\d+_.+ [AB])')
    match = pattern.search(string)
    if match:
        return f"Match found: {match.group(1)}"
    else:
        return "No match found"

# Example usage
print(main(r"24-3158_livx5 A Data File Path"))