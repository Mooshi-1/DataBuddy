import os
import re
import shutil

folder_pattern = re.compile(r'([A-Za-z]{0,2}\d+-\d+)')

def Shuttle(input_dir):
    for folders in os.listdir(input_dir):
        path_folders = os.path.join(input_dir, folders)
        if os.path.isdir(path_folders) and folder_pattern.match(folders):
            #print(f"Checking contents of directory: {folders}")
            move_contents(path_folders, input_dir)
    print("completed checking case directories")

def move_contents(src_dir, dest_dir):
    counter = 0
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        if os.path.isdir(src_path):
            # Skip directories to avoid moving them inside input_dir
            print(f"Skipping directory: {src_path}")
            continue
        #add 3 digit counter to files
        base_name, extension = os.path.splitext(item)
        dest_path = os.path.join(dest_dir, f"{base_name}{extension}")
        while os.path.exists(dest_path):
            counter +=1
            dest_path = os.path.join(dest_dir, f"{base_name}_{counter:03d}{extension}")

        #print(f"Moving file: {item} to {dest_dir}")
        shutil.move(src_path, dest_path)

def binder_dir(input_dir, counter=0):
    binder_path = os.path.join(input_dir, f"--binder files--" if counter == 0 else f"--binder files{counter}--")
    if os.path.exists(binder_path):
        return binder_dir(input_dir, counter + 1)
    else:
        os.makedirs(binder_path)
        print(f"made directory {binder_path}")
        return binder_path


def ShuttleHome(input_dir):
    #list contents
    print("returning contents to individual case folders:")
    for contents in os.listdir(input_dir):

        
        #look for pdfs, extract last 4 of case number as string
        if contents.endswith('.pdf'):
            content_path = os.path.join(input_dir, contents)
            #print("found a pdf")
            try:
                number = str(contents.split('_')[0].split('-')[1])
            except Exception as e:
                print(f"could not find folder for {contents}")
                continue
            #check folders and look for case number in folder
            for folder in os.listdir(input_dir):
                folder_path = os.path.join(input_dir, folder)
                if os.path.isdir(folder_path) and number in folder:
                    #if found, attempt to move
                    try:
                        shutil.move(content_path, os.path.join(folder_path, contents))
                        #print(f"moved {contents} to {folder}")
                        continue
                    except Exception as e:
                        print(e)
                        continue                           
    print("completed moving data files to individual directories")

def FindBatch(data_dir, batch_num):
    
    print("finding batch...")
    for year in os.listdir(data_dir):
        year_dir = os.path.join(data_dir, year)
        if not os.path.isdir(year_dir):
            continue
        
        for month in os.listdir(year_dir):
            month_dir = os.path.join(year_dir, month)
            if not os.path.isdir(month_dir):
                continue
            
            for batch in os.listdir(month_dir):
                if batch == str(batch_num):
                    print(f"found batch {batch_num}")
                    
                    case_dir = os.path.join(month_dir, batch, "CASE DATA")
                    print(f"Case Directory = {case_dir}")
                    qc_dir = os.path.join(month_dir, batch, "BATCH PACK DATA")
                    print(f"QC Directory = {qc_dir}")
                    return case_dir, qc_dir
    return None, None

if __name__ == "__main__":
    input_dir = r"C:\Users\e314883\Desktop\python pdf\PDF DATA\2025\01\12786\CASE DATA"

    Shuttle(input_dir)