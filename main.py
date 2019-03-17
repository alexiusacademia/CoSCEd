import tkinter as tk
import json

from visualization_page import *

if __name__ == '__main__':
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    # root.geometry('640x480') -> No need to set

    # Retrieve the string from project file
    proj_file = open('timeline.json', 'r')
    proj_file_lines = proj_file.readlines()

    json_string = ''

    for line in proj_file_lines:
        json_string += line

    json_project = json.loads(json_string)

    # Retrieve the projected object timeline
    projected_imeplementation = json_project['projected']

    # Retrieve actual object timeline
    actual_implementation = json_project['actual']

    g = Graph(root)
    g.plot_projected(projected_imeplementation)

    root.mainloop()
