from enum import Enum

class QCTYPE(Enum):
    SR = 'spiked recovery'
    DL = 'dilution'
    CTL = 'control'
    CAL = 'calibrator'
    SH = 'shooter'
    MOA = 'method of addition'

def QC_handler(self):
    if self.type == QCTYPE.SR:
        pass
    raise Exception("Invalid QC")
    
#define QC objects
class Sample:
    def __init__(self, ID, type, results, path):
        self.ID = ID
        self.type = type
        self.results = results
        self.path = path
        self.cleaned_results = self.clean_data()

    def clean_data(self):
        pass

class QC(Sample):
    def __init__(self, ID, type, results, path):
        super().__init__(ID, type, results, path)

#example = Sample(QCTYPE.SR, None, pdf_path)
#any subclasses needed?