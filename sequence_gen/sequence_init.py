import time
import os
import re
import fitz  # type: ignore # PyMuPDF
from sample_dict import sample_type_dict, sample_container_dict

class sequence():
    def __init__(self, sample_number, sample_type, sample_container, barcode, method, batch_number):
        self.number = sample_number
        self.type = sample_type
        self.barcode = barcode
        self.container = sample_container
        self.method = method
        self.batch = batch_number
        self.abbrv = ""

    def __repr__(self):
        return (f"({self.number!r}, {self.type!r}, {self.barcode!r}, {self.container!r}, {self.method!r}, {self.batch!r}, {self.abbrv!r})")
    
    def __str__(self):
        return (f"{self.number}, {self.type}, {self.container}, {self.abbrv}")

    def __eq__(self, other):
        return self.barcode == other.barcode
    
    def transform_number(self):
        leading_chars = ""
        if len(self.number) > 10:
            if self.number[1].isdigit():
                leading_chars += self.number[0]
            if self.number[2].isdigit():
                leading_chars += self.number[0]
                leading_chars += self.number[1]
        self.abbrv += leading_chars + self.number[-8:-6] + "-" + self.number[-4:] + "_"

    def abbreviate_type(self):
        try:
            self.abbrv += sample_type_dict[self.type]
        except KeyError:
            print(f"Sample type {self.type} not found in Sample Type Dictionary")
            val1 = input(f"Enter the desired abbreviation for {self.type}: ").upper()
            sample_type_dict[self.type] = val1
            self.abbreviate_type()

    def abbreviate_container(self):
        try:
            self.abbrv += sample_container_dict[self.container]
        except KeyError:
            print(f"Sample container {self.container} not found in Sample Container Dictionary")
            val2 = input(f"Enter the desired abbreviation for {self.container}: ").upper()
            sample_container_dict[self.container] = val2
            self.abbreviate_container()
    

    
#probably need to handle how it will be called... where to save pdf... what info to get from the user
#maybe a search to see if 'TEST BATCH ' is in lines before proceeding
def read_sequence(seq_dir):
    samples = [] #will hold sample objects created here
    # Iterate through directory defined by filepath
    for filename in os.listdir(seq_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(seq_dir, filename)        
            doc = fitz.open(pdf_path)
            # Extract text from the first page
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                lines = text.strip().split('\n')
                batch_number = lines[3].strip().replace(",","")

                start_index = lines.index('TEST BATCH ') + 1
                end_index = lines.index('CRTestBatch') - 1

                cases = lines[start_index:end_index]
                #print(cases)
                for i in range(0, len(cases), 5):
                    sample_number = (cases[i])
                    sample_type = (cases[i+1]).upper()
                    barcode = (cases[i+2]).strip()
                    method = cases[i+3]
                    sample_container = cases[i+4].upper()
                    case_ID = barcode
                #create object
                    case_ID = sequence(sample_number, sample_type, sample_container, barcode, method, batch_number)
                #append object to samples list
                    samples.append(case_ID)
                #assign abbrv 
                    case_ID.transform_number()
                    case_ID.abbreviate_type()
                    case_ID.abbreviate_container()
                #confirmation print
                    print(case_ID)
                    #print(repr(case_ID))
    return samples



# [('2025-00048', 'BLOOD - HEART', '2301182', '50ML RED TOP', 'SCGEN', '12821', '25-00048_HBBRT'),
# ('2025-00053', 'BRAIN', '2301269', 'FRESH SPECIMEN CUP', 'SCGEN', '12821', '25-00053_BRNCUP'),
# ('2025-00099', 'BLOOD - HEART', '2302145', '50ML RED TOP', 'SCGEN', '12821', '25-00099_HBBRT'),
# ('2025-00115', 'BLOOD - AORTA', '2302625', '50ML RED TOP', 'SCGEN', '12821', '25-00115_AOBBRT'),
# ('2025-00118', 'BLOOD - ANTEMORTEM', '2303301', 'PURPLE TOP TUBE', 'SCGEN', '12821', '25-00118_AMBPRPT'),
# ('2025-00119', 'BLOOD - AORTA', '2302775', '50ML RED TOP', 'SCGEN', '12821', '25-00119_AOBBRT'),
# ('2025-00120', 'BLOOD - AORTA', '2302815', '50ML RED TOP', 'SCGEN', '12821', '25-00120_AOBBRT')]

if __name__ == "__main__":
    seq_dir = r'C:\Users\e314883\Desktop\python pdf\sequence_gen'
    print('running...')
    read_sequence(seq_dir)
