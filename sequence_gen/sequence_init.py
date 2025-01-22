import time
import os
import re
import fitz  # type: ignore # PyMuPDF

class sequence():
    def __init__(self, case, sample, barcode, container, method, batch):
        self.case = case
        self.sample = sample
        self.barcode = barcode
        self.container = container
        self.method = method
        self.batch = batch

    def __repr__(self):
        return (f"{self.case}, {self.type}, {self.container}")

    def __eq__(self, other):
        return self.barcode == other.barcode
    
def read_sequence(file):
    samples = [] #will hold sample objects created here
    # Iterate through directory defined by filepath
    for filename in os.listdir(batch_dir):
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
