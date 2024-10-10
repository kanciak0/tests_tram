import tkinter as tk
from datetime import datetime
from tkinter import messagebox
import subprocess
import os
import glob
import time

class TestRunnerGUI:
    def __init__(self, root, test_directory, config_file):
        self.root = root
        self.root.title("Pytest Runner")
        self.test_directory = test_directory
        self.config_file = config_file

        # List of test files
        self.test_files = []

        # Frame for test selection
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.test_listbox = tk.Listbox(self.frame, selectmode=tk.MULTIPLE)
        self.test_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.load_tests_button = tk.Button(self.frame, text="Load Tests", command=self.load_tests)
        self.load_tests_button.pack(side=tk.RIGHT)

        # Label for config file path
        self.config_file_label = tk.Label(self.root, text="Config File: " + os.path.basename(self.config_file))
        self.config_file_label.pack(pady=5)

        self.run_tests_button = tk.Button(self.root, text="Run Selected Tests", command=self.run_selected_tests)
        self.run_tests_button.pack(pady=20)

        self.run_all_button = tk.Button(self.root, text="Run All Tests", command=self.run_all_tests)
        self.run_all_button.pack(pady=20)

        # Text area for displaying results
        self.result_text = tk.Text(self.root, height=15, width=80)
        self.result_text.pack(pady=10)
        self.result_text.insert(tk.END, "Test results will be displayed here...\n")
        self.result_text.config(state=tk.DISABLED)  # Make it read-only initially

        # Automatically load tests from the predefined directory
        self.load_tests()
        self.log_start_time = None
        # Start the log output monitoring
        self.log_file_path = os.path.join("logs", "serial_log_COM1.txt")  # Path to your log file
        self.log_start_time = None  # To store when tests were started
        self.monitor_log()

    def load_tests(self):
        """Load test files from the predefined test directory."""
        self.test_files.clear()  # Clear previous entries
        for subdir in ['n27', 'n717']:
            path = os.path.join(self.test_directory, subdir)
            print(f"Checking path: {path}")  # Debug print statement
            if os.path.exists(path):
                found_files = glob.glob(os.path.join(path, '*.py'))  # Adjust the pattern as needed
                print(f"Found files: {found_files}")  # Debug print statement
                self.test_files.extend(found_files)  # Add found files to the list
        self.update_test_list()

    def update_test_list(self):
        self.test_listbox.delete(0, tk.END)
        for test_file in self.test_files:
            self.test_listbox.insert(tk.END, os.path.basename(test_file))

    def run_selected_tests(self):
        selected_indices = self.test_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No selection", "Please select at least one test.")
            return

        selected_files = [self.test_files[i] for i in selected_indices]
        self.run_tests(selected_files)

    def run_all_tests(self):
        if not self.test_files:
            messagebox.showwarning("No tests loaded", "Please load test files first.")
            return

        self.run_tests(self.test_files)

    def run_tests(self, test_files):
        if not os.path.isfile(self.config_file):
            messagebox.showwarning("Invalid Config File", "The config file does not exist.")
            return

        # Set the log start time to the current time when tests are run
        self.log_start_time = datetime.now()

        # Prepare the pytest command with the config file
        command = ['pytest', '--serial-config', self.config_file, '--tb=short', '--log-cli-level=DEBUG', '--log-file=pytest_output_1.log']
        command.extend(test_files)

        subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k'] + command)

    def monitor_log(self):
        """Monitor the log file for new output."""
        if os.path.isfile(self.log_file_path):
            with open(self.log_file_path, 'r') as log_file:
                # Read the entire log contents
                log_contents = log_file.readlines()

                # Filter logs for entries after the test start time
                filtered_logs = self.filter_logs_after_time(log_contents)
                self.update_log_display(filtered_logs)

        # Schedule the next check
        self.root.after(2000, self.monitor_log)  # Check every 2 seconds

    def filter_logs_after_time(self, log_contents):
        """Filter logs to show only entries after the start time."""
        filtered_logs = []
        for log in log_contents:
            # Split the log entry into timestamp and message
            try:
                log_time_str, log_message = log.split(' - ', 1)
                log_time = datetime.strptime(log_time_str, "%Y-%m-%d %H:%M:%S.%f")
                # Check if the log time is after the recorded start time
                if self.log_start_time and log_time >= self.log_start_time:
                    filtered_logs.append(log)
            except ValueError:
                # Handle logs that do not match the expected format
                continue
        return filtered_logs

    def update_log_display(self, log_contents):
        """Update the text area with the latest log contents."""
        self.result_text.config(state=tk.NORMAL)  # Make the text area editable to insert text
        self.result_text.delete('1.0', tk.END)  # Clear previous contents
        self.result_text.insert(tk.END, "Test results will be displayed here...\n")
        self.result_text.insert(tk.END, "".join(log_contents))  # Append new log content

        # Scroll to the end of the text area
        self.result_text.see(tk.END)  # Scroll to the end
        self.result_text.config(state=tk.DISABLED)  # Make it read-only again

if __name__ == "__main__":
    # Set the relative path for the test directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up two levels to get to tests_tram
    test_directory = os.path.join(project_root, "tests")  # Now point to the 'tests' directory

    # Set the fixed path for the config file
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config_file.txt')  # Fixed path to config_file.txt in common

    root = tk.Tk()
    app = TestRunnerGUI(root, test_directory, config_file)
    root.mainloop()
