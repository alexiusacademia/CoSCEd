import tkinter as tk
from tkinter import messagebox
import json


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

            project_json['projected'].append({
                'time': 30,
                'accomp': 25
            })

            # Convert the json object to python object
            with open(self.filename, 'w') as output_file:
                json.dump(project_json, output_file, indent=4)
