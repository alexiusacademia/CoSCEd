import tkinter as tk


class Graph(tk.Frame):
    canvas_width = 640
    canvas_height = 480

    def __init__(self, parent):
        super().__init__(parent)

        self.grid(column=0, row=0)
        self.master.title('Timeline Visual')
        self.center_window()

        lblLeft_controls = tk.Label(self, text="Controls")
        lblLeft_controls.grid(column=0, row=0, sticky='nesw')

        lbl = tk.Label(self, text="Time Frame")
        lbl.grid(column=1, row=0)

        canvas_frame = tk.Frame(self)
        canvas_frame.grid(column=1, row=1)

        self.canvas = tk.Canvas(canvas_frame)
        self.canvas.configure(width=640, height=480)
        self.canvas.grid(column=1, row=1, sticky='nesw')

    def plot_projected(self, projected_list):
        can = self.canvas

        min_y = projected_list[0]['accomp']
        max_y = projected_list[len(projected_list)-1]['accomp']
        diff_y = max_y - min_y

        min_x = projected_list[0]['time']
        max_x = projected_list[len(projected_list)-1]['time']
        diff_x = max_x - min_x

        height_factor = self.canvas_height / diff_y

        width_factor = self.canvas_width / diff_x

        rows = len(projected_list)
        for i in range(rows-1):
            # Draw lines on canavs
            x1 = projected_list[i]['time']
            y1 = projected_list[i]['accomp']
            x2 = projected_list[i + 1]['time']
            y2 = projected_list[i + 1]['accomp']
            can.create_line(x1 * width_factor,
                            self.canvas_height - y1 * height_factor,
                            x2 * width_factor,
                            self.canvas_height - y2 * height_factor,
                            fill="red", activedash=(5, 5))

    def center_window(self):
        w = self.master.winfo_screenwidth()
        h = self.master.winfo_screenheight()

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
