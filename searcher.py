import os


input_dir = r"/home/mooshi_1/workspace/github.com/Mooshi-1/Work/python-pdf/T_ENV/2025/01/12345/"


def Searcher(input_dir):


    for files in os.listdir(input_dir):
        print(files)
    
    
    
    
Searcher(input_dir)