import json

from visualization_page import *

if __name__ == '__main__':
    root = tk.Tk()

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

    # Retrieve suspensions
    suspensions = json_project['suspensions']

    timeline = Timeline(root)
    # timeline.projected_accomplishment = projected_imeplementation
    # timeline.actual_accomplishment = actual_implementation
    # timeline.suspensions = suspensions
    # timeline.plot_timeline()

    root.mainloop()
