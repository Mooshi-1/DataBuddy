# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 16:20:55 2024

@author: e314883
"""
import fitz  # type: ignore # PyMuPDF
import os
import re

from aux_func import table_converter
from sample_sorter import QCTYPE, Sample

def LC_quant_init(batch_dir):
    samples = [] #will hold sample objects created here
    # Iterate through directory defined by filepath
    for filename in os.listdir(batch_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(batch_dir, filename)        
            doc = fitz.open(pdf_path)
            # Extract text from the first page
            page = doc[0]
            text = page.get_text()
            #print(text)
            lines = text.split('\n')
            #print(lines)
            case_number = None
            #quant_method = lines[3]
            # Currently storing "ABUSE PANEL QUANTITATION BY LC-MS/MS"
            #init curves count to handle multiple curves
            curves = {}
            curve_count = 0
            try:
                #take care of special cases
                if " 0:Unknown " in lines:
                    Sequence = Sample("Sequence", pdf_path, "sequence", {QCTYPE.SEQ}, None, None)
                    print("found sequence")
                    samples.append(Sequence)
                    doc.close()
                    continue
                if "Calibration Curve Report" in lines:
                    #uses dictionary key to ensure unique object name
                    curve_key = f"curve_{curve_count}"
                    curves[curve_key] = Sample(curve_key, pdf_path, "curve", {QCTYPE.CUR}, None, None)
                    print("found curve")
                    samples.append(curves[curve_key])
                    curve_count += 1
                    doc.close()
                    continue
                # Find case number using sample name index + 1
                try:
                    sample_name_index = lines.index("Sample Name")
                except ValueError:
                    print(f"invalid sample {filename}")
                    doc.close
                    continue
                case_number = lines[sample_name_index + 1]
                # Trim characters off case number string
                case_number = case_number[2:].upper()
                #print(f"{case_number}")
                # Extract table data
                ISTDs_data = []
                analytes_data = []
                capture_ISTDs = False
                capture_analytes = False
                for line in lines:
                    #differentiate collection windows
                    if "Quantitative Results: ISTDs" in line:
                        capture_ISTDs = True
                        capture_analytes = False
                    elif "Quantitative Results: Analytes" in line:
                        capture_ISTDs = False
                        capture_analytes = True
                    #stop collecting here
                    elif (capture_ISTDs or capture_analytes) and line.strip() == "":
                        capture_ISTDs = False
                        capture_analytes = False
                    #if capture = true, append the data
                    elif capture_ISTDs:
                        ISTDs_data.append(line.strip())
                    elif capture_analytes:
                        analytes_data.append(line.strip())
                #print(f"Extracted table data: {len(ISTDs_data)} and {len(analytes_data)}")
                format_ISTDs = table_converter(ISTDs_data)
                format_analytes = table_converter(analytes_data)

                case_ID = f"{case_number}_0"
                #change case number if it already exists as an object
                duplicate_count = 1
                while any(case_ID == sample.ID for sample in samples):
                    case_ID = f"{case_ID.rsplit('_', 1)[0]}_{duplicate_count}"
                    duplicate_count += 1
                    #print(f"recognized duplicate, new ID: {case_ID}")
                
                #create sample object
                case_ID = Sample(case_ID, pdf_path, case_number, None, format_ISTDs, format_analytes)
                #print(case_ID)
                samples.append(case_ID)
            except Exception as e:
                print(f"--ERROR-- FAILED TO INIT SAMPLE (VERY BAD) {filename}: {e}")
                doc.close()
                continue
            doc.close()  

    #return list of sample objects
    print(f"{len(samples)} samples initialized from directory {batch_dir}")        
    return samples


if __name__ == "__main__":

    batch = 12786
    
    batch_dirs = [
        r"/home/mooshi_1/workspace/github.com/Mooshi-1/Work/locked/private/12786/CASE DATA"
    ]

    all_samples = []

    for batch_dir in batch_dirs:
        print(f"checking {batch_dir}")
        samples = LC_quant_init(batch_dir)
        all_samples.extend(samples)

    for sample in all_samples:
        sample.assign_type()

