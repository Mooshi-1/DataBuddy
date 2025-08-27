# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22, 2025

@author: e314883
"""
import fitz  # type: ignore # PyMuPDF
import os
import shutil
#from pypdf import PdfWriter, PdfReader
import io
import re

from aux_func import table_converter
from sample_sorter import QCTYPE, Sample

class CasePacket():
    def __init__(self, case_number, top_sheet_path, date, ISTDs, analytes):
        self.case_number = case_number
        self.top_sheet_path = top_sheet_path
        self.supporting_sheets = [top_sheet_path]
        self.date = date
        self.ISTDs = ISTDs
        self.analytes = analytes

    def __eq__(self, other):
        return (
            self.case_number == other.case_number and
            self.supporting_sheets == other.supporting_sheets and
            self.date == other.date
        )
    
def df_format(list_of_tuples):
    ISTDs_data = []
    analytes_data = []

    header = ("Name", "RT", "Area", "Amount", "Units", "Result Type")

    ISTDs_data.append(header)
    analytes_data.append(header)

    for tuples in list_of_tuples[1:]:
        if re.search(r"-D\d+", tuples[0]) or re.search(r",D\d+", tuples[0]):
            ISTDs_data.append(tuples)
        else:
            analytes_data.append(tuples)
    
    print(ISTDs_data, analytes_data)
    return ISTDs_data, analytes_data

def raw_pdf_handler(cases_to_bind, batch_dir, samples):
    #first run of program
    destination_folder = os.path.join(batch_dir, "SINGLE_PAGES")
    os.makedirs(destination_folder, exist_ok=True)

    for case in cases_to_bind:
        case_ID = None

        case_ID = f"{case.case_number}_0"
        #change case number if it already exists as an object
        duplicate_count = 1
        while any(case_ID == sample.ID for sample in samples):
            case_ID = f"{case_ID.rsplit('_', 1)[0]}_{duplicate_count}"
            duplicate_count += 1
            print(f"recognized duplicate, new ID: {case_ID}")

        filename = f'{case_ID}.pdf'
        output = os.path.join(batch_dir, filename)

        merger = fitz.open()
        for path in case.supporting_sheets:
            try:
                current_pdf = fitz.open(path)
                merger.insert_pdf(current_pdf)
                current_pdf.close()
            except Exception as e:
                print(f'error binding {path} | error: {e}')

        merger.save(output)
        merger.close()
        
        #create sample object
        case_ID = Sample(case_ID, os.path.join(batch_dir, filename), case.case_number, None, case.ISTDs, case.analytes)
        samples.append(case_ID)

    for case in cases_to_bind:
        if len(case.supporting_sheets) == 1:
            continue
        else:
            for path in case.supporting_sheets:
                if path.endswith("_0.pdf") or path.endswith("_1.pdf"):
                    continue
                else:
                    try:
                        shutil.move(path, destination_folder)
                    except Exception as e:
                        print(f'error moving file {path} | error: {e}')
                        continue
    #return list of sample objects
    print(f"{len(samples)} samples initialized from directory {batch_dir}")        
    return samples


def GC_quant_init(batch_dir):
    samples = []
    cases_to_bind = []
    curves = {}
    curve_count = 0

    for filename in os.listdir(batch_dir):
        pdf_path = None
        date = None

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

            #case sample
            if "Acquisition Date:" in lines:
                date_index = lines.index("Acquisition Date:")
                date = lines[date_index + 1]
                sample_name_index = lines.index("Sample Name:")
                case_number = lines[sample_name_index + 1].upper()


                #this is bottom sheet
                if "Compound Report" in lines:
                    for case in cases_to_bind:
                        if case.date == date:
                            case.supporting_sheets.append(pdf_path)    
                    doc.close()
                #this is top sheet
                else:
                    ISTDs = None
                    analytes = None
                    print(f"{case_number}")

                    data_index_start = lines.index("Compound Name")
                    data_index_end = len(lines) - 5

                    if "Cannabinoid Confirmation" in lines:
                        continue
                    else:
                        raw_data = [tuple(lines[i:i+6]) for i in range(data_index_start, data_index_end, 6)]
                        ISTDs, analytes = df_format(raw_data)

                    cases_to_bind.append(CasePacket(case_number, pdf_path, date, ISTDs, analytes))
                    doc.close()

            # sequence + tune
            elif "Directory for Data Files:" in lines:
                print("found sequence")
                samples.append(Sample("Sequence", pdf_path, "sequence", {QCTYPE.SEQ}, None, None))
                doc.close()

            # cal curves
            elif "Calibration Curve Report" in lines:
                curve_key = f"curve_{curve_count}"
                curves[curve_key] = Sample(curve_key, pdf_path, curve_key, {QCTYPE.CUR}, None, None)
                print("found curve")
                samples.append(curves[curve_key])
                doc.close()

            else:
                print(f'unable to identify file | {pdf_path}')

    return raw_pdf_handler(cases_to_bind, batch_dir, samples)


if __name__ == "__main__":

    batch = 12786
    
    batch_dirs = [
        r"C:\Users\e314883\Desktop\python pdf\quants\test"
    ]

    all_samples = []

    for batch_dir in batch_dirs:
        print(f"checking {batch_dir}")
        samples = GC_quant_init(batch_dir)
        all_samples.extend(samples)

    for sample in all_samples:
        sample.assign_type()

