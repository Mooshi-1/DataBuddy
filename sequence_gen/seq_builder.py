from seq_init import sequence

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

def screens(samples, interval):
    SCREENS = []
    i = 0

    SCREENS.append(make_solvent())
    SCREENS.append(make_neg_ctl())
    SCREENS.append(make_pos_ctl())
    SCREENS.append(make_solvent())
    while i < len(samples):
        SCREENS.extend(samples[i:i + interval])
        SCREENS.append(make_solvent())
        SCREENS.append(make_pos_ctl())
        SCREENS.append(make_solvent())
        i += interval
    return SCREENS

def quants(samples, interval):
    QUANTS = []
    i = 0

    QUANTS.append(make_solvent())
    QUANTS.append(make_shooter())
    QUANTS.append(make_neg_ctl())
    QUANTS.extend(make_curve(6))
    QUANTS.extend(make_LH())
    QUANTS.append(make_solvent())
    while i 

    if any('SERUM' in sample.type for sample in samples):
