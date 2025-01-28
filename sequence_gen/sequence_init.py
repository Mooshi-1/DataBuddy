import time
import os
import re
import fitz  # type: ignore # PyMuPDF

class sequence():
    def __init__(self, sample_number, sample_type, sample_container, barcode, method, batch_number):
        self.number = sample_number
        self.type = sample_type
        self.barcode = barcode
        self.container = sample_container
        self.method = method
        self.batch = batch_number

    def __repr__(self):
        return (f"{self.number}, {self.type}, {self.container}")

    def __eq__(self, other):
        return self.barcode == other.barcode
    
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

                print(lines)
                
                batch_number = lines[3]
                print(batch_number)

                start_index = lines.index('TEST BATCH ') + 1
                end_index = lines.index('CRTestBatch') - 1
                #print(end_index)

                cases = lines[start_index:end_index]
                print(cases)
                for i in range(0, len(cases), 5):
                    sample_number = (cases[i])
                    sample_type = (cases[i+1])
                    barcode = (cases[i+2]).strip()
                    method = cases[i+3]
                    sample_container = cases[i+4]
                    case_ID = barcode
                    case_ID = sequence(sample_number, sample_type, sample_container, barcode, method, batch_number)
                    samples.append(case_ID)
                    #print(samples)

if __name__ == "__main__":
    seq_dir = r'C:\Users\e314883\Desktop\python pdf\sequence_gen'
    print('running...')
    read_sequence(seq_dir)
