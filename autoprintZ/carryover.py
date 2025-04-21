import os
from PyPDF2 import PdfReader
import pandas as pd
import openpyxl
import openpyxl.cell._writer #pyinstaller needs this specific line or will be missing dependancy
import sys

def extract_info_from_page(page):
    text = page.extract_text()
    drug_name = None
    score = None
    abundance = None
    RT = None
    case_number = None


    lines = text.split('\n')
    try:
        case_number = lines[0].rsplit('\\', 1)[1].strip()
        for line in lines:
            if "SCRNZ-MH" in line:
                parts = line.strip().split(':')
                drug_name = parts[1].strip()
                if "?" in drug_name:
                    drug_name = drug_name.replace("?","").strip()
                score = parts[0].split('=')[1]
                score = float(score[:2])
                if score == 10:
                    score = 100
            if "Abundance" in line:
                parts = line.split('[')
                abundance = float(parts[1].split(']')[0].strip())
            if "Extracted spectrum" in line:
                parts = line.split('(')
                RT = parts[1].split(')')[0].strip()
    except Exception as e:
        print(f'.pdf file is not an AMDIS report || {e}')
        return 'ERROR', 'ERROR', 'ERROR', 'ERROR'
    if drug_name != None and score != None and abundance != None and RT != None:
        return drug_name, score, abundance, RT
    else:
        return case_number, 'score', 'abundance', 'retention'

def extract_text_from_pdf(pdf_path):
    info_list = []
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            drug_name, score, abundance, RT = extract_info_from_page(page)
            info_list.append((
                page_num + 1, drug_name,score,abundance, RT
            ))
    return info_list

def reinject_to_excel(reinjects, path):
    rows = []
    sequence = []
    sequence_rows = []

    for key, values in reinjects.items():
        if values:
            for i, value in enumerate(values):
                if i == 0:
                    sequence.append(key)
                    rows.append([key, *value])
                else:
                    rows.append(["", *value])
    if sequence:
        counter = 900
        for item in sequence[::-1]:
            if ' A_' in item or ' B_' in item:
                sequence_rows.append(("S", 101, f'{counter}_S_101.D'))
                counter += 1

                delimiter = ' A_' if ' A_' in item else ' B_'
                parts = item.rsplit(delimiter)
                number = parts[0][4:] + "_RI" + delimiter.strip('_')
                vial = parts[1]
                filename = parts[0] + "_RI" + delimiter + vial + ".D"
                sequence_rows.append((number, int(vial), filename))
        sequence_rows.append(("S", 101, f'{counter}_S_101.D'))
        counter += 1

    RI_list = pd.DataFrame(rows, columns=['Case Number', 'Page', 'Drug Name', 'Score', 'Abundance', 'Retention'])
    RI_sequence = pd.DataFrame(sequence_rows, columns=['Case Number', 'Vial', 'Filename'])

    excel_path = os.path.join(path, f'AMDIS_REPORT.xlsx')
 
    if os.path.exists(excel_path):
        with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            RI_list.to_excel(writer, sheet_name='reinjects', index=False)
            RI_sequence.to_excel(writer, sheet_name='sequence', index=False)
    else:
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            RI_list.to_excel(writer, sheet_name='reinjects', index=False)
            RI_sequence.to_excel(writer, sheet_name='sequence', index=False)

def full_info_to_excel(all_reports, path):
    print('starting export')
    df = pd.DataFrame(all_reports, columns=['Page', 'Drug Name', 'Score', 'Abundance', 'Retention'])

    excel_path = os.path.join(path, f'AMDIS_REPORT.xlsx')
 
    if os.path.exists(excel_path):
        with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name='full_report', index=False)

    else:
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='full_report', index=False)

    print(f'data written to {excel_path}')

def main(path):
    previous_report = {}
    reinjects = {}
    all_reports = []

    for filename in os.listdir(path):
    
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(path, filename)
            print(f"Processing file: {filename}")
            #get data
            info_list = extract_text_from_pdf(pdf_path)
            #send to excel
#                 (1, '005_24-3725_IVBGT B_3 ', 'score', 'abundance', 'retention')
# INFO STRUCTURE: (4, 'Pseudoephedrine formyl artifact', '62', '229', '2.142 min')
            case_key = info_list[0][1]
            reinjects[case_key] = []

            for info in info_list:
                all_reports.append(info)
                if info[1] in previous_report:
                    if info[3] <= previous_report[info[1]]:
                        reinjects[case_key].append(info)
        else:
            continue
        all_reports.append(("","","",""))
        previous_report = {info[1]: info[3] for info in info_list if (info[1] != 'Mepivacaine ISTD' and info [1] != 'Aprobarbital ISTD')}
        #add calculation to info[3] to adjust for tolerance, if needed
    # #print verify
    #     print(previous_report)
    # for key, value in reinjects.items():
    #     print(f"{key}: {value}")
    reinject_to_excel(reinjects, path)
    full_info_to_excel(all_reports, path)    
    #print(reinjects)


if __name__ == "__main__":

    print(f"sys.argv: {sys.argv}")

    if len(sys.argv) < 2:

        path = input("enter the directory where the data is located")

    else:
        # Use CLI provided arguments
        path = sys.argv[1]
    
    path = os.path.normpath(path)


    main(path)
    print("SCRIPT END")


