

def finalize_SCRNZ(seq):
    final_list = []
    #make 3 item tuple according to columns
    #sample name, vial, datafile
    bases = seq
    acids = seq
    
    filename_count = 0
    vial_count = 0
    solvent_base = 101
    solvent_acid = 102

    # ^ init counters
    # v create bases and then acids

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
    
    for sample in acids:
        col_1 = sample.abbrv + ' A'
        if sample.type == 'SOLVENT':
            col_2 = solvent_base
        else:
            vial_count += 1
            col_2 = vial_count
        filename_count += 1
        col_3 = f"{filename_count:03}_{col_1}_{col_2}.D"
        final_list.append((col_1, col_2, col_3))        

    