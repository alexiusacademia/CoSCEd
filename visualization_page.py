import tkinter as tk

class Timeline(tk.Frame):
    projected_accomplishment = []
    actual_accomplishment = []
    suspensions = []

    canvas_width = 720
    canvas_height = 480

    canvas_top_margin = 30
    canvas_bottom_margin = 30
    canvas_left_margin = 30
    canvas_right_margin = 30

    def __init__(self, parent):
        super().__init__(parent)
        self.points = []
        self.grid(column=0, row=0)
        self.master.title('Timeline Visual')

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.total_suspension_duration = 0

        canvas_title = tk.Label(self, text="Time Frame")
        canvas_title.grid(column=1, row=0)

        # ===========================================================
        # String Variables
        self.str_cdp_time = tk.StringVar()
        self.str_cdp_accomp = tk.StringVar()
        self.str_summary_total_suspensions = tk.StringVar()
        #===========================================================
        left_panel = tk.Frame(self)
        left_panel.grid(row=0, column=0, rowspan=2, sticky='nesw')

        # Canvas data display
        frame_canvas_data_display = tk.LabelFrame(left_panel, text="Canvas Data")
        frame_canvas_data_display.grid(row=0, column=0, sticky="new", padx=10, pady=5)

        cdp_time_label = tk.Label(frame_canvas_data_display, text="Time").grid(row=0, column=0, sticky="nw")
        cdp_time = tk.Label(frame_canvas_data_display, text='', width=10, anchor='ne', textvariable=self.str_cdp_time).grid(row=0, column=1, sticky="new", padx=10)
        cdp_accomp_label = tk.Label(frame_canvas_data_display, text="Accomplishment").grid(row=1, column=0, sticky='nw')
        cdp_accomp = tk.Label(frame_canvas_data_display, width=10, anchor='ne', textvariable=self.str_cdp_accomp).grid(row=1, column=1, sticky='new', padx=10)

        # Summary
        frame_summary = tk.LabelFrame(left_panel, text='Summary')
        frame_summary.grid(row=1, column=0, sticky='new', padx=10, pady=5)

        summary_total_suspension_label = tk.Label(frame_summary, text='Total Suspension').grid(row=0, column=0)
        summary_total_suspension = tk.Entry(frame_summary, textvariable=self.str_summary_total_suspensions).grid(row=0, column=1, padx=5, pady=5)

        #===========================================================
        # Canvas
        canvas_frame = tk.Frame(self)
        canvas_frame.grid(column=1, row=1)
        self.canvas = tk.Canvas(canvas_frame, cursor='target')
        self.canvas.configure(width=self.canvas_width, height=self.canvas_height, bg="#ffffff")
        self.canvas.grid(column=1, row=1, sticky='nesw')
        #===========================================================

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

            self.total_suspension_duration += duration_suspended

            for j in range(len(self.projected_accomplishment) - 1):

                t1 = self.projected_accomplishment[j]['time']
                accomp1 = self.projected_accomplishment[j]['accomp']
                t2 = self.projected_accomplishment[j+1]['time']
                accomp2 = self.projected_accomplishment[j+1]['accomp']

                temp_projected.append({
                    "time": t1 + total_suspensions,
                    "accomp": accomp1
                })

                if (t1 < start_suspended) and (start_suspended < t2):
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
        self.str_summary_total_suspensions.set(self.total_suspension_duration)

    def hover(self, event):
        point = (event.widget.find_closest(event.x, event.y))[0]
        data = None
        for p in self.points:
            if p['point'] == point:
                data = p
        if data is not None:
            self.str_cdp_time.set(data['time'])
            self.str_cdp_accomp.set(data['accomp'])

    def plot_timeline(self):
        self.recalculate()
        self.display_grid()
        self.plot(self.projected_accomplishment, '#0000ff')
        self.plot(self.actual_accomplishment, '#ff0000')

    def display_grid(self):
        grid_color = '#808080'
        can = self.canvas
        grid_count_vertical = 10
        grid_height = (self.canvas_height - self.canvas_top_margin - self.canvas_bottom_margin) / grid_count_vertical

        w = self.canvas_width

        for i in range(1, grid_count_vertical):
            can.create_line(self.canvas_left_margin,
                            i * grid_height + self.canvas_top_margin,
                            w - self.canvas_right_margin,
                            i * grid_height + self.canvas_top_margin,
                            fill=grid_color,
                            dash=(2, 2))
        can.create_line(self.canvas_left_margin,
                        self.canvas_top_margin,
                        w - self.canvas_right_margin,
                        self.canvas_top_margin,
                        width=2)
        can.create_line(self.canvas_left_margin,
                        self.canvas_height - self.canvas_bottom_margin,
                        w - self.canvas_right_margin,
                        self.canvas_height - self.canvas_bottom_margin,
                        width=2)
        can.create_line(self.canvas_left_margin,
                        self.canvas_top_margin,
                        self.canvas_left_margin,
                        self.canvas_height - self.canvas_bottom_margin,
                        width=2)
        can.create_line(self.canvas_width - self.canvas_right_margin,
                        self.canvas_top_margin,
                        self.canvas_width - self.canvas_right_margin,
                        self.canvas_height - self.canvas_bottom_margin,
                        width=2)

    def plot(self, data, line_fill_color):
        can = self.canvas

        min_y = data[0]['accomp']
        max_y = 100

        diff_y = max_y - min_y

        # Minimum abscissa shall always be the taken from the first time entry of projected
        min_x = data[0]['time']
        # Maximum width shall always be the timeline of projected
        max_x = self.projected_accomplishment[len(self.projected_accomplishment)-1]['time']
        diff_x = max_x - min_x

        height_factor = (self.canvas_height - (self.canvas_top_margin + self.canvas_bottom_margin)) / diff_y

        width_factor = (self.canvas_width - (self.canvas_left_margin + self.canvas_right_margin)) / diff_x

        left_margin = self.canvas_left_margin
        bottom_margin = self.canvas_bottom_margin

        rows = len(data)
        for i in range(rows-1):
            # Draw lines on canavs
            x1 = data[i]['time']
            y1 = data[i]['accomp']
            x2 = data[i + 1]['time']
            y2 = data[i + 1]['accomp']
            can.create_line(x1 * width_factor + left_margin,
                            self.canvas_height - y1 * height_factor - bottom_margin,
                            x2 * width_factor + left_margin,
                            self.canvas_height - y2 * height_factor - bottom_margin,
                            fill=line_fill_color, activedash=(5, 5))
            pt = can.create_rectangle(x1 * width_factor - 2 + left_margin,
                                 self.canvas_height - y1 * height_factor - 2 - bottom_margin,
                                 x1 * width_factor + 2 + left_margin,
                                 self.canvas_height - y1 * height_factor + 2 - bottom_margin,
                                 fill=line_fill_color,
                                 tags='point')
            self.canvas.tag_bind(pt, '<Enter>', self.hover)
            self.points.append({
                "point" : pt,
                "time" : x1,
                "accomp" : y1
            })
        # Plot the last node
        x1 = data[rows-1]['time']
        y1 = data[rows-1]['accomp']
        pt = can.create_rectangle(x1 * width_factor - 2 + left_margin,
                                  self.canvas_height - y1 * height_factor - 2 - bottom_margin,
                                  x1 * width_factor + 2 + left_margin,
                                  self.canvas_height - y1 * height_factor + 2 - bottom_margin,
                                  fill=line_fill_color,
                                  tags='point')
        self.canvas.tag_bind(pt, '<Enter>', self.hover)
        self.points.append({
            "point": pt,
            "time": x1,
            "accomp": y1
        })

    def center_window(self):
        w = self.master.winfo_screenwidth()
        h = self.master.winfo_screenheight()

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
