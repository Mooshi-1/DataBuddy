"""
Created 03-03-25 -- adg
"""
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
import subprocess
import os
import datetime
import threading
import itertools
import time

import audit
import logging

#things to code:
#figure out how to encode ascii art into terminal
#some sort of loading/confirmation that script has started in terminal
#spinny/loady wheel
#get rid of notification popup once working

#font / font size overhaul
#button styles with ttk bootstrap
#bootstyle = "success"
#explore other widgets

#SQVOL - anything in CUP -- add blanks
#reinject/reassign tracker + whole batch analysis

#Z SCREENS - what else do we need?
# C > G > C transfer and folder creation
# AMDIS printer updates, choose which iteration to start the loop on
# fix extra spaces in RI generation

#quant reports / tox req time and case assignment time, update stats

#"help" tab to open training docs like 'how to use sequence generator'
#helpful images to explain the process


version = "3.2" #4-15-25

##### SUBPROCESSES ######

base_dir = os.path.dirname(os.path.abspath(__file__))
# Construct paths dynamically
script_path_screens = os.path.join(base_dir, "screens", "screen_main.py")
script_path_quants = os.path.join(base_dir, "quants", "quant_main.py")
script_path_sequence = os.path.join(base_dir, "sequence", "seq_main.py")
script_path_carryover = os.path.join(base_dir, "autoprintZ", "carryover.py")
script_path_Zprint = os.path.join(base_dir,"autoprintZ", "AMDIS_printer.py")
script_path_rename = os.path.join(base_dir,"rename", "file_renamer.py")
venv_path = os.path.join(base_dir, ".venv", "Scripts", "python.exe")

class ProcessManager:
    def __init__(self, command, env=None, ui_callback=None):
        #print('starting pm class')
        self.process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            env=env,
            encoding='utf-8',
            errors='replace'
        )
        self.ui_callback = ui_callback
        self.output_thread = threading.Thread(target=self.read_output, daemon=True)
        self.output_thread.start()

    def read_output(self):
        """Read output asynchronously and update GUI"""
        for line in iter(self.process.stdout.readline, ''):
            #print(f'raw line received: {repr(line)}')
            self.handle_output(line)

    def handle_output(self, line):
        """send subprocess output to GUI"""
        if self.ui_callback:
            self.ui_callback(line)
        else:
            print(line,end="")

    def send_input(self, input_text):
        """Send input to the subprocess."""
        if self.process and self.process.stdin:
            if self.ui_callback:
                self.ui_callback(f"> {input_text}\n")
            self.process.stdin.write(input_text + "\n")
            self.process.stdin.flush()

    def terminate(self):
        """Terminate the subprocess."""
        if self.process:
            self.process.terminate()
        self.process = None

class Spinner:
    def __init__(self, ui_callback, message="Working...", delay=0.05):
        self.spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        self.delay = delay
        self.message = message
        self.ui_callback = ui_callback
        self._stop_event = threading.Event()
        self.thread = None
        self._last_spinner_line = ""

    def _spin(self):
        while not self._stop_event.is_set():
            spinner_char = next(self.spinner)
            current_line = f"\r{self.message} {spinner_char}"
            self.ui_callback(f"SPINNER:{current_line}")
            self._last_spinner_line = current_line
            time.sleep(self.delay)

    def start(self):
        if self.thread and self.thread.is_alive():
            return
        self._stop_event.clear()
        self.ui_callback(f"SPINNER:{self.message} ")
        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()

    def stop(self):
        if not self.thread and self.thread.is_alive():
            return
        self._stop_event.set()
        self.thread.join(timeout=1.0)
        self.ui_callback(f"\nSCRIPT START\n")

##### MAIN FUNCTION #####

def main():
# # TK MAIN WINDOW
    #root = tk.Tk()
    root = ttk.Window(themename="darkly")
    root.title(f"Data Buddy - {version}")
    root.geometry("1500x800")

    pm = None
    spinner = None

    # RUN
    def run_script(venv_path, script_path, *args):
        print(f"running script with args: {venv_path}\n{script_path}\n{list(args)}")

        env = os.environ.copy()
        env["LOG_FILE"] = "log.log"

        script_name = os.path.basename(script_path)

        try: 
            nonlocal pm, spinner
            #print('starting pm')
            update_output("CLEAR_ALL")
            spinner = Spinner(update_output, message=f"Loading file {script_name}...")
            spinner.start()
            pm = ProcessManager([venv_path, script_path] + list(args), env=env, ui_callback=update_output)
            #logging.info("Subprocess completed")
        except subprocess.CalledProcessError as e:
            spinner.stop()
            print(f"An error occurred while running script: {e}")
        except FileNotFoundError:
            spinner.stop()
            print(f"Script or the Python interpreter could not be found!")

    def start_thread(venv_path, script_path, *args):
        thread = threading.Thread(target=run_script, args=(venv_path, script_path, *args))
        thread.start()

    def get_weekday():
        today = datetime.date.today()
        return today.strftime("%A")

# header
    date = get_weekday()
    header = ttk.Label(root, text=f"Happy {date}.", font=("Arial", 16, "bold"))
    header.pack(pady=10, side='top')
    
    readme = ttk.Label(root, text="Use the tabs on the left to start a script \
                       \nCheck the terminal on the right for verification and user-input \
                       \nFor more info, check the 'help' tab", font=("Arial", 14))
    readme.pack(pady=10, side="top")

## create notebook tabs ##
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", side='left')

## IO ##
    io = ttk.Frame(root)
    io.pack(expand=True, side='right')

    io_label = ttk.Label(io, text="Terminal")
    io_label.pack(side='top')

    output_text = tk.Text(io, height = 33, width=90, wrap="word", state="disabled")
    output_text.pack(side='top')

    scrollbar = ttk.Scrollbar(io, command=output_text.yview)
    scrollbar.pack(side='right', fill='y')
    output_text['yscrollcommand'] = scrollbar.set

    def update_output(text):
        if text.startswith("SPINNER:"):
            message = text[8:]
            output_text.config(state='normal')
            output_text.delete("end-1l linestart", "end")
            output_text.insert(tk.END, message)
            output_text.config(state='disabled')
        elif text == "SPINNER:CLEAR":
            output_text.config(state="normal")
            output_text.delete("end-1l linestart", "end")
            output_text.config(state='disabled')
        elif text == "CLEAR_ALL":
            output_text.config(state='normal')
            output_text.delete("1.0", tk.END)
            output_text.config(state='disabled')
        # elif text.startswith("sys.argv"):
        #     try:
        #         spinner.stop()
        #     except:
        #         print("subprocess not started")
        #send subprocess output to text widget
        else:
            if spinner and spinner.thread and spinner.thread.is_alive():
                spinner.stop()
            output_text.config(state="normal")
            output_text.insert(tk.END, text)
            output_text.yview_moveto(1)
            output_text.config(state="disabled")


    entry_widget = ttk.Entry(io, width=90)
    entry_widget.pack(pady=10, side="left")
    try:
        def send_command(event=None):
            command = entry_widget.get()
            pm.send_input(command)
            entry_widget.delete(0, tk.END)
    except Exception as e:
        print(e)

    send_button = ttk.Button(io, text="Send", command=send_command)
    send_button.pack(side='right')
    entry_widget.bind("<Return>", send_command)

    def on_close():
        if spinner:
            spinner.stop()
        if pm:
            pm.terminate()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)

## START SCREENS TAB ##
    screens = ttk.Frame(notebook)
    notebook.add(screens, text="Screens")

    ttk.Label(screens, text="Batch Number: ").pack()
    sc_batch = ttk.Entry(screens)
    sc_batch.pack()

    ttk.Label(screens, text="Method: ").pack()
    sc_methods = ["SCRNZ", "SCLCMSMS", "SCGEN"]
    sc_var = tk.StringVar()
    combobox = ttk.Combobox(screens, textvariable=sc_var, values=sc_methods)
    combobox.pack()

    renamer_var = tk.StringVar(value=None)
    renamer_check = ttk.Checkbutton(screens, text="Rename only mode?", onvalue='-r', offvalue=None, variable=renamer_var).pack(pady=5)

    ttk.Button(screens, text="Run Screen Binder", command=lambda: [start_thread(venv_path, script_path_screens, \
                    sc_batch.get(), sc_var.get(), renamer_var.get())]).pack(pady=10)
    
    ttk.Label(screens, text="Requirements: \
              \n-Data must be in BATCH PACK DATA, CASE DATA, or auto-generated CASE DATA subfolders\
              \n-Data that is not in the directories listed above will be ignored by the script \
              \n-Data that is open in Adobe or open in a windows explorer preview window may have issues -- make sure to close them\
              \n \
              \n-If you have reinjects, manually bind them to the appropriate file beforehand and ensure that no duplicate files are present \
              \n-Manually bind your sequence to the batch pack after running. \
              \n ").pack(pady=20)
    


## START QUANTS TAB ##
    quants = ttk.Frame(notebook)
    notebook.add(quants, text="Quants")

    ttk.Label(quants, text="Batch Number: ").pack()
    qt_batch = ttk.Entry(quants)
    qt_batch.pack()

    ttk.Label(quants, text="Method: ").pack()
    qt_methods = ["SQVOL", "QTABUSE", "QTSTIM", "QTPSYCH", "QTBZO1", "QTBZO2", "QTANTIDEP1", "QTANTIHIST", "QTMEPIRIDINE", "QTMETHADONE", "QTACETAMINOPHEN", "QTSALICYLATE", "QTDASH"]
    qt_var = tk.StringVar()
    combobox2 = ttk.Combobox(quants, textvariable=qt_var, values=qt_methods)
    combobox2.pack()

    ttk.Label(quants, text="The 2 boxes below can be left blank", font=('Arial', 12, 'bold')).pack(pady=10)
    ttk.Label(quants, text="Extraction date in MM/DD/YY format WITH slashes: ").pack()
    qt_date = ttk.Entry(quants)
    qt_date.pack()

    ttk.Label(quants, text="Enter your initials: ").pack()
    qt_initials = ttk.Entry(quants)
    qt_initials.pack()

    ttk.Button(quants, text="Run Quants Binder", command=lambda: [start_thread(venv_path, script_path_quants, \
                            qt_batch.get(), qt_var.get().upper(), qt_date.get(), qt_initials.get().upper())]).pack(pady=10)
    
    ttk.Label(quants, text="Requirements: \
              \n-Data must be in BATCH PACK DATA, CASE DATA, or auto-generated CASE DATA subfolders\
              \n-Data that is not in the directories listed above will be ignored by the script \
              \n-Data that is open in Adobe or open in a windows explorer preview window may have issues -- make sure to close them\
              \n \
              \n-If you have MSA's, Excel must be closed on your computer to fill the LF-10/LF-11 forms \
              \n-Make sure your curve and sequence are printed, the script will handle them appropriately. \
              \n-Extraction date and initials can be left empty -- these are for the LJ charts which are not being used currently \
              \n ").pack(pady=20,)

## START SEQUENCE TAB ##
    sequence = ttk.Frame(notebook)
    notebook.add(sequence, text="Sequence")

    ttk.Label(sequence, text="Enter your initials: ").pack()
    initials = ttk.Entry(sequence)
    initials.pack()

    ttk.Button(sequence, text="Run Sequence Generator", command=lambda: [start_thread(venv_path, script_path_sequence, initials.get().upper())]).pack()


    ttk.Label(sequence, text=r""" 
-New feature: CME Test Batches with different Methods is now supported.
    A test batch report for QTABUSE and separate batch report for QTSTIM will be separated into 
    two sequences automatically. 2 test batch reports for SCRNZ will still create only one sequence.

Requirements:
    -This script looks in the directory G:\PDF DATA\TEST BATCH REPORTS for pdf printed Test Batches,
    then prepares a sequence suitable for the instrument/method being prepared
    -You can make extra directories, 'Archive', 'Old batches', etc, without issue -- 
    they are not checked or recognized by the script
                
""").pack(pady=20)
    
    
## START CARRYOVER TAB ##
    carryover = ttk.Frame(notebook)
    notebook.add(carryover, text="Z Carryover")

    ttk.Label(carryover, text="start AMDIS printer: Your files must be processed already").pack()
    ttk.Button(carryover, text="Start AMDIS Printer", command=lambda: [start_thread(venv_path, script_path_Zprint)]).pack()

    ttk.Label(carryover, text="Enter the network path where the raw data is: ").pack()
    location = ttk.Entry(carryover, width=80)
    location.pack()
    ttk.Label(carryover, text="make sure that no other files are in the directory except for the AMDIS reports in order they were printed").pack()

    ttk.Button(carryover, text="Run Carryover Check", command=lambda: [start_thread(venv_path, script_path_carryover, location.get())]).pack()


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
""").pack(pady=20)

## START PDF RENAME TAB ##
    rename = ttk.Frame(notebook)
    notebook.add(rename, text="Rename")

    ttk.Label(rename, text="Enter the full network path where the raw data is: ").pack()
    rename_ent = ttk.Entry(rename, width=80)
    rename_ent.pack()

    ttk.Label(rename, text="Instrument: ").pack()
    rename_methods = ["Shimadzu", "Hans", ]
    rename_var = tk.StringVar()
    combobox3 = ttk.Combobox(rename, textvariable=rename_var, values=rename_methods)
    combobox3.pack()

    ttk.Button(rename, text="Run PDF Rename", command=lambda: [start_thread(venv_path, script_path_rename, rename_ent.get(), rename_var.get())]).pack()



    ttk.Label(rename, text=r"""
              This script will simply check the directory for instrument raw data reports.
              If the format matches a supported type... then the file will be renamed by the sample ID field.
              This tab should only be used if the data you are producing is not part of a routine batch (validation, etc)
              
              To rename files but not bind a routine batch, use the checkbox on the 'screens' tab.
                """).pack()
    
## START HELP TAB ##
    help = ttk.Frame(root)
    notebook.add(help, text="Help")

    help_text = r""" 
What's going on here?

In previous versions of the data manipulation scripts, each one would be a separate executable file.
This new program is GUI (graphical user interface) that serves as a launch-pad for the same data manipulation scripts.
Each of the tabs corresponds to a separate script, and the data entered before you hit "RUN" is passed as a command-line argument, in the same way you were prompted before. 

The program is split into 2 main windows. A "Notebook" which holds all the tabs for different ways we process data, and a "Terminal" which shows the output of the script.
The terminal will remain empty until a script is started. 

This new setup makes it much easier for the maintainer (me) to not only push updates, but also continue to scale it with more and more features. 

"""
    help_box = tk.Text(help, wrap="word", font=("Arial", 13))
    help_box.insert("1.0", help_text)
    help_box.config(state="disabled")
    help_box.pack(padx=10, pady=10)


## TK MAIN LOOP ##
    root.mainloop()

if __name__ == "__main__":
    #logging.info("Application started")
    main()
