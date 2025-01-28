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
        return (f"({self.number}, {self.type}, {self.barcode}, {self.container}, {self.method}, {self.batch})")
    
    def __str__(self):
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
                batch_number = lines[3].strip()

                start_index = lines.index('TEST BATCH ') + 1
                end_index = lines.index('CRTestBatch') - 1

                cases = lines[start_index:end_index]
                print(cases)
                for i in range(0, len(cases), 5):
                    sample_number = (cases[i])
                    sample_type = (cases[i+1]).upper()
                    barcode = (cases[i+2]).strip()
                    method = cases[i+3]
                    sample_container = cases[i+4]
                    case_ID = barcode
                    case_ID = sequence(sample_number, sample_type, sample_container, barcode, method, batch_number)
                    samples.append(case_ID)
    print(samples)


#[(2024-03606, Blood - Heart, 2294548, 50ml Red Top, SCGEN, 12,821), 
# (2024-03650, Brain, 2295805, Fresh Specimen Cup, SCGEN, 12,821), 
# (2024-03756, Blood - Heart, 2299168, 50ml Red Top, SCGEN, 12,821), 
# (2025-00001, Blood - Aorta, 2299284, 50ml Red Top, SCGEN, 12,821), 
# (2025-00020, Blood - Aorta, 2300494, 50ml Red Top, SCGEN, 12,821), 
# (2025-00024, Blood - Heart, 2300139, 50ml Red Top, SCGEN, 12,821), 
# (2025-00027, Blood - Heart, 2300177, 50ml Red Top, SCGEN, 12,821), 
# (2025-00028, Blood - Heart, 2300279, 50ml Red Top, SCGEN, 12,821), 
# (2025-00031, Blood - Heart, 2300329, 50ml Red Top, SCGEN, 12,821), 
# (2025-00044, Blood - Aorta, 2301033, 50ml Red Top, SCGEN, 12,821), 
# (2025-00048, Blood - Heart, 2301182, 50ml Red Top, SCGEN, 12,821), 
# (2025-00053, Brain, 2301269, Fresh Specimen Cup, SCGEN, 12,821), 
# (2025-00099, Blood - Heart, 2302145, 50ml Red Top, SCGEN, 12,821), 
# (2025-00115, Blood - Aorta, 2302625, 50ml Red Top, SCGEN, 12,821), 
# (2025-00118, Blood - Antemortem, 2303301, Purple Top Tube, SCGEN, 12,821), 
# (2025-00119, Blood - Aorta, 2302775, 50ml Red Top, SCGEN, 12,821), 
# (2025-00120, Blood - Aorta, 2302815, 50ml Red Top, SCGEN, 12,821), 
# (2025-00127, Blood - Aorta, 2303007, 50ml Red Top, SCGEN, 12,821), 
# (2025-00132, Blood - Aorta, 2303199, 50ml Red Top, SCGEN, 12,821), 
# (2025-00134, Blood - Antemortem, 2303599, Purple Top Tube, SCGEN, 12,821), 
# (2025-00134, Serum - Antemortem, 2303600, Clear Top Tube SST, SCGEN, 12,821)]

if __name__ == "__main__":
    seq_dir = r'C:\Users\e314883\Desktop\python pdf\sequence_gen'
    print('running...')
    read_sequence(seq_dir)
