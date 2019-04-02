import tkinter as tk
from tkinter import messagebox
import json
from tkintertable import TableModel, TableCanvas


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
            self.top = tk.Toplevel(self.parent)
            self.top.title = "Projected Accomplishment Editor"
            self.top.transient(self.parent)
            self.top.grab_set()

            # Parse the file
            json_string = ''
            file = open(self.filename, 'r')
            for line in file.readlines():
                json_string += line
            file.close()

            # Convert string to json
            project_json = json.loads(json_string)

            data = {}
            ctr = 0
            for rec in project_json['projected']:
                data[ctr] = rec
                ctr += 1

            self.model = TableModel()
            self.table = TableCanvas(self.top, model=self.model)
            self.model.importDict(data)
            self.table.rowheight = 30
            self.table.show()
            self.table.bind('<FocusIn>', self.enter_pressed)

    def write_data(self, json_data):
        with open(self.filename, 'w') as output_file:
            json.dump(json_data, output_file, indent=4)

    def enter_pressed(self, evt):
        print('Enter pressed!', evt)
        data = self.model.getData()
        print(data)

