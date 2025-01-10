# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 16:20:55 2024

@author: e314883
"""

import fitz  # PyMuPDF
import os
import re

from objects import QCTYPE, QC, Sample, table_converter



def SHIMADZU_SAMPLEINIT(batch_dir):
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

            try:
                #take care of special cases
                if " 0:Unknown " in lines:
                    Sequence = Sample("Sequence", pdf_path, {QCTYPE.SEQ}, None, None)
                    print("found sequence")
                    samples.append(Sequence)
                    doc.close()
                    continue
                if "Calibration Curve Report" in lines:
                    Curve = Sample("Curve", pdf_path, {QCTYPE.CUR}, None, None)
                    print("found curve")
                    samples.append(Curve)
                    doc.close()
                    continue

                # Find case number using sample name index + 1
                sample_name_index = lines.index("Sample Name")
                case_number = lines[sample_name_index + 1]
                # Trim characters off case number string
                case_number = case_number[2:]
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

                case_number = f"{case_number}_0"
                #change case number if it already exists as an object
                duplicate_count = 1
                while any(case_number == sample.ID for sample in samples):
                    case_number = f"{case_number.rsplit('_', 1)[0]}_{duplicate_count}"
                    duplicate_count += 1
                    #print(f"recognized duplicate, new ID: {case_number}")
                
                #create sample object
                case_number = Sample(case_number, pdf_path, None, format_ISTDs, format_analytes)
                #append to list
                samples.append(case_number)

            except Exception as e:
                print(f"FAILED TO INIT SAMPLE {filename}: {e}")
            doc.close()  

    #return list of sample objects
    print(f"{len(samples)} total samples initialized")        
    return samples

            
def pdf_rename(samples):
    def sanitize_filename(filename):
        return re.sub(r'[\\/*?:"<>|]', "_", filename)

    for sample in samples:
        # Define the new filename
        new_filename = sanitize_filename(f"{sample.ID}.pdf")
        new_path = os.path.join(os.path.dirname(sample.path), new_filename)

        # Rename the file
        try:
            os.rename(sample.path, new_path)
            #print(f"{sample.ID} has been renamed to {new_filename}")

        except PermissionError as e:
            print(f"PermissionError: {e}")
            continue
        except FileExistsError as e:
            print(f"File Exists Error: {e}")
            continue
        except FileNotFoundError as e:
            print(f"File Not Found Error: {e}")
            continue

        # Rename the sample object
        sample.path = new_path

    print("naming complete")

def obj_binder(sample1, sample2, output_dir, batch):
    #open docs and insert
    doc1 = fitz.open(sample1.path)
    doc2 = fitz.open(sample2.path)
    doc1.insert_pdf(doc2)
    #modify name
    base_id = sample1.ID.rsplit('_', 1)[0]

    output_path = os.path.join(output_dir, f"{base_id}_{batch}.pdf")
    #save
    doc1.save(output_path)
    print(f"Successfully bound {sample1.ID} and {sample2.ID} into {output_path}")

def compare_and_bind_samples(samples, output_dir, batch):
    # Create a dictionary to map sample IDs without the suffix to their corresponding samples
    sample_dict = {}
    for sample in samples:
        if sample.type != {QCTYPE.SH}:
            base_id = sample.ID.rsplit('_', 1)[0]
            if base_id not in sample_dict:
                sample_dict[base_id] = {}
            sample_dict[base_id][sample.ID] = sample

    # Iterate through the dictionary to find and bind corresponding samples
    for base_id, sample_versions in sample_dict.items():
        if f"{base_id}_0" in sample_versions and f"{base_id}_1" in sample_versions:
            first_rpt = sample_versions[f"{base_id}_0"]
            second_rpt = sample_versions[f"{base_id}_1"]

            # Perform the binding operation
            obj_binder(first_rpt, second_rpt, output_dir, batch)

if __name__ == "__main__":
    global batch
    batch = 12786
    
    batch_dirs = [
        r"/home/mooshi_1/workspace/github.com/Mooshi-1/Work/locked/private/12786/CASE DATA"
    ]

    all_samples = []

    for batch_dir in batch_dirs:
        print(f"checking {batch_dir}")
        samples = SHIMADZU_SAMPLEINIT(batch_dir)
        all_samples.extend(samples)

    pdf_rename(all_samples)

    for sample in all_samples:
        sample.assign_type()
        #print(sample.path)

    #make sure this is at the end
    #changes self.path of a single repeat and may cause issues for other references
    compare_and_bind_samples(all_samples)

    print("complete")

