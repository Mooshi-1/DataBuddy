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

def make_diln(value):
    return sequence(f'DILN CTL {value}', 'CTL', '', f'DILN CTL {value}', f'DILN CTL {value}')

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

def sort_quants(samples):

    bad_matrix = []
    priority = []

    temp = samples.copy()

    for i in range(len(temp) -1, -1, -1):
        if hasattr(temp[i], 'prio'):
            priority.append(samples.pop(i))
            print(f'sending sample to the front {temp[i]}')

        if temp[i].type in caboose:
            bad_matrix.append(samples.pop(i))
            print(f'sending sample to the back {temp[i]}')    

def build_screens(samples, interval):
    print('starting builder')
    screen_samples = []
    z = 0
    bad_matrix = []
    priority = []

    temp = samples.copy()

    for i in range(len(temp) -1, -1, -1):
        if hasattr(temp[i], 'prio'):
            priority.append(samples.pop(i))
            print(f'sending sample to the front {temp[i]}')

        if temp[i].type in caboose or hasattr(temp[i], 'bad'):
            bad_matrix.append(samples.pop(i))
            print(f'sending sample to the back {temp[i]}')


    bad_matrix = bad_matrix[::-1]
    bad_matrix = sorted(bad_matrix, key=lambda x: caboose.get(x.type, '99'))
    samples = priority[::-1] + samples + bad_matrix

    screen_samples.append(make_solvent())
    screen_samples.append(make_neg_ctl())
    screen_samples.append(make_pos_ctl())
    screen_samples.append(make_solvent())
    while z < len(samples):
        screen_samples.extend(samples[z:z + interval])
        screen_samples.append(make_solvent())
        screen_samples.append(make_pos_ctl())
        screen_samples.append(make_solvent())
        z += interval

    return screen_samples

def build_vols(samples, interval):
    print('starting builder')
    vol_list = []
    z = 0
    priority = []
    dilns = set()
    temp = samples.copy()

    for i in range(len(temp) -1, -1, -1):

        if hasattr(temp[i], 'diln'):
            if temp[i].diln != 'X0':
                dilns.add(samples[i].diln)
                print(f'creating dilution control {samples[i].diln}')

        if hasattr(temp[i], 'prio'):
            priority.append(samples.pop(i))
            print(f'sending sample to the front {temp[i]}')

    vol_list.append(make_neg_ctl())
    vol_list.extend(make_curve(6))
    vol_list.extend(make_LH())
    if dilns:
        sorted_dilns = sorted(dilns, key=lambda x: int(x[1:]), reverse=True)
        for diln in sorted_dilns:
            vol_list.append(make_diln(diln))
    while z < len(samples):
        vol_list.extend(samples[z:z + interval])
        vol_list.extend(make_LH())
        z += interval
    
    return vol_list

    


#consider making case blocks?
#replace block by finding index of case block
#then SCREENS[(block_index):(block_index)+1] = [list of cases]

def quants(samples, interval):
    blood_quants = []
    serum_quants = []
    if any(case.type):
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
        return