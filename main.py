"""
Created 03-03-25 -- adg
"""
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import subprocess
import os
import datetime
import threading

import audit
import logging

#things to code:
#sequence instrument 1/2 and enter extraction date (leave blank for today)

version = "2.4" #3-27-25

base_dir = os.path.dirname(os.path.abspath(__file__))
# Construct paths dynamically
script_path_screens = os.path.join(base_dir, "screens", "screen_main.py")
script_path_quants = os.path.join(base_dir, "quants", "quant_main.py")
script_path_sequence = os.path.join(base_dir, "sequence", "seq_main.py")
script_path_carryover = os.path.join(base_dir, "autoprintZ", "carryover.py")
venv_path = os.path.join(base_dir, ".venv", "Scripts", "python.exe")

def run_script(venv_path, script_path, *args):
    print(f"running script with args: {venv_path}\n{script_path}\n{list(args)}")

    env = os.environ.copy()
    env["LOG_FILE"] = "log.log"

    try: 
        subprocess.run([venv_path, script_path] + list(args), check=True, env=env)
        logging.info("Subprocess completed")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running script: {e}")
    except FileNotFoundError:
        print(f"Script or the Python interpreter could not be found!")

def start_thread(venv_path, script_path, *args):
    thread = threading.Thread(target=run_script, args=(venv_path, script_path, *args))
    thread.start()

def get_weekday():
    today = datetime.date.today()
    return today.strftime("%A")


def show_popup():
    messagebox.showinfo("Notification", "The script is running and your files are loading. Check the terminal!")

def main():
# # TK MAIN WINDOW
    root = tk.Tk()
    root.title(f"Data Buddy - {version}")
    root.geometry("800x700")


# header
    date = get_weekday()
    header = ttk.Label(root, text=f"Happy {date}.", font=("Arial", 16, "bold"))
    header.pack(pady=10)
    
    readme = ttk.Label(root, text="Use the tabs below to navigate the program \
                       \nAfter pressing 'Run', please wait a moment while it loads the relevant files \
                       \nFor more info, check the 'help' tab", font=("Arial", 14))
    readme.pack(pady=10)

## create notebook tabs ##
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

## IO ##
    io = ttk.Frame(root)
    io.pack(pady=10)

## START SCREENS TAB ##
    screens = ttk.Frame(notebook)
    notebook.add(screens, text="Screens")

    ttk.Label(screens, text="Batch Number: ").pack(padx=10, pady=10)
    sc_batch = ttk.Entry(screens)
    sc_batch.pack(padx=10, pady=10)

    ttk.Label(screens, text="Method: ").pack(padx=10, pady=10)
    sc_methods = ["SCRNZ", "SCLCMSMS", "SCGEN"]
    sc_var = tk.StringVar()
    combobox = ttk.Combobox(screens, textvariable=sc_var, values=sc_methods)
    combobox.pack(padx=10, pady=10)

    renamer_var = tk.StringVar(value=None)
    renamer_check = ttk.Checkbutton(screens, text="Rename only mode?", onvalue='-r', offvalue=None, variable=renamer_var).pack()

    ttk.Button(screens, text="Run Screen Binder", command=lambda: [start_thread(venv_path, script_path_screens, \
                    sc_batch.get(), sc_var.get(), renamer_var.get()), show_popup()]).pack()
    
    ttk.Label(screens, text="Requirements: \
              \n-Data must be in BATCH PACK DATA, CASE DATA, or auto-generated CASE DATA subfolders\
              \n-Data that is not in the directories listed above will be ignored by the script \
              \n-Data that is open in Adobe or open in a windows explorer preview window may have issues -- make sure to close them\
              \n \
              \n-If you have reinjects, manually bind them to the appropriate file beforehand and ensure that no duplicate files are present \
              \n-Manually bind your sequence to the batch pack after running. \
              \n \
              \n \
              \n future improvements are coming!").pack(pady=20)
    


## START QUANTS TAB ##
    quants = ttk.Frame(notebook)
    notebook.add(quants, text="Quants")

    ttk.Label(quants, text="Batch Number: ").pack(padx=10, pady=10)
    qt_batch = ttk.Entry(quants)
    qt_batch.pack(padx=10, pady=10)

    ttk.Label(quants, text="Method: ").pack()
    qt_methods = ["SQVOL", "QTABUSE", "QTSTIM", "QTPSYCH", "QTBZO1", "QTBZO2", "QT"]
    qt_var = tk.StringVar()
    combobox2 = ttk.Combobox(quants, textvariable=qt_var, values=qt_methods)
    combobox2.pack()

    ttk.Label(quants, text="Date in MM/DD/YY format WITH slashes: ").pack()
    qt_date = ttk.Entry(quants)
    qt_date.pack()

    ttk.Label(quants, text="Enter your initials: ").pack()
    qt_initials = ttk.Entry(quants)
    qt_initials.pack()

    ttk.Button(quants, text="Run Quants Binder", command=lambda: [start_thread(venv_path, script_path_quants, \
                            qt_batch.get(), qt_var.get().upper(), qt_date.get(), qt_initials.get().upper()), show_popup()]).pack()
    
    ttk.Label(quants, text="Requirements: \
              \n-Data must be in BATCH PACK DATA, CASE DATA, or auto-generated CASE DATA subfolders\
              \n-Data that is not in the directories listed above will be ignored by the script \
              \n-Data that is open in Adobe or open in a windows explorer preview window may have issues -- make sure to close them\
              \n \
              \n-If you have MSA's, Excel must be closed on your computer to fill the LF-10/LF-11 forms \
              \n-Make sure your curve and sequence are printed, the script will handle them appropriately. \
              \n-Extraction date and initials can be left empty -- these are for the LJ charts which are not being used currently \
              \n \
              \n \
              \n future improvements are coming!").pack(pady=20)

## START SEQUENCE TAB ##
    sequence = ttk.Frame(notebook)
    notebook.add(sequence, text="Sequence")

    ttk.Label(sequence, text="Enter your initials: ").pack()
    initials = ttk.Entry(sequence)
    initials.pack()

    ttk.Button(sequence, text="Run Sequence Generator", command=lambda: [start_thread(venv_path, script_path_sequence, initials.get().upper()), show_popup()]).pack()


    ttk.Label(sequence, text=r""" 
-New feature: CME Test Batches with different Methods is now supported.
    A test batch report for QTABUSE and separate batch report for QTSTIM will be separated into 
    two sequences automatically. 2 test batch reports for SCRNZ will still create only one sequence.

Requirements:
    -This script looks in the directory G:\PDF DATA\TEST BATCH REPORTS for pdf printed Test Batches,
    then prepares a sequence suitable for the instrument/method being prepared
    -You can make extra directories, 'Archive', 'Old batches', etc, without issue -- 
    they are not checked or recognized by the script
                
-This script takes 5-10 seconds to load due to the hundreds of sample types/containers that we have. 
Don't worry, it's working!

future improvements are coming!""").pack(pady=20)
    
    
## START CARRYOVER TAB ##
    carryover = ttk.Frame(notebook)
    notebook.add(carryover, text="Z Carryover")

    ttk.Label(carryover, text="Enter the network path where the raw data is: ").pack()
    location = ttk.Entry(carryover)
    location.pack()
    ttk.Label(carryover, text="make sure that no other files are in the directory except for the AMDIS reports in order they were printed").pack()

    ttk.Button(carryover, text="Run Carryover Check", command=lambda: [start_thread(venv_path, script_path_carryover, location.get()), show_popup()]).pack()


    ttk.Label(carryover, text=r""" 
Requirements:
    -This script only accepts entire network paths to a directory
    -The only files inside the above directory are the printed AMDIS reports, in the order they were injected
    -It is important to not rename these files before running carryover to ensure proper order
    
Output:
    -A single excel file with 3 tabs. 
    -The first tab contains a list of samples for reinject and the analytes which are potentially carryover
        The script checks for carryover in a rudimentary manner, and should be overridden by an 
        analyst if necessary.
              
    -The second tab contains a summation of each AMDIS pdf report fed into it.
        The analyte name and abundance found in each report is compared to the previous report.
        If the same analyte appeared in the previous sample at a larger abundance, the current sample
        is marked for carryover. 
              
        If this tab is not accurate to the injection order or contains "ERROR"/repeated fields, 
        the automated carryover check is invalid and should be done manually instead.
              
    -The third tab contains a new sequence directly for copy/paste into Agilent instrument software.
        Adjust with analyst discretion as necessary.

future improvements are coming!""").pack(pady=20)


## START HELP TAB ##
    help = ttk.Frame(root)
    notebook.add(help, text="Help")

    help_text = r""" 
What's going on here?

In previous versions of the data manipulation scripts, each one would be a separate executable file.
This new program is GUI (graphical user interface) that serves as a launch-pad for the same data manipulation scripts.
Each of the tabs corresponds to a separate script, and the data entered before you hit "RUN" is passed as a command-line argument, in the same way you were prompted before. 

You can think of it like a 'face' to the same commands you've been running before.

This new setup makes it much easier for the maintainer (me) to not only push updates, but also continue to scale it with more and more features. 

There will be constant updates as I'm learning my own way around the GUI, so don't be too surprised as things shift around. 

Should something appear to be terribly wrong, the old versions of the data-binders will be in "G:\PDF DATA\Python" for a few weeks.
"""
    help_box = tk.Text(help, wrap="word", font=("Arial", 13))
    help_box.insert("1.0", help_text)
    help_box.config(state="disabled")
    help_box.pack(padx=10, pady=10)



## TK MAIN LOOP ##
    root.mainloop()

if __name__ == "__main__":
    logging.info("Application started")
    main()
