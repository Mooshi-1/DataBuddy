from seq_init import sequence
from sample_dict import caboose

# class sequence():
#     def __init__(self, sample_number, sample_type, sample_container, barcode, abbrv=None):
#         self.number = sample_number
#         self.type = sample_type
#         self.container = sample_container
#         self.barcode = barcode
#         self.abbrv = "" if abbrv is None else abbrv

#screens

def make_solvent():
    if not hasattr(make_solvent, "counter"):
        make_solvent.counter = 0
    make_solvent.counter += 1
    return sequence(f'S{make_solvent.counter}', 'SOLVENT', '', f'S{make_solvent.counter}', f'S{make_solvent.counter}')

def make_pos_ctl():
    if not hasattr(make_pos_ctl, "counter"):
        make_pos_ctl.counter = 0
    make_pos_ctl.counter += 1
    return sequence(f'P{make_pos_ctl.counter}', 'POS CTL', '', f'P{make_pos_ctl.counter}', f'POS CTL {make_pos_ctl.counter}')

def make_neg_ctl():
    if not hasattr(make_neg_ctl, "counter"):
        make_neg_ctl.counter = 0
    make_neg_ctl.counter += 1
    return sequence(f'N{make_neg_ctl.counter}', 'NEG CTL', '', f'N{make_neg_ctl.counter}', f'NEG CTL {make_neg_ctl.counter}')

#quants

def make_shooter():
    if not hasattr(make_shooter, "counter"):
        make_shooter.counter = 0
    make_shooter.counter += 1
    return sequence(f'SHOOTER {make_shooter.counter}', 'SHOOTER', '', f'SHOOTER {make_shooter.counter}', f'SHOOTER {make_shooter.counter}')

#for curve, add cal# arg and call .extend
def make_curve(CALS):
    curve_list = []
    for i in range(1, CALS):
        curve_list.append(sequence(f'CAL L{i}', f'CAL L{i}', '', f'CAL L{i}', f'CAL L{i}'))
    return curve_list

#call .extend
def make_LH(init_counter=None):
    if init_counter is not None:
        make_LH.counter = init_counter
    elif not hasattr(make_LH, "counter"):
        make_LH.counter = 0
    make_LH.counter += 1
    return [
        sequence(f'CTL LOW {make_LH.counter}', 'LOW CTL', '', f'CTL LOW {make_LH.counter}', f'CTL LOW {make_LH.counter}'),
        sequence(f'CTL HIGH {make_LH.counter}', 'HIGH CTL', '', f'CTL HIGH {make_LH.counter}', f'CTL HIGH {make_LH.counter}')
    ]

nested_list = [[1, 2], [3, 4], [5, 6]]
flattened_list = [item for sublist in nested_list for item in sublist]
print(flattened_list)  # Output: [1, 2, 3, 4, 5, 6]

nested_list = [[23-1, 23-2, 23-3], [24-01, 24-02, 24-03], [25-1, 25-2, 25-3]]
new_list = [23-4, 23-5, 23-6]

# Insert at the second position (index 1)
nested_list.insert(1, new_list)
print(nested_list)

nested_list = [[23-1, 23-2, 23-3], [24-01, 24-02, 24-03], [25-1, 25-2, 25-3]]
new_list = [26-1, 26-2, 26-3]

# Append at the end
nested_list.append(new_list)
print(nested_list)

#insert backwards to avoid indices getting messed up
def duplicate_quants():
    # Original list
    original_list = ["24-01", "24-02", "24-03"]

    # Intertwine the two lists
    duplicate_list = []
    for item in original_list:
        duplicate_list.append(item)
        duplicate_list.append(item)
        duplicate_list.append(make_solvent())

    print(duplicate_list)


def handle_special():
    pass


def slice_case_list(samples, interval):
    sliced_cases = []



def SCRNZ_seq(samples, interval):
    scrnz_samples = []
    i = 0
    bad_matrix = []

    temp = samples.copy()

    for i in range(len(temp)):
        if samples[i].type in caboose:
            bad_matrix.append(samples.pop(i))

    bad_matrix = sorted(bad_matrix, key=lambda x: list(caboose.keys()).index(x.type))
    
    samples.extend(bad_matrix)

    scrnz_samples.append(make_solvent())
    scrnz_samples.append(make_neg_ctl())
    scrnz_samples.append(make_pos_ctl())
    scrnz_samples.append(make_solvent())
    while i < len(samples):
        scrnz_samples.extend(samples[i:i + interval])
        scrnz_samples.append(make_solvent())
        scrnz_samples.append(make_pos_ctl())
        scrnz_samples.append(make_solvent())
        i += interval

    return scrnz_samples



#consider making case blocks?
#replace block by finding index of case block
#then SCREENS[(block_index):(block_index)+1] = [list of cases]

def quants(samples, interval):
    blood_quants = []
    serum_quants = []
    if any(case.type)
    i = 0

    blood_quants.append(make_solvent())
    blood_quants.append(make_shooter())
    blood_quants.append(make_neg_ctl())
    blood_quants.extend(make_curve(6))
    blood_quants.extend(make_LH())
    blood_quants.append(make_solvent())



    for case in samples:
        
            blood_quants.append(samples[i:i + interval])


    if any('SERUM' in sample.type for sample in samples):
