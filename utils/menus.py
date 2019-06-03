import tkinter as tk


class ProjectMenu(tk.Menu):
    def __init__(self, master=None):
        tk.Menu.__init__(self, master=None)
        self.master = master

    def init_menus(self):
        pass