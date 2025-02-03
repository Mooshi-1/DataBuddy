import itertools
from sample_dict import caboose

# I think... make dict to move samples around


#check sample.type


def sort_shitty_matrices():
    #make function to sort / order bad matrices
    pass

def finalize_SCRNZ(seq):
    print("starting finalizer")
    final_list = []

    #make 3 item tuple according to columns
    #sample name, vial, datafile

    filename_count = 0
    vial_count = 0
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
        if sample.type in caboose:
            filename_count += 1
            col_1 = 'BLANK'
            col_2 = solvent_base
            col_3 = f"{filename_count:03}_{col_1}_{col_2}.D"
            final_list.append((col_1, col_2, col_3))

    for sample in acids:
        col_1 = sample.abbrv + ' A'
        if sample.type == 'SOLVENT':
            col_2 = solvent_acid
        else:
            vial_count += 1
            col_2 = vial_count
        filename_count += 1
        col_3 = f"{filename_count:03}_{col_1}_{col_2}.D"
        final_list.append((col_1, col_2, col_3))       
        if sample.type in caboose:
            filename_count += 1
            col_1 = 'BLANK'
            col_2 = solvent_acid
            col_3 = f"{filename_count:03}_{col_1}_{col_2}.D"
            final_list.append((col_1, col_2, col_3)) 

    return final_list
    
def finalize_SCGEN(seq):


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
    method = 'Toxtyper 3.0_GEN'
    volume = 5
    solvent_namer = itertools.cycle(range(1,9))

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

def finalize_LCMSMS(seq):
    final_list = []
    