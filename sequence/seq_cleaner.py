import itertools
from sample_dict import caboose
from seq_init import quants


def finalize_SCRNZ(seq):
    print("starting finalizer")
    final_list = []
    #make 3 item tuple according to columns
    #sample name, vial, datafile
    filename_count = 0
    vial_count = 0
    acid_vial_count = 50
    solvent_base = 101
    solvent_acid = 102
    # ^ init counters
    # v create bases and then acids
    bases = seq
    acids = seq

    for sample in bases:
        col_1 = sample.abbrv + ' B'
        if sample.type == 'SOLVENT':
            col_2 = solvent_base
        else:
            vial_count += 1
            col_2 = vial_count
        filename_count += 1
        col_3 = f"{filename_count:03}_{col_1}_{col_2}.D"
        final_list.append((col_1, col_2, col_3))
        if sample.type in caboose or hasattr(sample, 'bad'):
            filename_count += 1
            col_1 = 'BLANK'
            col_2 = solvent_base
            col_3 = f"{filename_count:03}_{col_1}_{col_2}.D"
            final_list.append((col_1, col_2, col_3))

    #skip first solvent since B ends with a solvent
    for sample in acids[1:]:
        col_1 = sample.abbrv + ' A'
        if sample.type == 'SOLVENT':
            col_2 = solvent_acid
        else:
            acid_vial_count += 1
            col_2 = acid_vial_count
        filename_count += 1
        col_3 = f"{filename_count:03}_{col_1}_{col_2}.D"
        final_list.append((col_1, col_2, col_3))       
        if sample.type in caboose or hasattr(sample, 'bad'):
            filename_count += 1
            col_1 = 'BLANK'
            col_2 = solvent_acid
            col_3 = f"{filename_count:03}_{col_1}_{col_2}.D"
            final_list.append((col_1, col_2, col_3)) 

    return final_list
    
def finalize_SCGEN(seq, method):
    print('starting finalizer')
    #excluded RE for now and placing solvents there
    tray_rows = ['GA', 'GB', 'GC', 'GD', 'GE', 'BA', 'BB', 'BC', 'BD', 'BE', 'RA', 'RB', 'RC', 'RD']
    tray_numbers = range(1,9)

    solvent_rows = ['RE']
    solvent_numbers = range(1,9)

    #can eventually implement starting positions / loop
    counter_case = itertools.product(tray_rows, tray_numbers)
    counter_solvent = itertools.cycle(itertools.product(solvent_rows, solvent_numbers))

    def get_position():
        letter, number = next(counter_case)
        return f"{letter}{number}"
    
    def get_solvent():
        letter, number = next(counter_solvent)
        return f"{letter}{number}"
    
    columns=['Sample Name', 'Sample Description', 'Sample Position', 'Method Name', 'Volume']
    final_list = []
    method = 'Toxtyper 3.0_GEN' if method != "SCSYNCANNA" else 'Toxtyper 3.0_SCSYNCAN'
    volume = 5 if method != "Toxtyper 3.0_SCSYNCAN" else 10
    solvent_namer = itertools.cycle(range(1,9))

    if method == "Toxtyper 3.0_SCSYNCAN":
        for sample in seq:
            if final_list and final_list[-1][0].startswith('S') and sample.type == 'SOLVENT':
                continue
            elif sample.type == 'SOLVENT':
                final_list.append((f'S {next(solvent_namer)}', '', get_solvent(), method, volume))  
            elif sample.container != '':
                final_list.append((sample.abbrv, '', get_position(), method, volume))
                #final_list.append((f'S {next(solvent_namer)}', '', get_solvent(), method, volume))
            else:
                final_list.append((sample.abbrv, '', get_position(), method, volume))  
        final_list.append((f'S {next(solvent_namer)}', '', get_solvent(), 'Toxtyper R_Wash_Column', volume))                                       
    else:
        for sample in seq:
            #make sure list isn't empty to avoid index error
            if final_list and final_list[-1][0].startswith('S') and sample.type == 'SOLVENT':
                continue
            elif sample.type == 'SOLVENT':
                final_list.append((f'S {next(solvent_namer)}', '', get_solvent(), method, volume))
            elif sample.container != '':
                final_list.append((sample.abbrv + ' B', '', get_position(), method, volume))
                final_list.append((sample.abbrv + ' A', '', get_position(), method, volume))
                final_list.append((f'S {next(solvent_namer)}', '', get_solvent(), method, volume))
            else:
                final_list.append((sample.abbrv + ' B', '', get_position(), method, volume))
                final_list.append((sample.abbrv + ' A', '', get_position(), method, volume))

        final_list.append((f'S {next(solvent_namer)}', '', get_solvent(), 'Toxtyper R_Wash_Column', volume))
    return final_list

def finalize_LCMSMS(seq, batch):
    final_list = []
    columns=['Batch #', 'Tray', 'Vial#', 'Sample Name']
    #4 item tuple
    solvent_vials = itertools.cycle(range(1,4))
    vial_count = 0

    for sample in seq:
        if sample.type == 'SOLVENT':
            final_list.append((batch, 2, next(solvent_vials), sample.abbrv))
        else:
            vial_count += 1
            final_list.append((batch, 1, vial_count, sample.abbrv))

    return final_list

def finalize_SQVOL(seq, batch):
    final_list = []
    columns=['Batch #', 'Tray Name', 'Vial#', 'Sample Name', 'Sample ID', 'barcode']
    #vial 1-60 tray 1, vial 1-60 tray 2

    tray = 1
    vial = 1

    def increment_vial(tray, vial):
        vial += 1
        if vial > 60:
            vial = 1
            tray += 1
        return tray, vial

    for sample in seq:
        final_list.append((batch, tray, vial, sample.abbrv, sample.abbrv, sample.barcode))
        tray, vial = increment_vial(tray, vial)
        if sample.type in caboose or sample.abbrv.endswith("CUP"):
            final_list.append((batch, tray, vial, 'BLANK', 'BLANK', ''))
            tray, vial = increment_vial(tray, vial)

    return final_list


def finalize_quants(seq, batch):
    final_list = []
    columns=['Batch #', 'Tray', 'Vial#', 'Sample Name']
    tray = 1
    vial_number = 1
    #max vial = 105
    solvents = itertools.cycle(range(100,106))

    previous_sample = None
    for sample in seq:
        if sample.type == 'SOLVENT':
            final_list.append((batch, tray, next(solvents), sample.number))

        elif sample.container == '':
            final_list.append((batch, tray, vial_number, sample.abbrv))
            vial_number += 1

        elif isinstance(sample, quants):
            if previous_sample and previous_sample == sample:
                final_list.append((batch, tray, vial_number, sample.abbrv))
                vial_number += 1
            elif previous_sample and previous_sample != sample:
                #print(f'adding solvent before {sample}')
                final_list.append((batch, tray, next(solvents), 'S'))
                final_list.append((batch, tray, vial_number, sample.abbrv))
                vial_number += 1 
        previous_sample = sample
    final_list.append((batch, tray, next(solvents), 'S'))

    return final_list