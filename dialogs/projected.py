import tkinter as tk
from tkinter import messagebox


class ProjectedAccomplishmentDialog:
    top = None
    filename = ''

    def __init__(self, parent):
        self.parent = parent

    def show(self, filename):
        self.filename = filename
        self.init_ui()

    def init_ui(self):
        if self.filename == '':
            messagebox.showinfo("Error", "No file opened.\n"
                                         "A file is necessary to be opened or created to show this editor.")
        else:
            print('Filename:', self.filename)

            self.top = tk.Toplevel(self.parent)
            self.top.title = "Projected Accomplishment Editor"
            self.top.transient(self.parent)
            self.top.grab_set()
