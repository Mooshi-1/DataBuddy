# -*- coding: utf-8 -*-
"""
Created on Monday 01/27/25

@author: Giachetti
"""
import seq_init
import seq_builder
import seq_cleaner
import excel_fill

ascii_art = '''

███████╗███████╗ ██████╗ ██╗   ██╗███████╗███╗   ██╗ ██████╗███████╗         
██╔════╝██╔════╝██╔═══██╗██║   ██║██╔════╝████╗  ██║██╔════╝██╔════╝         
███████╗█████╗  ██║   ██║██║   ██║█████╗  ██╔██╗ ██║██║     █████╗           
╚════██║██╔══╝  ██║▄▄ ██║██║   ██║██╔══╝  ██║╚██╗██║██║     ██╔══╝           
███████║███████╗╚██████╔╝╚██████╔╝███████╗██║ ╚████║╚██████╗███████╗         
╚══════╝╚══════╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚══════╝         
                                                                             
 ██████╗ ███████╗███╗   ██╗███████╗██████╗  █████╗ ████████╗ ██████╗ ██████╗ 
██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝███████║   ██║   ██║   ██║██████╔╝
██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗
╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║
 ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
                                                                             
 Version 1.00 - 2/7/25
'''

def main(initials):
    seq_dir = fr'G:\PDF DATA\TEST BATCH REPORTS\{initials}'
    #create sequence objects, stored in list samples
    try:
        samples, method, batches = seq_init.read_sequence(seq_dir)
    except Exception as e:
        print(f'INIT FAILED -- THIS IS NOT GOOD -- {e}')
        
    batch_num = "/".join(map(str, batches))

    print(f"{len(samples)} samples found, method = {method}, batch number = {batch_num}")

    def build_and_export(samples, method, batch_num, seq_dir):
        if method.startswith("SC"):
            slice_interval = 20
            samples_for_seq = seq_builder.build_screens(samples, slice_interval)
            
            if method == 'SCGEN':
                samples_for_write = seq_cleaner.finalize_SCGEN(samples_for_seq)
                excel_fill.export_SCGEN(samples_for_write, seq_dir)        

            if method == 'SCRNZ':
                samples_for_write = seq_cleaner.finalize_SCRNZ(samples_for_seq)
                excel_fill.export_SCRNZ(samples_for_write, seq_dir)

            if method == 'SCLCMSMS':
                samples_for_write = seq_cleaner.finalize_LCMSMS(samples_for_seq, batch_num)
                excel_fill.export_LCMSMS(samples_for_write, seq_dir)        
            return       
        
        elif method == 'SQVOL':
            slice_interval = 20

            samples_for_seq = seq_builder.build_vols(samples, slice_interval)
            samples_for_write = seq_cleaner.finalize_SQVOL(samples_for_seq, batch_num)
            excel_fill.export_SQVOL(samples_for_write, seq_dir)
            return

        elif method.startswith("QT") or method.startswith("SQ"):
            slice_interval = 20

            samples_for_seq = seq_builder.build_quants(samples, slice_interval, method)
            samples_for_write = seq_cleaner.finalize_quants(samples_for_seq, batch_num)
            excel_fill.export_quants(samples_for_write, seq_dir)
            return
        
        else:
            print('Unable to find a sequence builder for the method listed in the TEST BATCH.')
            method = input('Enter another/similar method and attemp to re-run: ').upper()
            build_and_export(samples, method, batch_num, seq_dir)

    try:
        build_and_export(samples, method, batch_num, seq_dir)
        print('-----------------------------------------------------------------------------------------')
        print(f'sequence building is complete! An excel file has been created where your TEST BATCH is.')
        print('-----------------------------------------------------------------------------------------')
    except Exception as e:
        print(f'Sequence build and export failed :[   | {e}]')


if __name__ == '__main__':
   # try:
    print(ascii_art)
    print(r'place your sequence in G:\PDF DATA\TEST BATCH REPORTS under your initials')
    initials = input('Enter your initials: ').upper()

    #inst = input('which instrument are you running on? ')
    #map out instruments
    main(initials)

    #except Exception as e:
       # print(f'sequence generation failed :(  | {e})')
