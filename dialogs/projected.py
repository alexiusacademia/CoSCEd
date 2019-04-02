import tkinter as tk


class ProjectedAccomplishmentDialog:
    def __init__(self, parent):
        self.parent = parent

    def show(self):
        top = self.top = tk.Toplevel(self.parent)
