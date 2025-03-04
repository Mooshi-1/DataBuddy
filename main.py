import tkinter as tk
from tkinter import ttk
import subprocess
import os

def run_script(script_name, *args):
    # Path to the virtual environment's Python interpreter
    venv_python = r"G:\PDF DATA\Python\GUI TESTING\.venv\Scripts\python.exe" #UPDATE LATER
    py_path = os.path.join(os.getcwd(), script_name)
    
    try: 
        subprocess.run([venv_python, py_path] + list(args), check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running {script_name}: {e}")
    except FileNotFoundError:
        print(f"Script {script_name} or the Python interpreter could not be found!")

# Set up the main tkinter window
def main():
    root = tk.Tk()
    root.title("Script Launcher")
    root.geometry("400x200")

    # Add a label
    label = ttk.Label(root, text="Select a script to run:", font=("Arial", 14))
    label.pack(pady=10)

    # Add buttons for each script
    ttk.Button(root, text="Run Script 1", command=lambda: run_script("script1.py")).pack(pady=5)
    ttk.Button(root, text="Run Script 2", command=lambda: run_script("script2.py")).pack(pady=5)
    ttk.Button(root, text="Run Script 3", command=lambda: run_script("script3.py")).pack(pady=5)

    # Start the tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
