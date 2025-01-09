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
    def __init__(self, ID, path, type=None, results_ISTD=None, results_analyte=None):
        self.ID = ID
        self.path = path
        self.type = type if type is not None else []
        self.results_ISTD = results_ISTD if results_ISTD is not None else []
        self.results_analyte = results_analyte if results_analyte is not None else []

    def __eq__(self, other):
        if isinstance(other, Sample):
            return self.ID == other.ID
        return False
    
    def __hash__(self):
        return hash(self.ID)

    def compare_qc(self, other):
        return self.type == other.type
        
    def __repr__(self):
        return f"{self.ID}, QC={self.type}, {len(self.results_ISTD)} ISTD {len(self.results_analyte)} analyte, +.path"

class QC(Sample):
    def __init__(self, ID, path, type, results_ISTD, results_analyte):
        super().__init__(ID, path, type, results_ISTD, results_analyte)

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


