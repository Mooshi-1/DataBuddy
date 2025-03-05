import tkinter as tk
from tkinter import ttk
from queue import Queue
import threading
import subprocess


def run_script_with_input(queue, venv_path, script_path, *args):
    """Run a script in a subprocess and handle its IO."""
    try:
        process = subprocess.Popen(
            [venv_path, script_path] + list(args),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Continuously read output and pass it to the queue
        while True:
            output = process.stdout.readline()
            if output:
                queue.put(output.strip())  # Send output to the queue
            if process.poll() is not None:
                break

        # Capture final output or errors
        stderr = process.stderr.read().strip()
        if stderr:
            queue.put(f"Error: {stderr}")
        queue.put("DONE")
    except FileNotFoundError:
        queue.put("Script or Python interpreter could not be found!")
    except Exception as e:
        queue.put(f"Unexpected error: {e}")


def send_input_to_process(process, input_text):
    """Send user input to the subprocess."""
    if process and process.stdin:
        process.stdin.write(input_text + "\n")
        process.stdin.flush()


def start_thread_with_input(queue, progress_bar, status_label, input_box, venv_path, script_path, *args):
    """Start the script in a thread and enable user input."""
    status_label.config(text="Running script...", foreground="blue")
    thread = threading.Thread(target=run_script_with_input, args=(queue, venv_path, script_path, *args))
    thread.start()
    check_queue_with_input(queue, progress_bar, status_label, input_box)


def check_queue_with_input(queue, progress_bar, status_label, input_box):
    """Check the queue for updates from the subprocess and handle input."""
    try:
        while not queue.empty():
            message = queue.get_nowait()
            if message == "DONE":
                progress_bar.stop()
                status_label.config(text="Script completed!", foreground="green")
                input_box.config(state="disabled")  # Disable input when script finishes
            else:
                status_label.config(text=message, foreground="blue")
    except Exception as e:
        status_label.config(text=f"Error: {e}", foreground="red")
    finally:
        # Schedule the next queue check
        if progress_bar["value"] < 100:  # Prevent indefinite queue checks
            progress_bar.after(100, check_queue_with_input, queue, progress_bar, status_label, input_box)


def main():
    root = tk.Tk()
    root.title("Interactive Script Runner")
    root.geometry("800x600")

    queue = Queue()

    # Status Label
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

    # Run Button
    run_button = ttk.Button(
        root,
        text="Run Script",
        command=lambda: start_thread_with_input(
            queue, progress_bar, status_label, input_box, "python", "path_to_script.py"
        ),
    )
    run_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()


    