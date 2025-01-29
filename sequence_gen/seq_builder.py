from seq_init import sequence

# class sequence():
#     def __init__(self, sample_number, sample_type, sample_container, barcode, abbrv=None):
#         self.number = sample_number
#         self.type = sample_type
#         self.container = sample_container
#         self.barcode = barcode
#         self.abbrv = "" if abbrv is None else abbrv

def make_solvent():
    counter = 0
    counter += 1
    return sequence('S1', 'SOLVENT', None, None, None, None)

def screens(samples, interval):
    
    new_list = []
    i = 0
    while i < len(samples):
        new_list.extend(samples[i:i + 20])
        new_list.append("S")
        i += 20
    return new_list

