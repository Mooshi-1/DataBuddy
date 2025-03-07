"""
Created 03-03-25 -- adg
"""

import tkinter as tk
from tkinter import ttk
import subprocess
import os
import datetime
import threading
from queue import Queue

version = "2.1" #3-5-25
script_path_screens = r"G:\PDF DATA\DataBuddy\screens\screen_main.py"
script_path_quants = r"G:\PDF DATA\DataBuddy\quants\quant_main.py"
script_path_sequence = r"G:\PDF DATA\DataBuddy\sequence\seq_main.py"
script_path_carryover = r"G:\PDF DATA\DataBuddy\autoprintZ\carryover.py"
venv_path = r"G:\PDF DATA\DataBuddy\.venv\Scripts\python.exe"

def run_script(queue, venv_path, script_path, *args):
    print(f"running script with args: {venv_path}\n{script_path}\n{list(args)}")
    try: 
        process = subprocess.Popen([venv_path, script_path] + list(args), 
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True)

        while True:
            output = process.stdout.readline()
            if output:
                queue.put(output.strip())
            if process.poll() is not None:
                break

        stderr = process.stderr.read().strip()
        if stderr:
            queue.put(f"Error: {stderr}")
        queue.put("COMPLETE")

    except FileNotFoundError:
        print(f"Script or the Python interpreter could not be found!")
    except Exception as e:
        queue.put(f"Unexpected error: {e}")

def send_input_to_process(process, input_text):
    if process and process.stdin:
        process.stdin.write(input_text + "\n")
        process.stdin.flush()

def get_weekday():
    today = datetime.date.today()
    return today.strftime("%A")

def start_thread(queue, progress_bar, status_label, input_box, venv_path, script_path, *args):
    status_label.config(text="Running script...", foreground="blue")
    thread = threading.Thread(target=run_script, args=(queue, venv_path, script_path, *args))
    thread.start()
    check_queue(queue, progress_bar, status_label, input_box)

def check_queue(queue, progress_bar, status_label, input_box):
    try:
        while not queue.empty():
            message = queue.get_nowait()
            if message == "COMPLETE":
                progress_bar.stop()
                status_label.config(text="Script completed!", foreground="green")
                input_box.config(state="disabled")
            else:
                status_label.config(text=message, foreground="blue")
    except Exception as e:
        status_label.config(text=f"Error: {e}", foreground="red")
    finally:
        if progress_bar["value"] < 100:
            progress_bar.after(100, check_queue, queue, progress_bar, status_label, input_box)

def main():
# # TK MAIN WINDOW
    root = tk.Tk()
    root.title(f"Data Buddy - {version}")
    root.geometry("800x700")

# start Queue
    queue = Queue()

# header
    date = get_weekday()
    header = ttk.Label(root, text=f"Happy {date}.", font=("Arial", 16, "bold"))
    header.pack(pady=10)
    
    readme = ttk.Label(root, text="Use the tabs below to navigate the program \
                       \nAfter pressing 'Run', please wait a moment while it loads the relevant files \
                       \nFor more info, check the 'help' tab", font=("Arial", 14))
    readme.pack(pady=10)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

#progress bar
    progress_bar = ttk.Progressbar(root, mode="indeterminate")
    progress_bar.pack(pady=10, fill="x")

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

## START CARRYOVER TAB ##
    carryover = ttk.Frame(notebook)
    notebook.add(carryover, text="Z Carryover")

    ttk.Label(carryover, text="Enter the network path where the raw data is: ").pack()
    location = ttk.Entry(carryover)
    location.pack()
    ttk.Label(carryover, text="make sure that no other files are in the directory except for the AMDIS reports in order they were printed").pack()

    ttk.Button(carryover, text="Run Carryover Check", command=lambda: run_script(venv_path, script_path_carryover, location.get())).pack()

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

#status, progress, input, output
    status_label = ttk.Label(root, text="Ready", font=("Arial", 12), foreground="green")
    status_label.pack(pady=10)

    # Progress Bar
    progress_bar = ttk.Progressbar(root, mode="indeterminate")
    progress_bar.pack(pady=10, fill="x")

    # Output Box
    output_box = tk.Text(root, wrap="word", height=15, font=("Arial", 12))
    output_box.pack(pady=10, padx=10, fill="both", expand=True)

    # Input Box
    input_box = ttk.Entry(root)
    input_box.pack(pady=10, padx=10, fill="x")
    input_box.bind("<Return>", lambda event: send_input_to_process(process, input_box.get()))

## IO ##
    io = ttk.Frame(root)
    io.pack(pady=10)

## TK MAIN LOOP ##
    root.mainloop()

if __name__ == "__main__":
    main()
