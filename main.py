import tkinter as tk
import json


class Graph(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.pack(fill="both", expand=True)
        self.master.title('Timeline Visual')
        self.centerWindow()

        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)

    def centerWindow(self):
        w = 640
        h = 480

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))


    def plot_projected(self, projected_list):
        can = self.canvas
        rows = len(projected_list)
        for i in range(rows-1):
            # Draw lines on canavs
            can.create_line(projected_list[i]['time'], projected_list[i]['accomp'],
                            projected_list[i + 1]['time'], projected_list[i + 1]['accomp'],
                            fill="red", activedash=(5, 3))
            print(projected_list[i]['time'])

        can.create_line(0, 0, 640, 0, fill='red')



if __name__ == '__main__':
    root = tk.Tk()
    #root.title("Timeline Visual")
    root.geometry('640x480')

    proj_file = open('timeline.json', 'r')
    proj_file_lines = proj_file.readlines()

    json_string = ''

    for line in proj_file_lines:
        json_string += line

    json_timeline = json.loads(json_string)

    projected = json_timeline['projected']

    canvas = tk.Canvas(root)
    canvas.pack(side='top', fill='both', expand=True)

    #for i in range(len(projected)-1):
    #    canvas.create_line(projected[i]['time'], projected[i]['accomp'],
    #                       projected[i + 1]['time'], projected[i + 1]['accomp'],
    #                        fill="red")
    g = Graph(root)
    g.plot_projected(projected)

    root.mainloop()
