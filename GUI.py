import tkinter as tk
from tkinter import filedialog
from process import log_to_dict

class LogViewerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.logs = []
        self.current_log_index = 0

        self.title("Log Viewer")
        self.geometry("800x400")

        self.create_widgets()

    def create_widgets(self):
        # Frame for log path and load button
        self.path_frame = tk.Frame(self)
        self.path_frame.pack(side=tk.TOP, fill=tk.X)

        self.file_path_var = tk.StringVar()
        self.file_path_entry = tk.Entry(self.path_frame, textvariable=self.file_path_var, width=115)
        self.file_path_entry.pack(side=tk.LEFT, fill=tk.X, padx=5)

        self.load_button = tk.Button(self.path_frame, text="Load Logs", command=self.load_logs)
        self.load_button.pack(side=tk.LEFT, padx=5)

        # Text widget for displaying full log
        self.log_text = tk.Text(self, wrap=tk.WORD, height=2, width=80)
        self.log_text.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.BOTH, padx=5, pady=5)

        # Label for log
        self.log_label = tk.Label(self, text="Log:", font=("Arial", 12, "bold"))
        self.log_label.pack(side=tk.BOTTOM, anchor=tk.SW, padx=5)

        # Frame for log listbox
        self.log_frame = tk.Frame(self)
        self.log_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.log_listbox = tk.Listbox(self.log_frame, width=80)
        self.log_listbox.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.log_listbox.bind("<<ListboxSelect>>", self.show_log_details)

        # Scrollbar for log listbox
        self.scrollbar = tk.Scrollbar(self.log_frame, orient=tk.VERTICAL, command=self.log_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_listbox.config(yscrollcommand=self.scrollbar.set)

        # Frame for navigation buttons
        self.nav_frame = tk.Frame(self)
        self.nav_frame.pack(side=tk.BOTTOM)

        self.previous_button = tk.Button(self.nav_frame, text="Previous", command=self.show_previous_log)
        self.previous_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(self.nav_frame, text="Next", command=self.show_next_log)
        self.next_button.pack(side=tk.LEFT, padx=5)

        # Label for log info
        self.log_info_label = tk.Label(self, text="Log Info:", font=("Arial", 12, "bold"))
        self.log_info_label.pack(side=tk.TOP, pady=10)

        # Text widget for displaying log info
        self.log_info = tk.Text(self, wrap=tk.WORD, height=15, width=40)
        self.log_info.pack(side=tk.TOP, padx=5)



    def load_logs(self):
        file_path = filedialog.askopenfilename(filetypes=[("Log Files", "*.log")])
        if file_path:
            self.file_path_var.set(file_path)
            with open(file_path, "r") as file:
                self.logs = file.readlines()
                self.display_logs()

    def display_logs(self):
        self.log_listbox.delete(0, tk.END)
        for log in self.logs:
            self.log_listbox.insert(tk.END, log[:80] + "..." if len(log) > 80 else log)
        self.log_listbox.selection_set(self.current_log_index)
        self.show_log_details(None)

    def show_log_details(self, event):
        index = self.log_listbox.curselection()[0]
        self.current_log_index = index
        log = self.logs[index]

        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, log)

        info = log_to_dict(log)
        self.log_info.delete(1.0, tk.END)
        self.log_info.insert(tk.END, f'Date: {info['Month']} {info['Day']}\n')
        self.log_info.insert(tk.END, f'Time: {info['Time']}\n')
        self.log_info.insert(tk.END, f'SSHD: {info['sshd']}\n')
        self.log_info.insert(tk.END, f'IP: {info['ip']}\n')
        self.log_info.insert(tk.END, f'Port: {info['port']}\n')
        self.log_info.insert(tk.END, f'User: {info['user']}\n')
        self.log_info.insert(tk.END, f'Message type: {info['message-type']}\n')

    def show_previous_log(self):
        if self.current_log_index > 0:
            self.current_log_index -= 1
            self.log_listbox.selection_clear(0, tk.END)
            self.log_listbox.selection_set(self.current_log_index)
            self.show_log_details(None)

    def show_next_log(self):
        if self.current_log_index < len(self.logs) - 1:
            self.current_log_index += 1
            self.log_listbox.selection_clear(0, tk.END)
            self.log_listbox.selection_set(self.current_log_index)
            self.show_log_details(None)

if __name__ == "__main__":
    app = LogViewerApp()
    app.mainloop()
