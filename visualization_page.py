import tkinter as tk


class Graph(tk.Frame):
    width = 640
    height = 480
    def __init__(self, parent):
        super().__init__(parent)

        self.pack(fill="both", expand=True)
        self.master.title('Timeline Visual')
        self.centerWindow()

        self.canvas = tk.Canvas(self)
        self.canvas.configure(width=640, height=480)
        #self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.grid(column=0, row=1)

        time_frame = tk.Frame(self)
        time_frame.grid(column = 0, row = 0)

        lbl = tk.Label(time_frame, text="Time Frame")
        lbl.pack()

        time_frame_bottom = tk.Frame(self)
        time_frame_bottom.grid(column=0, row=2)

        lbl_bottom = tk.Label(time_frame_bottom, text="Time Frame")
        lbl_bottom.pack()

    def plot_projected(self, projected_list):
        can = self.canvas

        min_y = projected_list[0]['accomp']
        max_y = projected_list[len(projected_list)-1]['accomp']
        diff_y = max_y - min_y

        min_x = projected_list[0]['time']
        max_x = projected_list[len(projected_list)-1]['time']
        diff_x = max_x - min_x

        height_factor = self.height / diff_y

        width_factor = self.width / diff_x

        rows = len(projected_list)
        for i in range(rows-1):
            # Draw lines on canavs
            x1 = projected_list[i]['time']
            y1 = projected_list[i]['accomp']
            x2 = projected_list[i + 1]['time']
            y2 = projected_list[i + 1]['accomp']
            can.create_line(x1 * width_factor,
                            self.height - y1 * height_factor,
                            x2 * width_factor,
                            self.height - y2 * height_factor,
                            fill="red", activedash=(5, 5))

    def centerWindow(self):
        w = self.width
        h = self.height

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))