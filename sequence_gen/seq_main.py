
import seq_init
import seq_builder
import seq_cleaner
import excel_fill



def main():
    seq_dir = r'C:\Users\e314883\Desktop\python pdf\sequence_gen'
    #create sequence objects, stored in list samples
    samples, method, batches = seq_init.read_sequence(seq_dir)
    batch_num = "/".join(map(str, batches))

    print(f"{len(samples)} samples found, method = {method}, batch number = {batch_num}")

    def build_and_export(samples, method, batch_num):
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
            return       
        
        elif method == 'SQVOL':
            slice_interval = 20
            
            samples_for_seq = seq_builder.build_vols(samples, slice_interval)
            samples_for_write = seq_cleaner.finalize_SQVOL(samples_for_seq, batch_num)
            excel_fill.export_SQVOL(samples_for_write)
            return

        elif method.startswith("QT") or method.startswith("SQ"):
            slice_interval = 20

            samples_for_seq = seq_builder.build_quants(samples, slice_interval, method)
            samples_for_write = seq_cleaner.finalize_quants(samples_for_seq, batch_num)
            excel_fill.export_quants(samples_for_write)
            return
        
        else:
            print('Unable to find a sequence builder for the method listed in the TEST BATCH.')
            method = input('Enter another/similar method and attemp to re-run: ').upper()
            build_and_export(samples, method, batch_num)

    build_and_export(samples, method, batch_num)
    print(f'sequence building is complete!')





if __name__ == '__main__':
   # try:
    print('SEQUENCE GENERATOR START!')

    #inst = input('which instrument are you running on? ')
    #map out instruments
    main()

    #except Exception as e:
       # print(f'sequence generation failed :(  | {e})')
