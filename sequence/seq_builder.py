from seq_init import sequence
from sample_dict import caboose
import copy

# class sequence():
#     def __init__(self, sample_number, sample_type, sample_container, barcode, abbrv=None):
#         self.number = sample_number
#         self.type = sample_type
#         self.container = sample_container
#         self.barcode = barcode
#         self.abbrv = "" if abbrv is None else abbrv

def make_solvent():
    if not hasattr(make_solvent, "counter"):
        make_solvent.counter = 0
    make_solvent.counter += 1
    return sequence(f'S', 'SOLVENT', '', f'S{make_solvent.counter}', f'S{make_solvent.counter}')

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
    for i in range(1, CALS + 1):
        curve_list.append(sequence(f'CAL{i}', f'CAL{i}', '', f'CAL{i}', f'CAL{i}'))
    return curve_list

#call .extend
def make_LH(init_counter=None):
    if init_counter is not None:
        make_LH.counter = init_counter
    elif not hasattr(make_LH, "counter"):
        make_LH.counter = 0
    make_LH.counter += 1
    return [
        sequence(f'LOW CTL {make_LH.counter}', 'LOW CTL', '', f'LOW CTL {make_LH.counter}', f'LOW CTL {make_LH.counter}'),
        sequence(f'HIGH CTL {make_LH.counter}', 'HIGH CTL', '', f'HIGH CTL {make_LH.counter}', f'HIGH CTL {make_LH.counter}')
    ]

def make_diln(value):
    return sequence(f'DILN CTL {value}', 'CTL', '', f'DILN CTL {value}', f'DILN CTL {value}')

def make_SR(sample):
    return sequence('SPIKED RECOVERY', 'SR', '', sample.barcode, sample.abbrv + '_SR')

def build_screens(samples, interval):
    make_neg_ctl.counter = 0
    make_pos_ctl.counter = 0
    make_solvent.counter = 0

    print('starting builder')
    screen_samples = []
    z = 0
    bad_matrix = []
    priority = []
    PTs = []

    #make sure to add PT list back into samples

    temp = samples.copy()

    for i in range(len(temp) -1, -1, -1):
        if hasattr(temp[i], 'PTs'):
            PTs.append(samples.pop(i))
            print(f'found proficiency {temp[i]}')

        elif hasattr(temp[i], 'prio'):
            priority.append(samples.pop(i))
            print(f'sending sample to the front {temp[i]}')

        elif temp[i].type in caboose or hasattr(temp[i], 'bad'):
            bad_matrix.append(samples.pop(i))
            print(f'sending sample to the back {temp[i]}')
    
    if PTs:
        PTs = PTs[::-1]
        flag = input('Do you want your PTs in duplicate? [Y/n]').upper()
        if flag.startswith('Y'):
            PTs_rpt = copy.deepcopy(PTs)
            for case in PTs_rpt:
                case.abbrv = case.abbrv.split("_")[0] + "_RPT"
            PTs += PTs_rpt
    bad_matrix = bad_matrix[::-1]
    bad_matrix = sorted(bad_matrix, key=lambda x: caboose.get(x.type, 99))
    samples = PTs + priority[::-1] + samples + bad_matrix


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

    #print(screen_samples)
    return screen_samples

def build_vols(samples, interval):
    make_solvent.counter = 0
    make_neg_ctl.counter = 0
    make_LH.counter = 0

    print('starting builder')
    vol_list = []
    z = 0
    priority = []
    dilns = set()
    temp = samples.copy()

    for i in range(len(temp) -1, -1, -1):

        if hasattr(temp[i], 'diln'):
            if temp[i].diln != 'X0' and temp[i].diln != 'X1':
                dilns.add(samples[i].diln)
                print(f'creating dilution control {samples[i].diln}')

        if hasattr(temp[i], 'prio'):
            priority.append(samples.pop(i))
            print(f'sending sample to the front {temp[i]}')

        # organize single > double order and then append doubles to sample list
        # make sure to not disrupt index of samples
    samples = priority[::-1] + samples
    samples_final = []

    ## if continued issues here, order the list all in single and then loop through samples again and apply duplicates ##
    for sample in samples:
        if sample.single:
            if len(samples_final) >= 2:
                if sample == samples_final[-1] and sample == samples_final[-2]:
                    print(f'rearranged single injection {sample.abbrv}')
                    samples_final.insert(-2, sample)
                    continue
                elif sample == samples_final[-1] and "BLOOD" in sample.type:
                    samples_final.insert(-1, sample)
                    continue
            samples_final.append(sample)
        if sample.double:
            if len(samples_final) >= 2:
                if samples_final[-1] == sample and samples_final[-2] == sample:
                    if "BLOOD" in sample.type:
                        samples_final.insert(-2, sample)
                        samples_final.insert(-2, sample.copy())
                        continue
                    if "OCULAR" in sample.type and "BLOOD" not in samples_final[-1].type:
                        samples_final.insert(-2, sample)
                        samples_final.insert(-2, sample.copy())
                        continue
                    if "BRAIN" in sample.type and "LIVER" in samples_final[-1].type:
                        samples_final.insert(-2, sample)
                        samples_final.insert(-2, sample.copy())
                        continue      
            samples_final.append(sample)
            samples_final.append(sample.copy())

    vol_list.append(make_neg_ctl())
    vol_list.extend(make_curve(6))
    vol_list.extend(make_LH())
    if dilns:
        sorted_dilns = sorted(dilns, key=lambda x: int(x[1:]), reverse=True)
        for diln in sorted_dilns:
            vol_list.append(make_diln(diln))
    while z < len(samples_final):
        vol_list.extend(samples_final[z:z + interval])
        vol_list.extend(make_LH())
        z += interval
    
    #print(vol_list)
    return vol_list


def build_quants(samples, interval, method):
    make_neg_ctl.counter = 0
    make_LH.counter = 0
    make_solvent.counter = 0
    make_shooter.counter = 0

    print('starting builder')
    quant_list = []
    z = 0
    y = 0
    priority = []
    dilns_b = set()
    serums = []
    dilns_s = set()
    temp = samples.copy()
    MSA = []

    def check_diln(sample, flag=None):
        if hasattr(sample, 'diln') and sample.diln != 'X0' and sample.diln != 'X1':
            if flag:
                dilns_s.add(sample.diln)
                print(f'creating serum dilution control {sample.diln}')
            else:
                dilns_b.add(sample.diln)
                print(f'creating blood control {sample.diln}')
                
#main loop to check for exceptions, handle MSA/serums then bloods
    for i in range(len(temp) -1, -1, -1):
        if hasattr(temp[i], 'MSA'):
            MSA.append(samples.pop(i))
            print(f'found MSA {temp[i]}')
            continue

        elif hasattr(temp[i], 'serum'):
            print(f'found serum sample')
            check_diln(samples[i], 'S')
            serums.append(samples.pop(i))
            continue
        
        else:
            check_diln(temp[i])
            if hasattr(temp[i], 'prio'):
                priority.append(samples.pop(i))
                print(f'sending sample to the front {temp[i]}')
                


    samples = priority[::-1] + samples
    bloods_final = []
    serums_final = []
    for sample in samples:
        if sample.single:
            bloods_final.append(sample)
        if sample.double:
            bloods_final.append(sample)
            bloods_final.append(sample.copy())
        if hasattr(sample, 'SR'):
            bloods_final.append(make_SR(sample))
    
    if serums:
        for serum in serums[::-1]:
            if serum.single:
                serums_final.append(serum)
            if serum.double:
                serums_final.append(serum)
                serums_final.append(serum.copy())
            if hasattr(serum, 'SR'):
                serums_final.append(make_SR().add_serum())

    quant_list.append(make_solvent())
    quant_list.append(make_shooter())
    quant_list.append(make_neg_ctl())
    quant_list.extend(make_curve(6))
    quant_list.append(make_solvent())
    quant_list.extend(make_LH())
    if dilns_b:
        sorted_dilns = sorted(dilns_b, key=lambda x: int(x[1:]), reverse=True)
        for diln in sorted_dilns:
            quant_list.append(make_diln(diln))
    while z < len(bloods_final):
        quant_list.extend(bloods_final[z:z + interval])
        quant_list.append(make_solvent())
        quant_list.extend(make_LH())

        z += interval
    if serums_final:
        quant_list.append(make_solvent())
        quant_list.append(make_shooter().add_serum())
        quant_list.append(make_neg_ctl().add_serum())
        if method.startswith('QTACET'):
            quant_list.extend([cal.add_serum() for cal in make_curve(6)])
        quant_list.extend([ctl.add_serum() for ctl in make_LH(0)])
        if dilns_s:
            sorted_dilns = sorted(dilns_s, key=lambda x: int(x[1:]), reverse=True)
            for diln in sorted_dilns:
                quant_list.append(make_diln(diln).add_serum())

        while y < len(serums_final):
            quant_list.extend(serums_final[y:y+interval])
            quant_list.append(make_solvent())
            quant_list.extend([ctl.add_serum() for ctl in make_LH()])
            y += interval
    if MSA:
        for case in MSA[::-1]:
            quant_list.append(case)
            quant_list.append(sequence(case.number, 'MSA', '', case.barcode, case.abbrv + '_L1'))
            quant_list.append(sequence(case.number, 'MSA', '', case.barcode, case.abbrv + '_L2'))
            quant_list.append(sequence(case.number, 'MSA', '', case.barcode, case.abbrv + '_L3'))
            quant_list.append(sequence(case.number, 'MSA', '', case.barcode, case.abbrv + '_L4'))
            quant_list.append(sequence(case.number, 'MSA', '', case.barcode, case.abbrv + '_L5'))

    return quant_list