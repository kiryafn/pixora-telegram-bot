import logging
import tkinter as tk
from queue import Queue

class TkinterLogHandler(logging.Handler):
    def __init__(self, log_queue: Queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        msg = self.format(record)
        self.log_queue.put(msg)

class LogWindow:
    def __init__(self, log_queue: Queue):
        self.root = tk.Tk()
        self.root.title("Pixora Logs")
        self.text = tk.Text(self.root, state="disabled", height=30, width=100, bg="black", fg="lime")
        self.text.pack(fill="both", expand=True)
        self.log_queue = log_queue
        self.update_log()

    def update_log(self):
        while not self.log_queue.empty():
            msg = self.log_queue.get_nowait()
            self.text.config(state="normal")
            self.text.insert("end", msg + "\n")
            self.text.config(state="disabled")
            self.text.yview("end")
        self.root.after(1000, self.update_log)

    def run(self):
        self.root.mainloop()