# -*- coding: utf-8 -*-
"""
Created on Monday 01/27/25

@author: Giachetti
"""
import seq_init
import seq_builder
import seq_cleaner
import excel_fill
from sample_dict import method_dict
import searcher
import sys

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
                                                                             
 Version 1.02 - 3/4/25
'''

def main(initials):
    seq_dir = fr'G:\PDF DATA\TEST BATCH REPORTS\{initials}'
    #create sequence objects, stored in list samples
    try:
        samples, method, batches = seq_init.read_sequence(seq_dir)
    except Exception as e:
        print(f'INIT FAILED -- Umm... is your file in the right place? -- {e}')
        input('Press enter to exit...')
        return
        
    batch_num = "-".join(sorted(batches))

    print(f"{len(samples)} samples found, method = {method}, batch number = {batch_num}")

    def build_and_export(samples, method, batch_num, seq_dir):
        if method.startswith("SC") or method.startswith('CO'):
            slice_interval = 20
            samples_for_seq = seq_builder.build_screens(samples, slice_interval)
            
            if method == 'SCGEN' or method == 'COSTIM':
                samples_for_write = seq_cleaner.finalize_SCGEN(samples_for_seq)
                excel_fill.export_SCGEN(samples_for_write, seq_dir, batch_num)        

            if method == 'SCRNZ':
                samples_for_write = seq_cleaner.finalize_SCRNZ(samples_for_seq)
                excel_fill.export_SCRNZ(samples_for_write, seq_dir, batch_num)

            if method == 'SCLCMSMS' or method == 'COTHC' or method == 'SCNITAZENE':
                samples_for_write = seq_cleaner.finalize_LCMSMS(samples_for_seq, batch_num)
                excel_fill.export_LCMSMS(samples_for_write, seq_dir, batch_num)        
            return       
        
        elif method == 'SQVOL':
            slice_interval = 20

            samples_for_seq = seq_builder.build_vols(samples, slice_interval)
            samples_for_write = seq_cleaner.finalize_SQVOL(samples_for_seq, batch_num)
            excel_fill.export_SQVOL(samples_for_write, seq_dir, batch_num)
            return

        elif method.startswith("QT") or method.startswith("SQ"):
            slice_interval = 20

            samples_for_seq = seq_builder.build_quants(samples, slice_interval, method)
            samples_for_write = seq_cleaner.finalize_quants(samples_for_seq, batch_num)
            excel_fill.export_quants(samples_for_write, seq_dir, batch_num)
            return
        
        else:
            print('Unable to find a sequence builder for the method listed in the TEST BATCH.')
            method = input('Enter another/similar method and attemp to re-run?: ').upper()
            build_and_export(samples, method, batch_num, seq_dir)

    try:
        build_and_export(samples, method, batch_num, seq_dir)
        print('-----------------------------------------------------------------------------------------')
        print(f'sequence building is complete! An excel file has been created where your TEST BATCH is.')
        print('-----------------------------------------------------------------------------------------')
    except Exception as e:
        print(f'Sequence build and export failed :[   | {e}')

    def find_instrument(method):
        matched_methods = [methods for methods in method_dict if methods.startswith(method)]
        if not matched_methods:
            print(f'Unable to find instrument associated with {method}')
            method = input('Enter another method name that uses the same instrument?: ').upper()
            return find_instrument(method)
        elif len(method_dict[matched_methods[0]]) == 1:
            return method_dict[matched_methods[0]][0]
        else:
            choice = input(f'type 1 for {method_dict[matched_methods[0]][0]} OR 2 for {method_dict[matched_methods[0]][1]}: ')
            choice = int(choice) - 1
            return method_dict[matched_methods[0]][choice]

    try:
        var = input('Would you like an LF-23 INSTRUMENT CHECKLIST folder created for you? [Y/n]:').upper()
        if var.startswith('Y'):
            print('comparing method to instruments available...')
            instrument = find_instrument(method)
            print(f'Make sure your files are closed. Attempting to move to {instrument} folder')
            input('press enter to continue')
            searcher.LF_plumbing(seq_dir, instrument, initials)
            print('-----------------------------------------------------------------------------------------')
            print('                Successful! Your files have been copied :) Bye!')
            input('-----------------------------------------------------------------------------------------')

        if var.startswith('N'):
            input('Press enter to exit...')
            return
    except Exception as e:
        print(f'theres been a problem... unable to create LF-23 directory | {e}')
        input('Exiting...')
        return

if __name__ == '__main__':

    print(ascii_art)
    print(f"sys.argv: {sys.argv}")

    if len(sys.argv) < 2:
        print(r'place your sequence in G:\PDF DATA\TEST BATCH REPORTS under your initials')
        initials = input('Enter your initials: ').upper()

    else:
        # Use CLI provided arguments
        initials = sys.argv[1]

    main(initials)
