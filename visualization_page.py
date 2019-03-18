import tkinter as tk


class Timeline(tk.Frame):
    projected_accomplishment = []
    actual_accomplishment = []
    suspensions = []

    canvas_width = 640
    canvas_height = 480

    def __init__(self, parent):
        super().__init__(parent)

        self.grid(column=0, row=0)
        self.master.title('Timeline Visual')

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        lblLeft_controls = tk.Label(self, text="Controls")
        lblLeft_controls.configure(bg="#ff0000")
        lblLeft_controls.grid(column=0, row=0, sticky='nesw')

        lbl = tk.Label(self, text="Time Frame")
        lbl.grid(column=1, row=0)

        canvas_frame = tk.Frame(self)
        canvas_frame.grid(column=1, row=1)

        self.canvas = tk.Canvas(canvas_frame)
        self.canvas.configure(width=640, height=480, bg="#ffffff")

        self.canvas.grid(column=1, row=1, sticky='nesw')

    def recalculate(self):
        """
        Recalculates the graph for projected and actual timeline to be plotted
        by incorporating all the suspensions.
        """

        # Breaks the projected based on suspensions
        for i in range(len(self.suspensions)):
            # Temporary holder for the projected timeline
            temp_projected = []

            # Total number of days the project is suspended
            total_suspensions = 0

            start_suspended = self.suspensions[i]['start']
            duration_suspended = self.suspensions[i]['duration']

            for j in range(len(self.projected_accomplishment) - 1):

                t1 = self.projected_accomplishment[j]['time']
                accomp1 = self.projected_accomplishment[j]['accomp']
                t2 = self.projected_accomplishment[j+1]['time']
                accomp2 = self.projected_accomplishment[j+1]['accomp']

                temp_projected.append({
                    "time": t1 + total_suspensions,
                    "accomp": accomp1
                })

                if (t1 < start_suspended and start_suspended < t2):
                    total_suspensions += duration_suspended

                    # Now, calculate the corresponding accomplishment
                    accomp = (accomp2 - accomp1) / (t2 - t1) * (start_suspended - t1) + accomp1

                    # Append to new list
                    temp_projected.append({
                        "time": start_suspended,
                        "accomp": accomp     # To be calculated by interpolation
                    })
                    temp_projected.append({
                        "time": start_suspended + duration_suspended,
                        "accomp": accomp
                    })

            # Add the last node
            temp_projected.append({
                "time": self.projected_accomplishment[len(self.projected_accomplishment)-1]['time'] + total_suspensions,
                "accomp": 100
            })

            self.projected_accomplishment = temp_projected

    def plot_timeline(self):
        self.recalculate()
        self.plot_projected()

    def plot_projected(self):
        can = self.canvas

        min_y = self.projected_accomplishment[0]['accomp']
        max_y = self.projected_accomplishment[len(self.projected_accomplishment)-1]['accomp']
        diff_y = max_y - min_y

        min_x = self.projected_accomplishment[0]['time']
        max_x = self.projected_accomplishment[len(self.projected_accomplishment)-1]['time']
        diff_x = max_x - min_x

        height_factor = self.canvas_height / diff_y

        width_factor = self.canvas_width / diff_x

        rows = len(self.projected_accomplishment)
        for i in range(rows-1):
            # Draw lines on canavs
            x1 = self.projected_accomplishment[i]['time']
            y1 = self.projected_accomplishment[i]['accomp']
            x2 = self.projected_accomplishment[i + 1]['time']
            y2 = self.projected_accomplishment[i + 1]['accomp']
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
