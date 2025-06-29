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
from PIL import Image, ImageTk

import audit
import logging

#things to code:
#figure out how to encode ascii art into terminal

#font / font size overhaul
#button styles with ttk bootstrap
#bootstyle = "success"
#explore other widgets

#SQVOL - anything in CUP -- add blanks
#reinject/reassign tracker + whole batch analysis
# solution for FDLE's, binding/naming

#Z SCREENS - what else do we need?
# C > G > C transfer and folder creation
# AMDIS printer updates, choose which iteration to start the loop on
# fix extra spaces in RI generation

#"help" tab to open training docs like 'how to use sequence generator'
#helpful images to explain the process


version = "3.4" #5-06-25

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
    root.geometry("1300x800")

    pm = None
    spinner = None
    try:
        gif_path = os.path.join(base_dir, 'misc', 'HappyFriday3.gif')
        img = Image.open(gif_path)

        frames = []
        while True:
            #frame = img.copy()
            frame = img.copy().resize((341,161))
            frames.append(ImageTk.PhotoImage(frame))
            img.seek(img.tell()+1)
    except EOFError:
        pass
    except Exception as e:
        print(f'unable to load gif | {e}')

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

    ## HEADER ##

    date = get_weekday()
    if date == 'Friday':
        header = ttk.Label(root)

        ind = 0
        forward = True
        def update():
            nonlocal ind, forward
            header.configure(image=frames[ind])

            if forward:
                ind += 1
                if ind == len(frames) - 1:
                    forward = False
            else:
                ind -= 1
                if ind == 0:
                    forward =True
            root.after(100, update)
        header.grid(row=0, column=0, columnspan=2, pady=10)
        update()
    else:    
        header = ttk.Label(root, text=f"Happy {date}.", font=("Arial", 16, "bold"))
        header.grid(row=0, column=0, columnspan=2, pady=10)


    readme = ttk.Label(root, text="Use the tabs to start a Python script", font=("Arial", 14))
    readme.grid(row=1, column=0, pady=10)

    readme2 = ttk.Label(root, text="Use the terminal for verification and script input", font=("Arial", 14))
    readme2.grid(row=1, column=1, pady=10)

    ## create notebook tabs ##
    notebook = ttk.Notebook(root)
    notebook.grid(row=2, column=0)

    ## IO ##
    io = ttk.Frame(root)
    io.grid(row=2, column=1, padx=5, sticky='nsew')

    io_label = ttk.Label(io, text="Terminal")
    io_label.grid(row=0, column=0, columnspan=2)

    output_text = tk.Text(io, wrap="word", state="disabled")
    output_text.grid(row=1, column=0, sticky="nsew", columnspan=2, rowspan=6, padx=5)

    scrollbar = ttk.Scrollbar(io, command=output_text.yview)
    scrollbar.grid(row=1, column=1, sticky="nse", rowspan=6)
    output_text['yscrollcommand'] = scrollbar.set

    # Configure row and column weights
    root.columnconfigure(0, weight=1, uniform='equal_width')
    root.columnconfigure(1, weight=1, uniform='equal_width')
    io.columnconfigure(0, weight=1, uniform='equal_width')
    io.columnconfigure(1, weight=1, uniform='equal_width')
    io.rowconfigure(0, weight=1, uniform='equal_width')
    io.rowconfigure(1, weight=1, uniform='equal_width')
    io.rowconfigure(2, weight=1, uniform='equal_width')
    io.rowconfigure(3, weight=1, uniform='equal_width')
    io.rowconfigure(4, weight=1, uniform='equal_width')
    io.rowconfigure(5, weight=1, uniform='equal_width')
    io.rowconfigure(6, weight=1, uniform='equal_width')
    io.rowconfigure(7, weight=1, uniform='equal_width')

    def update_output(text):
        stdout_log = "stdout.txt"

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
        else:
            if spinner and spinner.thread and spinner.thread.is_alive():
                spinner.stop()
            try:
                with open(stdout_log, "a") as log_file:
                    log_file.write(text)
            except Exception as e:
                print(f"stdout log-file error | {e}")
            output_text.config(state="normal")
            output_text.insert(tk.END, text)
            output_text.yview_moveto(1)
            output_text.config(state="disabled")

    entry_widget = ttk.Entry(io, width=90)
    entry_widget.grid(row=7, column=0, sticky="ew", columnspan=2, pady=10)

    try:
        def send_command(event=None):
            command = entry_widget.get()
            pm.send_input(command)
            entry_widget.delete(0, tk.END)
    except Exception as e:
        print(e)

    send_button = ttk.Button(io, text="Send", command=send_command)
    send_button.grid(row=7, column=1, pady=10, sticky="e")
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

    screens.columnconfigure(0, weight=1, uniform='equal_width')
    screens.columnconfigure(1, weight=1, uniform='equal_width')

    ttk.Label(screens, text="Batch Number: ").grid(row=0, column=0, sticky='e', pady=10)
    sc_batch = ttk.Entry(screens)
    sc_batch.grid(row=0, column=1, sticky='w')

    ttk.Label(screens, text="Method: ").grid(row=1, column=0, sticky='e', pady=10)
    sc_methods = ["SCRNZ", "SCLCMSMS", "SCGEN"]
    sc_var = tk.StringVar()
    combobox = ttk.Combobox(screens, textvariable=sc_var, values=sc_methods)
    combobox.grid(row=1, column=1, sticky='w')

    renamer_var = tk.StringVar(value=None)
    renamer_check = ttk.Checkbutton(screens, text="Rename only mode?", onvalue='-r', offvalue=None, variable=renamer_var).grid(row=2, column=0, columnspan=2, pady=5)

    ttk.Button(screens, text="Run Screen Binder", command=lambda: [start_thread(venv_path, script_path_screens,
                                                                    sc_batch.get(), sc_var.get(), renamer_var.get())]).grid(row=3, column=0, columnspan=2, pady=10)

    ttk.Label(screens, text="Requirements: \
                                    \n-Data must be in BATCH PACK DATA, CASE DATA, or auto-generated CASE DATA subfolders\
                                    \n-Data that is not in the directories listed above will be ignored by the script \
                                    \n-Data that is open in Adobe or open in a windows explorer preview window may have issues -- make sure to close them\
                                    \n \
                                    \n-If you have reinjects, manually bind them to the appropriate file beforehand and ensure that no duplicate files are present \
                                    \n-Manually bind your sequence to the batch pack after running. \
                                    \n ").grid(row=4, column=0, columnspan=2, pady=20)

    ## START QUANTS TAB ##
    quants = ttk.Frame(notebook)
    notebook.add(quants, text="Quants")

    quants.columnconfigure(0, weight=1, uniform="equal_width")
    quants.columnconfigure(1, weight=1, uniform="equal_width")

    ttk.Label(quants, text="Batch Number: ").grid(row=0, column=0, sticky='e', pady=10)
    qt_batch = ttk.Entry(quants)
    qt_batch.grid(row=0, column=1, sticky='w')

    ttk.Label(quants, text="Method: ").grid(row=1, column=0, sticky='e', pady=10)
    qt_methods = ["SQVOL", "QTABUSE", "QTSTIM", "QTPSYCH", "QTBZO1", "QTBZO2", "QTANTIDEP1", "QTANTIHIST", "QTMEPIRIDINE", "QTMETHADONE", "QTACETAMINOPHEN", "QTSALICYLATE", "QTDASH", "QTTRAZODONE", "TYPE IN ANY SHIMADZU QUANT"]
    qt_var = tk.StringVar()
    combobox2 = ttk.Combobox(quants, textvariable=qt_var, values=qt_methods)
    combobox2.grid(row=1, column=1, sticky='w')

    ttk.Label(quants, text="The 2 boxes below can be left blank", font=('Arial', 12, 'bold')).grid(row=2, column=0, columnspan=2, pady=10)
    ttk.Label(quants, text="Extraction date in MM/DD/YY format WITH slashes: ").grid(row=3, column=0, sticky='e', pady=10)
    qt_date = ttk.Entry(quants)
    qt_date.grid(row=3, column=1, sticky='w')

    ttk.Label(quants, text="Enter your initials: ").grid(row=4, column=0, sticky='e', pady=10)
    qt_initials = ttk.Entry(quants)
    qt_initials.grid(row=4, column=1, sticky='w')

    ttk.Button(quants, text="Run Quants Binder", command=lambda: [start_thread(venv_path, script_path_quants,
                                                                    qt_batch.get(), qt_var.get().upper(), qt_date.get(), qt_initials.get().upper())]).grid(row=5, column=0, columnspan=2, pady=10)

    ttk.Label(quants, text="Requirements: \
                                    \n-Data must be in BATCH PACK DATA, CASE DATA, or auto-generated CASE DATA subfolders\
                                    \n-Data that is not in the directories listed above will be ignored by the script \
                                    \n-Data that is open in Adobe or open in a windows explorer preview window may have issues -- make sure to close them\
                                    \n \
                                    \n-If you have MSA's, Excel must be closed on your computer to fill the LF-10/LF-11 forms \
                                    \n-Make sure your curve and sequence are printed, the script will handle them appropriately. \
                                    \n-Extraction date and initials can be left empty -- these are for the LJ charts which are not being used currently \
                                    \n ").grid(row=6, column=0, columnspan=2, pady=20)

    ## START SEQUENCE TAB ##
    sequence = ttk.Frame(notebook)
    notebook.add(sequence, text="Sequence")

    sequence.columnconfigure(0, weight=1, uniform='equal_width')
    sequence.columnconfigure(1, weight=1, uniform='equal_width')

    ttk.Label(sequence, text="Enter your initials: ").grid(row=0, column=0, pady=10, sticky='e')
    initials = ttk.Entry(sequence)
    initials.grid(row=0, column=1, sticky='w')

    ttk.Button(sequence, text="Run Sequence Generator", command=lambda: [start_thread(venv_path, script_path_sequence, initials.get().upper())]).grid(row=1, column=0, columnspan=2, pady=10)

    ttk.Label(sequence, text=r""" 
    -New feature: CME Test Batches with different Methods is now supported.
        A test batch report for QTABUSE and separate batch report for QTSTIM will be separated into 
        two sequences automatically. 2 test batch reports for SCRNZ will still create only one sequence.

    Requirements:
        -This script looks in the directory G:\PDF DATA\TEST BATCH REPORTS for pdf printed Test Batches,
        then prepares a sequence suitable for the instrument/method being prepared
        -You can make extra directories, 'Archive', 'Old batches', etc, without issue -- 
        they are not checked or recognized by the script
                        
    """).grid(row=2, column=0, columnspan=2, pady=20)

    ## START CARRYOVER TAB ##
    carryover = ttk.Frame(notebook)
    notebook.add(carryover, text="Z Carryover")

    carryover.columnconfigure(0, weight=1, uniform='equal_width')
    carryover.columnconfigure(1, weight=1, uniform='equal_width')

    ttk.Label(carryover, text="start AMDIS printer: Your files must be processed already").grid(row=0, column=0, columnspan=2, pady=10)
    ttk.Button(carryover, text="Start AMDIS Printer", command=lambda: [start_thread(venv_path, script_path_Zprint)]).grid(row=1, column=0, columnspan=2, pady=10)

    ttk.Label(carryover, text="Enter the network path where the raw data is: ").grid(row=2, sticky='e', column=0)
    location = ttk.Entry(carryover, width=80)
    location.grid(row=2, column=1, sticky='w')
    ttk.Label(carryover, text="make sure that no other files are in the directory except for the AMDIS reports in order they were printed").grid(row=3, column=0, columnspan=2)

    ttk.Button(carryover, text="Run Carryover Check", command=lambda: [start_thread(venv_path, script_path_carryover, location.get())]).grid(row=4, column=0, columnspan=2)

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
    """).grid(row=5, column=0, columnspan=2, pady=20)

    ## START PDF RENAME TAB ##
    rename = ttk.Frame(notebook)
    notebook.add(rename, text="Rename")

    rename.columnconfigure(0, weight=1, uniform='equal_width')
    rename.columnconfigure(1, weight=1, uniform='equal_width')

    ttk.Label(rename, text="Enter the full network path where the raw data is: ").grid(row=0, column=0, pady=10, sticky='e')
    rename_ent = ttk.Entry(rename)
    rename_ent.grid(row=0, column=1, sticky='w')

    ttk.Label(rename, text="Instrument: ").grid(row=1, column=0, pady=20, sticky='e')
    rename_methods = ["Shimadzu", "Hans", ]
    rename_var = tk.StringVar()
    combobox3 = ttk.Combobox(rename, textvariable=rename_var, values=rename_methods)
    combobox3.grid(row=1, column=1, sticky='w')

    ttk.Button(rename, text="Run PDF Rename", command=lambda: [start_thread(venv_path, script_path_rename, rename_ent.get(), rename_var.get())]).grid(row=2, column=0, columnspan=2)

    ttk.Label(rename, text=r"""
                    This script will simply check the directory for instrument raw data reports.
                    If the format matches a supported type... then the file will be renamed by the sample ID field.
                    This tab should only be used if the data you are producing is not part of a routine batch (validation, etc)
                    
                    To rename files but not bind a routine batch, use the checkbox on the 'screens' tab.
                        """).grid(row=3, column=0, columnspan=2)

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
    help_box.grid(sticky='nsew')

    help.columnconfigure(0, weight=1)
    help.rowconfigure(0, weight=1)
## TK MAIN LOOP ##
    root.mainloop()

if __name__ == "__main__":
    #logging.info("Application started")
    main()
