from enum import Enum

class QCTYPE(Enum):
    SR = 'spiked recovery'
    DL = 'dilution'
    CTL = 'control'
    CAL = 'calibrator'
    SH = 'shooter'
    MOA = 'method of addition'
    SEQ = 'sequence'
    CUR = 'curve'

    #can add multiple 
    #type=[QCTYPE.SR, QCTYPE.DL, etc]

def QC_handler(self):
    if self.type == QCTYPE.SR:
        pass
        #function to check dependent cases and fill out worksheet
    if self.type == [QCTYPE.MOA]:
        pass
        #function to assemble surve
    raise Exception("Invalid QC")

def case_handler(self, other):
    if self.ID == other.ID:
        pass
        #bind the pdf paths
    
#define QC objects
class Sample:
    def __init__(self, ID, path, type=None, results=None):
        self.ID = ID
        self.path = path
        self.type = type if type is not None else []
        self.results = results
        
        self.cleaned_results = self.clean_data()

    def clean_data(self):
        pass
#         # Storing data as a list of dictionaries
#get it to look like this
# data = [
#     {"drug name": "morphine", "area counts": 6000000, "retention time": "0.23 min", "concentration": "0.03 mg/L"},
#     {"drug name": "codeine", "area counts": 7000000, "retention time": "2.5 min", "concentration": "0.10 mg/L"},

    def __repr__(self):
        return f"{self.ID}, QC={self.type}, +.results, +.path"

class QC(Sample):
    def __init__(self, ID, type, results, path):
        super().__init__(ID, type, results, path)

#example = Sample(QCTYPE.SR, None, pdf_path)
#any subclasses needed?