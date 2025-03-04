"""
Created 03-03-25 -- adg
"""

import tkinter as tk
from tkinter import ttk
import subprocess
import os
import datetime

version = "2.0" #3-4-25
script_path_screens = r"G:\PDF DATA\DataBuddy\screens\screen_main.py"
script_path_quants = r"G:\PDF DATA\DataBuddy\quants\quant_main.py"
script_path_sequence = r"G:\PDF DATA\DataBuddy\sequence\seq_main.py"
venv_path = r"G:\PDF DATA\DataBuddy\.venv\Scripts\python.exe"

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


def main(version, script_path_screens, script_path_quants, script_path_sequence, venv_path):
## TK MAIN WINDOW
    root = tk.Tk()
    root.title(f"Data Buddy - {version}")
    root.geometry("800x700")

    date = get_weekday()
    header = ttk.Label(root, text=f"Happy {date}.", font=("Arial", 16, "bold"))
    header.pack(pady=10)
    
    readme = ttk.Label(root, text="Use the tabs below to navigate the program \
                       \nAfter pressing 'Run', please wait a moment while it loads the relevant files \
                       \nFor more info, check the 'help' tab", font=("Arial", 14))
    readme.pack(pady=10)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

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

    ttk.Button(screens, text="Run Screen Binder", command=lambda: run_script(venv_path, script_path_screens, \
                    sc_batch.get(), sc_var.get(), renamer_var.get())).pack()

## START QUANTS TAB ##
    quants = ttk.Frame(notebook)
    notebook.add(quants, text="Quants")

    ttk.Label(quants, text="Batch Number: ").pack(padx=10, pady=10)
    qt_batch = ttk.Entry(quants)
    qt_batch.pack(padx=10, pady=10)

    ttk.Label(quants, text="Method: ").pack()
    qt_methods = ["SQVOL", "QTABUSE", "QT"]
    qt_var = tk.StringVar()
    combobox2 = ttk.Combobox(quants, textvariable=qt_var, values=qt_methods)
    combobox2.pack()

    ttk.Label(quants, text="Date in MM/DD/YY format WITH slashes: ").pack()
    qt_date = ttk.Entry(quants)
    qt_date.pack()

    ttk.Label(quants, text="Enter your initials: ").pack()
    qt_initials = ttk.Entry(quants)
    qt_initials.pack()

    ttk.Button(quants, text="Run Quants Binder", command=lambda: run_script(venv_path, script_path_quants, \
                            qt_batch.get(), qt_var.get().upper(), qt_date.get(), qt_initials.get().upper())).pack()

## START SEQUENCE TAB ##
    sequence = ttk.Frame(notebook)
    notebook.add(sequence, text="Sequence")

    ttk.Label(sequence, text="Enter your initials: ").pack()
    initials = ttk.Entry(sequence)
    initials.pack()

    ttk.Button(sequence, text="Run Sequence Generator", command=lambda: run_script(venv_path, script_path_sequence, initials.get().upper())).pack()

## START HELP TAB ##
    help = ttk.Frame(root)
    notebook.add(help, text="Help")

    help_text = """ \
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
    main(version, script_path_screens, script_path_quants, script_path_sequence, venv_path)
