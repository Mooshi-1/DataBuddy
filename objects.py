# -*- coding: utf-8 -*-
"""
Created on Thurs 01/09/2025

@author: Giachetti
"""


from enum import Enum
import re


class QCTYPE(Enum):
    SR = 'spiked recovery'
    DL = 'dilution'
    CTL = 'control'
    CAL = 'calibrator'
    SH = 'shooter'
    MOA = 'method of addition'
    SEQ = 'sequence'
    CUR = 'curve'
    NEG = 'negative'

    #can add multiple 
    #type=[QCTYPE.SR, QCTYPE.DL, etc]



# def QC_handler(samples):

#     if self.type == QCTYPE.SR:
#         pass
#         #function to check dependent cases and fill out worksheet
    
#     #brain/liver/gastric/blood? method of addition
#     if self.type == [QCTYPE.MOA, QCTYPE.]:
#         pass
#         #function to assemble surve
#     raise Exception("Invalid QC")

def case_handler(self, other):
    if self.ID == other.ID:
        pass
        #bind the pdf paths
    
#define QC objects
class Sample:
    def __init__(self, ID, path, base, type=None, results_ISTD=None, results_analyte=None):
        self.ID = ID
        self.path = path
        self.base = base
        self.type = set(type) if type is not None else set()
        self.results_ISTD = results_ISTD if results_ISTD is not None else []
        self.results_analyte = results_analyte if results_analyte is not None else []

    def assign_type(self):
        big_dilution = re.compile(r'x(1[1-9]|[2-9][0-9]+|[1-9][0-9]{2,})')
        dilution = re.compile(r'x[1-9]')
        MOA = ["BRN", "LIV", "GLG"]
        MOA_cal = ["_L1", "_L2", "_L3", "_L4", "_L5", "_L6"]
        SR = "_SR"
        CAL = "CAL"
        CTL = "CTL"
        SH = "SHOOTER"
        NEG = "NEG"

        if self.type == QCTYPE.SEQ or self.type == QCTYPE.CUR:
            return

        if big_dilution.search(self.ID):
            self.type.add(QCTYPE.MOA)
            self.type.add(QCTYPE.DL)

        if dilution.search(self.ID):
            self.type.add(QCTYPE.DL)

        for cal in MOA_cal:
            if cal in self.ID:
                self.type.add(QCTYPE.CAL)
                self.type.add(QCTYPE.MOA)
    
        for types in MOA:
            if types in self.ID:
                self.type.add(QCTYPE.MOA)

        if SR in self.ID:
            self.type.add(QCTYPE.SR)

        if CAL in self.ID:
            self.type.add(QCTYPE.CAL)

        if CTL in self.ID:
            self.type.add(QCTYPE.CTL)

        if SH in self.ID:
            self.type.add(QCTYPE.SH)
        
        if NEG in self.ID:
            self.type.add(QCTYPE.NEG)



    def __eq__(self, other):
        return self.base == other.base

    
    def __hash__(self):
        return hash(self.ID)

    def compare_qc(self, other):
        return self.type == other.type
        
    def __repr__(self):
        return f"{self.ID}, QC={self.type}, {len(self.results_ISTD)} ISTD {len(self.results_analyte)} analyte, +.path"
    
    

# class QC(Sample):
#     def __init__(self, ID, path, type, results_ISTD, results_analyte):
#         super().__init__(ID, path, type, results_ISTD, results_analyte)

def table_converter(table):
    #prep new columns
    keywords = ["ID#", "Name", "Ret. Time (min)", "Area", "Quant Ion (m/z)", "Conc.", "Unit", "Mode"]
    columns = {key: [] for key in keywords}
    current_keyword = None

    #populate sublists based on keywords
    for line in table:
        if line in keywords:
            current_keyword = line
        if current_keyword:
            columns[current_keyword].append(line)

    #ensure that all lists are same length by appending empty strings
    max_length = max([len(columns[key]) for key in keywords])
    for key in keywords:
        while len(columns[key]) < max_length:
            columns[key].append("")

    #create list of sublists to transpose, then zip
    data = [columns[key] for key in keywords]
    transposed_table = list(zip(*data))

    #debug print statements
    #for row in transposed_table:
        #print(", ".join(row))
    #print(transposed_table)
    return transposed_table


if __name__ == "__main__":
    tester1 = Sample("24-3456_IVBGT_x10", r"/home/mooshi_1/workspace/github.com/Mooshi-1/Work/locked/private/12786/CASE DATA/24-3456_IVBGT_x10.pdf", None, ["Morphine", "Codeine"], ["Morphine", "Codeine"])
    tester2 = Sample("24-3456_IVBGT_x10_1", r"/home/mooshi_1/workspace/github.com/Mooshi-1/Work/locked/private/12786/CASE DATA/24-3456_IVBGT_x10_1.pdf", None, ["Morphine", "Codeine"], ["Morphine", "Codeine"])
    tester3 = Sample("24-3560_BRNCUP_x2_L1", r"/home/mooshi_1/workspace/github.com/Mooshi-1/Work/locked/private/12786/CASE DATA/24-3560_BRNCUP_x2_L1.pdf", None, ["Morphine", "Codeine"], ["Morphine", "Codeine"])
    samples = [tester1, tester2, tester3]

    for sample in samples:
        sample.assign_type()
    print(samples)