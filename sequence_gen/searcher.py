import os
import re
import time



#simplify to name batch pdf
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
            print(f"--error--: {e}, while renaming {sample.path} to {new_path}")
            continue
        # keep sample.path up to date
        sample.path = new_path
    print("naming complete")

#adapt to find instrument/create dated folder
#and/or adapt to find sequence
def get_ISAR(method, TP_directory):
    for dir in os.listdir(TP_directory):
        if method in dir:
            TP = os.path.join(TP_directory, dir)
            #find TP folder
    for root, dirs, files in os.walk(TP):
        for file in files:
            if "Area Response" in file:
                source_path = os.path.join(root,file)
                return source_path

#adapt to find instrument log            
def get_MSA(LF_directory):
    for files in os.listdir(LF_directory):
        if 'LF-10' in files:
            source_path = os.path.join(LF_directory, files)
            #print(source_path)
            return source_path
    print('--error-- LF-10 not found -- cannot fill MSA')
    return

