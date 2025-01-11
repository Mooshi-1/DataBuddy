# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 2024

@author: ADG
"""
import os
import re
import fitz

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
            print(f"--error--: {e}")
            continue
        # keep sample.path up to date
        sample.path = new_path
    print("naming complete")


##binder functions
def obj_binder(sample1, sample2, output_dir, batch):
    #output warning if analytes or ISTDs are not equal
    find_misidentification(sample1, sample2)
    #open docs and insert
    doc1 = fitz.open(sample1.path)
    doc2 = fitz.open(sample2.path)
    doc1.insert_pdf(doc2)
    output_path = os.path.join(output_dir, f"{sample1.base}_{batch}.pdf")
    #save
    doc1.save(output_path)
    print(f"Successfully bound {sample1.ID} and {sample2.ID} into {output_path}")
    #update path
    sample1.path = output_path
    #print(sample1.path)
    #maybe I need to init a new object here...? will see if this causes issues

def compare_and_bind_duplicates(samples, output_dir, batch):
    # Create a list of matched pairs
    matched_pairs = []
    num_samples = len(samples)
    for i in range(num_samples):
        for j in range(i + 1, num_samples):
            if samples[i] == samples[j]:
                #print(samples[i], samples[j])
                matched_pairs.append((samples[i], samples[j]))
    # send matched pair list to obj_binder
    for sample1, sample2 in matched_pairs:
        obj_binder(sample1, sample2, output_dir, batch)
    #MAYBE CAN POP SAMPLE OUT OF CASES LIST HERE??? FIND OUT HOW TO GET SINGLES

#used to take list of objects and bind them together (batch pack)
def list_binder(list, output_dir, batch):
    if len(list) < 2:
        print(f"Cannot bindd - 1 sample in list {list}")
    doc1 = fitz.open(list[0].path)
    for sample in list[1:]:
        doc2 = fitz.open(sample.path)
        doc1.insert_pdf(doc2)
        doc2.close()

    output_path = os.path.join(output_dir, f"{list[0].base}_{batch}.pdf")
    doc1.save(output_path)
    print("completed binding list")

    #updated path, again, maybe this causes problems
    list[0].path = output_path
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


#create batch pack
def batch_pack_handler(curve,shooter,neg_ctl,cal_curve,controls,sequence,dil_controls):
    #get dil_controls inserted properly

    batch_pack = curve + shooter + neg_ctl + cal_curve + controls + sequence
    return batch_pack
