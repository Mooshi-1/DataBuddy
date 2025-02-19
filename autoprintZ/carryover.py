import os
from PyPDF2 import PdfReader

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


def create_full_excel(info_list):
        #columns = ['Page Number', 'Drug Name', 'Score', 'Abundance', 'Retention']
    pass

def main():
    path = r'C:\Users\e314883\Desktop\locked_git_repo\AMDIS'
    previous_report = {}
    reinjects = {}

    for filename in os.listdir(path):
    
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(path, filename)
            print(f"Processing file: {filename}")
            #get data
            info_list = extract_text_from_pdf(pdf_path)
            #send to excel
            create_full_excel(info_list)

#                 (1, '005_24-3725_IVBGT B_3 ', 'score', 'abundance', 'retention')
# INFO STRUCTURE: (4, 'Pseudoephedrine formyl artifact', '62', '229', '2.142 min')
            case_key = info_list[0][1]
            reinjects[case_key] = []

            for info in info_list:
                if info[1] in previous_report:
                    if info[3] <= previous_report[info[1]]:
                        reinjects[case_key].append(info)
        else:
            continue

        previous_report = {info[1]: info[3] for info in info_list if (info[1] != 'Mepivacaine ISTD' and info [1] != 'Aprobarbital ISTD')}

        print(previous_report)
    for key, value in reinjects.items():
        print(f"{key}: {value}")
    #print(reinjects)


if __name__ == "__main__":
    main()

# Processing file: 26877 Results of AMDIS Analysis.pdf

# (2, 'Chlorphenisin', '73', '308', '1.073 min')
# (3, 'Norketamine', '69', '2110', '1.862 min')
# (4, 'Pseudoephedrine formyl artifact', '62', '229', '2.142 min')
# (5, 'Bupropion', '85', '84187', '2.315 min')
# (6, 'Bupropion Threo Amino Alcohol', '95', '75735', '2.700 min')
# (7, 'Chlorophenylpiperazine', '89', '7182', '2.775 min')
# (8, 'Hydroxy-Bupropion', '94', '61693', '3.036 min')
# (9, 'Lidocaine', '64', '8287', '3.138 min')
# (10, 'Etomidate', '75', '4817', '3.190 min')
# (11, 'N-butyl pentylone', '61', '3828', '3.207 min')
# (12, 'Moclobemide', '67', '2531', '3.324 min')
# (13, 'Mepivacaine ISTD', '97', '35423', '3.651 min')
# (14, 'Sertraline', '86', '1982', '4.391 min')
# (15, 'Midazolam', '93', '2235', '4.886 min')
# (16, 'Fentanyl', '81', '432', '5.146 min')
# (17, 'Norchlorcyclizine', '92', '568', '5.153 min')
# (18, 'Trazodone', '92', '15730', '6.414 min')
