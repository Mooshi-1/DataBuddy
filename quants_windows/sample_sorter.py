# -*- coding: utf-8 -*-
"""
Created on Thurs 01/09/2025

@author: ADG
"""
from enum import Enum
import re

##class definitions, then broader sort functions

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
        big_dilution = re.compile(r'x(1[1-9]|[2-9][0-9]+|[1-9][0-9]{2,})', re.IGNORECASE)
        dilution = re.compile(r'x(10|[1-9])', re.IGNORECASE)
        MOA_type = ["BRN", "LIV", "GLG"]
        MOA_cal = ["_L0", "_L1", "_L2", "_L3", "_L4", "_L5", "_L6"]
        SR_type = ["_SR", '_x%R', '_%R']
        CAL = "CAL"
        CTL = "CTL"
        SH = "SHOOTER"
        NEG = "NEG"
        #assign QCTYPE by various means. must be of Sample class
        if self.type == QCTYPE.SEQ or self.type == QCTYPE.CUR:
            return #assigned at init, could always create logic
        if big_dilution.search(self.ID):
            self.type.add(QCTYPE.MOA)
            self.type.add(QCTYPE.DL)
        if dilution.search(self.ID):
            self.type.add(QCTYPE.DL)
        for cal in MOA_cal:
            if cal in self.ID:
                self.type.add(QCTYPE.CAL)
                self.type.add(QCTYPE.MOA)
        for types in MOA_type:
            if types in self.ID:
                self.type.add(QCTYPE.MOA)
        for vars in SR_type:
            if vars in self.ID:
                self.type.add(QCTYPE.SR)
        if CAL in self.ID:
            self.type.add(QCTYPE.CAL)
        if CTL in self.ID:
            self.type.add(QCTYPE.CTL)
        if SH in self.ID:
            self.type.add(QCTYPE.SH)
        if NEG in self.ID:
            self.type.add(QCTYPE.NEG)

    #ID is unique so using self.base for comparisons -- duplicate checker uses this
    def __eq__(self, other):
        return self.base == other.base
    #currently unused
    def __hash__(self):
        return hash(self.ID)
    #currently unused
    def compare_qc(self, other):
        return self.type == other.type
    #used for debugging
    def __repr__(self):
        return f"({self.ID}, {self.type}, {self.base}, {self.results_ISTD}, {self.results_analyte}, r{self.path!r})"
    #used for quick checks
    def __str__(self):
        return f"({self.base}, {self.type}, analytes={len(self.results_analyte)}, ISTDs={len(self.results_ISTD)})"
    

##below is not part of class

#general purpose sorting, calibrators, numerical sequences
def general_sort_key(sample):
    # extract numerical parts for sorting
    remove_suffix = re.sub(r'_0$', '', sample.ID)
    parts = re.findall(r'\d+', remove_suffix)
    parts = [int(part) for part in parts]
    return parts
def sort_samples(list):
    list.sort(key=general_sort_key)

#ensures low then high control for quant batches
def control_sort_key(sample):
    #sorts low 1 - high 1 - low 2 etc 
    match = re.match(r'(LOW|HIGH) CTL (\d+)', sample.base)
    if match:
        control_type, num = match.groups()
        #assign weight so low comes first
        weight = 0 if control_type == 'LOW' else 1
        return (int(num), weight)
    return (sample.base,)
def sort_controls(list):
    list.sort(key=control_sort_key)

#assigns samples into lists - must have sample.type
def sample_handler(all_samples):
    cal_curve = []
    neg_ctl = []
    shooter = []
    controls = []
    dil_controls = []
    SR_cases = []
    cases = []
    curve = []
    MOA_cases = []
    sequence = []
    for sample in all_samples:
        if sample.type == {QCTYPE.CAL}:
            cal_curve.append(sample)
        elif sample.type == {QCTYPE.SEQ}:
            sequence.append(sample)
        elif sample.type == {QCTYPE.CUR}:
            curve.append(sample)
        elif sample.type == {QCTYPE.SH}: 
            shooter.append(sample)
        elif sample.type.issuperset({QCTYPE.NEG,QCTYPE.CTL}):
            neg_ctl.append(sample)
        elif sample.type == {QCTYPE.CTL}:
            controls.append(sample)
        elif sample.type.issuperset({QCTYPE.DL,QCTYPE.CTL}):
            dil_controls.append(sample)
        elif QCTYPE.SR in sample.type:
            SR_cases.append(sample)
        elif QCTYPE.MOA in sample.type:
            MOA_cases.append(sample)
        else:
            cases.append(sample)
    #note that controls got a seperate sort method
    #return sorted lists
    try:
        sort_samples(cal_curve); sort_samples(neg_ctl); sort_samples(shooter)
        sort_controls(controls); sort_samples(dil_controls); sort_samples(SR_cases)
        sort_samples(cases); sort_samples(curve); sort_samples(MOA_cases); sort_samples(sequence)
    except Exception as e:
        print(f"error sorting files | {e}")


    return cal_curve, neg_ctl, shooter, controls, dil_controls, SR_cases, cases, curve, MOA_cases, sequence


if __name__ == "__main__":
    #tester1 = Sample("24-3456_IVBGT_x10", r"/home/mooshi_1/workspace/github.com/Mooshi-1/Work/locked/private/12786/CASE DATA/24-3456_IVBGT_x10.pdf", None, ["Morphine", "Codeine"], ["Morphine", "Codeine"])
    #tester2 = Sample("24-3456_IVBGT_x10_1", r"/home/mooshi_1/workspace/github.com/Mooshi-1/Work/locked/private/12786/CASE DATA/24-3456_IVBGT_x10_1.pdf", None, ["Morphine", "Codeine"], ["Morphine", "Codeine"])
    #tester3 = Sample("24-3560_BRNCUP_x2_L1", r"/home/mooshi_1/workspace/github.com/Mooshi-1/Work/locked/private/12786/CASE DATA/24-3560_BRNCUP_x2_L1.pdf", None, ["Morphine", "Codeine"], ["Morphine", "Codeine"])
    tester4 = Sample("DIL CTLx10_0", r"C:\Users\e314883\Desktop\locked_git_repo\12786\CASE DATA\CAL1_0.pdf", "DIL CTLx10", None, None, None)
    samples = [tester4]

    for sample in samples:
        sample.assign_type()
