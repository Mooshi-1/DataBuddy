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
                score = score[:2]
                if score == '10':
                    score = '100'
            if "Abundance" in line:
                parts = line.split('[')
                abundance = parts[1].split(']')[0].strip()
            if "Extracted spectrum" in line:
                parts = line.split('(')
                RT = parts[1].split(')')[0].strip()
    except:
        print(f'.pdf file is not an AMDIS report')
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
    #columns = ['Page Number', 'Drug Name', 'Score', 'Abundance', 'Retention']
def main():
    path = r'C:\Users\e314883\Desktop\locked_git_repo\AMDIS\2'
    for filename in os.listdir(path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(path, filename)
            print(f"Processing file: {filename}")
            info_list = extract_text_from_pdf(pdf_path)
            for info in info_list:
                print(info)

if __name__ == "__main__":
    main()
