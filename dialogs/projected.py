import tkinter as tk


class ProjectedAccomplishmentDialog:
    top = None

    def __init__(self, parent):
        self.parent = parent

    def show(self):
        self.top = tk.Toplevel(self.parent)
        self.top.title = "Projected Accomplishment Editor"
        self.top.transient(self.parent)
        self.top.grab_set()
