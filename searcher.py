import os
import re
import shutil
#testing comment below
#input_dir = r"/home/mooshi_1/workspace/github.com/Mooshi-1/Work/python-pdf/T_ENV/2025/01/12345/"

folder_pattern = re.compile(r'([A-Za-z]{0,2}\d+-\d)')

def Shuttle(input_dir):
    for folders in os.listdir(input_dir):
        path_folders = os.path.join(input_dir, folders)
        if os.path.isdir(path_folders) and folder_pattern.match(folders):
            print(f"Copying contents of directory: {path_folders}")
            copy_contents(path_folders, input_dir)

def copy_contents(src_dir, dest_dir):
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isdir(src_path):
            # Skip directories to avoid moving them inside input_dir
            print(f"Skipping directory: {src_path}")
            continue
        else:
            print(f"Copying file: {src_path} to {dest_path}")
            shutil.copy2(src_path, dest_path)

#testing comment below
#Shuttle(input_dir)

def binder_dir(input_dir):
    binder_path = os.path.join(input_dir, "--binder files--")
    if not os.path.exists(binder_path):
        os.makedirs(binder_path)
        print(f"made directory {binder_path}")

#binder_dir(input_dir)
#need to change -- sys.argv