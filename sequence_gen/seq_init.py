import time
import os
import re
import fitz  # type: ignore # PyMuPDF
from sample_dict import sample_type_dict, sample_container_dict

class sequence():
    def __init__(self, sample_number, sample_type, sample_container, barcode, abbrv=None, comment=None):
        self.number = sample_number
        self.type = sample_type
        self.container = sample_container
        self.barcode = barcode
        self.comment = comment
        self.abbrv = "" if abbrv is None else abbrv

    def __repr__(self):
        return (f"({self.number!r}, {self.type!r}, {self.container!r}, {self.barcode!r}, {self.comment!r}, {self.abbrv!r})")
    
    def __str__(self):
        return f"{self.abbrv}, {self.comment}"

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

    def add_comment(self):
        if self.comment == None:
            if self.type == 'BRAIN':
                self.abbrv += "_X2"
            if self.type == 'LIVER':
                self.abbrv += "_X5"
            if self.type == 'GASTRIC':
                self.abbrv += "_X10"
            return
        elif ',' in self.comment:
            notes = self.comment.split(',')
            self.comment = [item.strip() for item in notes]
            self.add_comment()
        else:
            if isinstance(self.comment, list):
                for item in self.comment:
                    self.process_comments(item)
            else:
                self.process_comments(self.comment)

    def process_comments(self, item):
        print(item)
        if item.startswith('X'):
            self.abbrv += f"_{item}"
            self.diln = True
        if item.startswith('P'):
            self.prio = True
        if item.startswith('M'):
            self.MSA = True
        if item.startswith('SR'):
            self.SR = True
        if item.startswith('SINGLE'):
            self.single = True


  
    

    
#probably need to handle how it will be called... where to save pdf... what info to get from the user
#maybe a search to see if 'TEST BATCH ' is in lines before proceeding
def read_sequence(seq_dir):
    samples = [] #will hold sample objects created here
    # Iterate through directory defined by filepath
    for filename in os.listdir(seq_dir):
        if filename.endswith(".pdf"):
            #counter = 0
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

                    comment = None


                    barcode_rect = page.search_for(barcode)
                    print(f'barcode = {barcode_rect}')
                    expand = 2
                    sample_rect = barcode_rect[0]

                    search_area = fitz.Rect(sample_rect.x0 - 285, #expand this one more to cover sample
                                            sample_rect.y0 - expand,
                                            sample_rect.x1 + expand, 
                                            sample_rect.y1 + expand)

                    annots = page.annots()
                    if annots is not None:
                        for annot in annots:
                            if search_area.intersects(annot.rect):
                                comment = annot.info.get('content', '').strip().upper()
                                #print(comment)

                    case_ID = barcode
                #create object
                    case_ID = sequence(sample_number, sample_type, sample_container, barcode, None, comment)
                    samples.append(case_ID)
                #assign abbrv 
                    case_ID.transform_number()
                    case_ID.abbreviate_type()
                    case_ID.abbreviate_container()
                    case_ID.add_comment()
                #confirmation print
                    print(case_ID)
                    #print(repr(case_ID))
    return samples, method, batch_number



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
