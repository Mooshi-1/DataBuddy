
import seq_init
import seq_builder
import seq_cleaner
import excel_fill


# [('2025-00048', 'BLOOD - HEART', '2301182', '50ML RED TOP', 'SCGEN', '12821', '25-00048_HBBRT'),
# ('2025-00053', 'BRAIN', '2301269', 'FRESH SPECIMEN CUP', 'SCGEN', '12821', '25-00053_BRNCUP'),
# ('2025-00099', 'BLOOD - HEART', '2302145', '50ML RED TOP', 'SCGEN', '12821', '25-00099_HBBRT'),
# ('2025-00115', 'BLOOD - AORTA', '2302625', '50ML RED TOP', 'SCGEN', '12821', '25-00115_AOBBRT'),
# ('2025-00118', 'BLOOD - ANTEMORTEM', '2303301', 'PURPLE TOP TUBE', 'SCGEN', '12821', '25-00118_AMBPRPT'),
# ('2025-00119', 'BLOOD - AORTA', '2302775', '50ML RED TOP', 'SCGEN', '12821', '25-00119_AOBBRT'),
# ('2025-00120', 'BLOOD - AORTA', '2302815', '50ML RED TOP', 'SCGEN', '12821', '25-00120_AOBBRT')]

def main():
    seq_dir = r'C:\Users\e314883\Desktop\python pdf\sequence_gen'

    #create sequence objects, stored in list samples
    samples, method, batches = seq_init.read_sequence(seq_dir)
    batch_num = "/".join(map(str, batches))



    print(f"{len(samples)} samples found, method = {method}, batch number = {batch_num}")

    # test comments --
    # P = priority
    # X# = dilution
    # still need to handle MSA's
    # make sure quants can do an MSA + dilution

    # list(dilution)

    #store batches in new "PDF DATA/BATCHES" folder
    #at very end of main, move seq pdf to analyst name within BATCHES folder
    #then rename


    if method.startswith("SC"):
        slice_interval = 20
        samples_for_seq = seq_builder.build_screens(samples, slice_interval)
        
        if method == 'SCGEN':
            samples_for_write = seq_cleaner.finalize_SCGEN(samples_for_seq)
            excel_fill.export_SCGEN(samples_for_write)        

        if method == 'SCRNZ':
            samples_for_write = seq_cleaner.finalize_SCRNZ(samples_for_seq)
            excel_fill.export_SCRNZ(samples_for_write)

        if method == 'SCLCMSMS':
            samples_for_write = seq_cleaner.finalize_LCMSMS(samples_for_seq, batch_num)
            excel_fill.export_LCMSMS(samples_for_write)              
    
    if method == 'SQVOL':
        slice_interval = 20
        samples_for_seq = seq_builder.build_vols(samples, slice_interval)
        samples_for_write = seq_cleaner.finalize_SQVOL(samples_for_seq, batch_num)
        excel_fill.export_SQVOL(samples_for_write)

    if method.startswith("QT"):
        slice_interval = 20
        





if __name__ == '__main__':
   # try:
    print('BINDER START!')

    inst = input('which instrument are you running on? ')
    #map out instruments
    main()

    #except Exception as e:
       # print(f'sequence generation failed :(  | {e})')
