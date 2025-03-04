"""
Created 03-03-25 -- adg
"""
#other options available
# check_var = tk.BooleanVar()
# checkbutton = ttk.Checkbutton(root, text="Enable Feature", variable=check_var)
# checkbutton.pack()

import tkinter as tk
from tkinter import ttk
import subprocess
import os
import datetime

version = "2.0" #3-4-25
script_path_screens = r""
script_path_quants = r""
script_path_sequence = r"G:\PDF DATA\DataBuddy\python-pdf\sequence\seq_main.py"
venv_path = r"G:\PDF DATA\DataBuddy\python-pdf\.venv\Scripts\python.exe"

def run_script(venv_path, script_path, *args):
    print(f"running script with args: {venv_path}\n{script_path}\n{list(args)}")
    try: 
        subprocess.run([venv_path, script_path] + list(args), check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running script: {e}")
    except FileNotFoundError:
        print(f"Script or the Python interpreter could not be found!")

def get_weekday():
    today = datetime.date.today()
    return today.strftime("%A")

# Set up the main tkinter window
def main(version, script_path_screens, script_path_quants, script_path_sequence, venv_path):
    root = tk.Tk()
    root.title(f"Data Buddy - {version}")
    root.geometry("800x400")

    date = get_weekday()
    header = ttk.Label(root, text=f"Happy {date}.", font=("Arial", 16, "bold"))
    header.pack(pady=10)
    
    readme = ttk.Label(root, text="Use the tabs below to navigate the program \
                       \nIt may take a moment to load a tab after swapping \
                       \nFor more info, check the 'help' tab", font=("Arial", 14))
    readme.pack(pady=10)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

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
    renamer_check = ttk.Checkbutton(screens, text="Renamer mode?", onvalue='-r', offvalue=None, variable=renamer_var).pack()

    ttk.Button(screens, text="Run Screen Binder", command=lambda: run_script(venv_path, script_path_screens, \
                    sc_batch.get(), sc_var.get())).pack()


    quants = ttk.Frame(notebook)
    notebook.add(quants, text="Quants")
    
    sequence = ttk.Frame(notebook)
    notebook.add(sequence, text="Sequence")

    ttk.Label(sequence, text="Enter your initials: ").pack()
    initials = ttk.Entry(sequence)
    initials.pack()

    ttk.Button(sequence, text="Run Sequence Generator", command=lambda: run_script(venv_path, script_path_sequence, initials.get().upper())).pack()


    # Start the tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main(version, script_path_screens, script_path_quants, script_path_sequence, venv_path)
