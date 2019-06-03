import tkinter as tk


class ProjectMenu(tk.Menu):
    def __init__(self, master, parent):
        tk.Menu.__init__(self, master=master)
        self.master = master
        self.parent = parent
        self.init_menus()

    def init_menus(self):
        menu_save = tk.Menu(self, tearoff=0)
        menu_save.add_command(label='Export S-Curve as Image (JPEG)', command=self.parent.export_image_as_jpeg)

        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label='New', command=self.parent.new_project)
        file_menu.add_command(label='Open Project' , command=self.parent.open_project)
        file_menu.add_cascade(label='Export', menu=menu_save)
        file_menu.add_separator()
        file_menu.add_command(label='Quit') # , command=self.close_main_window)

        self.add_cascade(label='File', menu=file_menu)
