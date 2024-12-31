import os
import re
import shutil
#testing comment below
#input_dir = r"C:\Users\e314883\Desktop\python pdf\PDF DATA\2024\12\12773\CASE DATA"

folder_pattern = re.compile(r'([A-Za-z]{0,2}\d+-\d)')

def Shuttle(input_dir):
    for folders in os.listdir(input_dir):
        path_folders = os.path.join(input_dir, folders)
        if os.path.isdir(path_folders) and folder_pattern.match(folders):
            print(f"Checking contents of directory: {folders}")
            move_contents(path_folders, input_dir)

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
        dest_path = os.path.join(dest_dir, f"{base_name}_{counter:03d}{extension}")
        while os.path.exists(dest_path):
            counter +=1
            dest_path = os.path.join(dest_dir, f"{base_name}_{counter:03d}{extension}")
        
        print(f"Moving file: {item} to {dest_dir}")
        shutil.move(src_path, dest_path)


#testing comment below
#Shuttle(input_dir)

def binder_dir(input_dir):
    binder_path = os.path.join(input_dir, "--binder files--")
    if not os.path.exists(binder_path):
        os.makedirs(binder_path)
        print(f"made directory {binder_path}")
    return binder_path

#binder_dir(input_dir)
input_dir = r"C:\Users\e314883\Desktop\python pdf\PDF DATA\2024\12\12777\CASE DATA"

def ShuttleHome(input_dir):
    for contents in os.listdir(input_dir):
        content_path = os.path.join(input_dir, contents)
        
        if contents.endswith('.pdf'):          
            number = contents.split('_')[0]
            number = number.split('-')[1]
            print(number)
            
        if os.isdir(contents) == True:
            case_folder = contents
        if number in case_folder:
            shutil.move(os.path.join(input_dir, number), os.path.join(input_dir, case_folder))
            
        
ShuttleHome(input_dir)

