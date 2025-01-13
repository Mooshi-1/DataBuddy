# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 2024

@author: ADG
"""
import os
import re
import fitz  # type: ignore # PyMuPDF
from shutil import copyfile
from sample_sorter import QCTYPE

##renamer functions
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
        except (PermissionError, FileExistsError, FileNotFoundError) as e:
            print(f"--error--: {e}, while renaming {sample.path} to {new_path}")
            continue
        # keep sample.path up to date
        sample.path = new_path
    print("naming complete")


##binder functions
def obj_binder(sample1, sample2, output_dir, batch):
    #output warning if analytes or ISTDs are not equal
    find_misidentification(sample1, sample2)
    #open docs and insert
    try:
        doc1 = fitz.open(sample1.path)
        doc2 = fitz.open(sample2.path)
        doc1.insert_pdf(doc2)
        output_path = os.path.join(output_dir, f"{sample1.base}_{batch}.pdf")
        #save
        doc1.save(output_path)
        print(f"Successfully saved {sample1.base}_{batch}")
    except (PermissionError, FileExistsError, FileNotFoundError) as e:
        print(f"--error--: {e}, while renaming {sample1.path}")


def compare_and_bind_duplicates(samples, output_dir, batch):
    leftovers = samples.copy()
    # Create a list of matched pairs
    matched_pairs = []
    num_samples = len(samples)
    for i in range(num_samples):
        for j in range(i + 1, num_samples):
            if samples[i] == samples[j]:
                matched_pairs.append((samples[i], samples[j]))
                leftovers.remove(samples[i])
                leftovers.remove(samples[j])
 
    # send matched pair list to obj_binder
    for sample1, sample2 in matched_pairs:
        #print(sample1, sample2)
        obj_binder(sample1, sample2, output_dir, batch)
    
    print (f"{len(leftovers)} samples found without a duplicate.")
    return leftovers

#used to take list of objects and bind them together (batch pack, MSA cases)
#added optional name parameter, used specifically in batch pack
def list_binder(list, output_dir, batch, name=None):
    if len(list) < 2:
        print(f"Cannot bind - 1 sample in list {list}")
        return
    doc1 = fitz.open(list[0].path)
    for sample in list[1:]:
        doc2 = fitz.open(sample.path)
        doc1.insert_pdf(doc2)
        doc2.close()

    filename = name if name else list[0].base
    output_path = os.path.join(output_dir, f"{filename}_{batch}.pdf")
    doc1.save(output_path)
    print(f"completed binding multiple files - {filename}_{batch}")

    doc1.close()


##misc functions

#used to take shimadzu format of columns and transpose as rows
def table_converter(table):
    #prep new columns
    keywords = ["ID#", "Name", "Ret. Time (min)", "Area", "Quant Ion (m/z)", "Conc.", "Unit", "Mode"]
    columns = {key: [] for key in keywords}
    current_keyword = None
    #populate sublists based on keywords
    for line in table:
        if line in keywords:
            current_keyword = line
        if current_keyword:
            columns[current_keyword].append(line)
    #ensure that all lists are same length by appending empty strings
    max_length = max([len(columns[key]) for key in keywords])
    for key in keywords:
        while len(columns[key]) < max_length:
            columns[key].append("")
    #create list of sublists to transpose, then zip
    data = [columns[key] for key in keywords]
    transposed_table = list(zip(*data))

    #debug print statements
    #for row in transposed_table:
        #print(", ".join(row))
    #print(transposed_table)
    return transposed_table

#checks stored values for mismatch between case repeats
def find_misidentification(self, other):
    if len(self.results_analyte) != len(other.results_analyte):
        print(f"--WARNING--: {self.base} does not have the same number of analytes reported as duplicate")
    if len(self.results_ISTD) != len(other.results_ISTD):
        print(f"--WARNING--: {self.base} does not have the same number of ISTDs reported as duplicate")


#create batch pack list - send to binder
def batch_pack_handler(curve,shooter,neg_ctl,cal_curve,controls,sequence,dil_controls):
    #get dil_controls inserted properly
    if len(controls) <=2:
        batch_pack = curve + shooter + neg_ctl + cal_curve + controls + dil_controls + sequence
        return batch_pack
    else:
        controls_split_1 = controls[:2]
        controls_split_2 = controls[2:]
        batch_pack = curve + shooter + neg_ctl + cal_curve + controls_split_1 + dil_controls + controls_split_2 + sequence
        return batch_pack

#currently only functions when L0 sample does not have an L suffix
#if it has L# in name the sample_sorter will asiggn QCTYPE.CAL to obj.type
def MOA_slicer(list):
    sliced_lists = []
    current_slice = []

    for obj in list:
        if QCTYPE.CAL not in obj.type:
            if current_slice:
                sliced_lists.append(current_slice) 
            current_slice = []
            current_slice.append(obj)
        current_slice.append(obj)

    if current_slice:
        sliced_lists.append(current_slice)

    return sliced_lists

#need to test this 
def find_sr(cases, SR_cases):
    sliced_lists = []
    print(f"{len(SR_cases)} SR cases found. attempting to find related cases")
    for SR in SR_cases:
        current_slice = []
        for case in cases:
            if case.base in SR.base:
            #if case in SR:
                print(f'match found, appended {case}')
                current_slice.append(case)
        current_slice.append(SR)
        sliced_lists.append(current_slice)
    return sliced_lists

#need to test this
def move_singles(list, output_dir, batch):
    for single in list:
        file_rename = os.path.join(output_dir, f"{single.ID}_{batch}.pdf")
        try:
            copyfile(single.path, file_rename)
        except Exception as e:
            print(f"error moving/naming single inject {single: {e}}")



#note in use
#this not gonna work - need to adjust SR_cases to include associated cases and throw to list binder
def insert_SR(SR_cases, output_dir, batch):
    for SR in SR_cases:
        filename = SR.base
    #iterate through output_dir
    #find filename in directory
    #send both files to binder obj1 obj2 ... SR = obj 2
    for contents in os.path(output_dir):
        if contents.endswith('.pdf'):
            if contents in filename:
                print(f"sending {SR.base} to binder")
                obj_binder(contents, filename, output_dir, batch)
                return
    f"aux.insert_SR function activated but unable to find file"
    return


#sublist slicer ##doesn't work quite right, but the idea is there
#NOT IN USE
def sublist_slicer(list):
    sliced_lists = []
    current_slice = []

    def identify_cal(base_id):
        return base_id.rsplit('_',1)[-1].startswith('L')

    for obj in list:
        base_id = obj.base
        print(f"checking object {obj.base}")
        if current_slice:
# Check if transition happens from ID ending with _L# to one without it or vice versa 
            if not identify_cal(current_slice[-1].base) and identify_cal(base_id):
                sliced_lists.append(current_slice)
                current_slice = []
                print("created new slice")
        current_slice.append(obj)
        print(f"appended {obj.base}")

    if current_slice:
        sliced_lists.append(current_slice)

    return sliced_lists


if __name__ == '__main__':
    SR_cases = ['24-3301_MKB_SR', '24-3303_MKO_SR']
    cases = ['24-3301_MKB', '24-3303_MKO', '24-3301_MKB', '24-3303_MKO']

    #find_sr(cases, SR_cases)

    samples = ['24-3301_MKB', '24-3303_MKO', '24-3301_MKB', '24-3303_MKO', '24-3302_TEST']
    compare_and_bind_duplicates(samples,None,None)
