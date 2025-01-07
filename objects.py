from enum import Enum

class QCTYPE(Enum):
    SR = 'spiked recovery'
    DL = 'dilution'
    CTL = 'control'
    CAL = 'calibrator'
    SH = 'shooter'
    MOA = 'method of addition'


#define QC objects
class QC:
    def __init__(self, type, worksheet, path):
        self.type = type
        self.worksheet = worksheet
        self.path = path

#any subclasses needed?