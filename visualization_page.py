import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox, ttk
from datetime import date
import datetime
import json
import subprocess

import dialogs.projected as projected_dialog
import dialogs.actual as actual_dialog
import dialogs.suspensions as suspensions_dialog
import utils.convert_to_num as converter


class Timeline(tk.Frame):
    projected_accomplishment = []
    actual_accomplishment = []
    suspensions = []

    canvas_width = 720
    canvas_height = 480

    canvas_top_margin = 30
    canvas_bottom_margin = 30
    canvas_left_margin = 40
    canvas_right_margin = 30

    width_factor = 1

    LINE_COLOR_PROJECTED = '#0000ff'
    LINE_COLOR_ACTUAL = '#ff0000'

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.points = []
        self.grid(column=0, row=0)
        self.master.title('Project Timeline Editor')

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.total_suspension_duration = 0
        self.slippage = 0

        self.project_opened = False

        self.actual_accomp = 0

        self.project_filename = ''

        # ===========================================================
        # String Variables
        self.str_cdp_time = tk.StringVar()
        self.str_cdp_accomp = tk.StringVar()
        self.str_cdp_actual_accomp = tk.StringVar()
        self.str_cdp_slippage = tk.StringVar()
        self.str_cdp_date = tk.StringVar()
        self.str_summary_total_suspended = tk.StringVar()
        self.str_summary_total_suspension_order = tk.StringVar()
        self.str_summ_orig_completion_days = tk.StringVar()
        self.str_summ_rev_completion_days = tk.StringVar()
        self.str_summ_rev_completion_date = tk.StringVar()
        self.str_start_date = tk.StringVar()
        self.str_vert_grid_interval = tk.StringVar()
        self.str_status_message = tk.StringVar()

        self.init_ui()

    def init_ui(self):
        """
        Creation of the user interface elements.
        """
        # ===========================================================
        # Menus
        menu_bar = tk.Menu(self.parent)

        menu_save = tk.Menu(menu_bar, tearoff=0)
        menu_save.add_command(label='Save S-Curve', command=self.save_scurve)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='New', command=self.new_project)
        file_menu.add_command(label='Open Project', command=self.open_project)
        file_menu.add_cascade(label='Save', menu=menu_save)
        file_menu.add_separator()
        file_menu.add_command(label='Quit', command=self.parent.quit)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label='Projected Accomplishment', command=self.edit_projected)
        edit_menu.add_command(label='Actual Accomplishment', command=self.edit_actual)
        edit_menu.add_command(label='Suspensions', command=self.edit_suspensions)

        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        self.parent.config(menu=menu_bar)

        canvas_title = tk.Label(self, text="Time Frame")
        canvas_title.grid(column=1, row=0)
        # ===========================================================
        # Left panel for displaying of textual data.
        left_panel = tk.Frame(self)
        left_panel.grid(row=0, column=0, rowspan=2, sticky='nesw')

        # Canvas data display
        frame_canvas_data_display = tk.LabelFrame(left_panel, text="Canvas Data")
        frame_canvas_data_display.grid(row=0, column=0, sticky="new", padx=10, pady=5)
        frame_canvas_data_display.grid_columnconfigure(1, weight=1)

        cdp_time_label = tk.Label(frame_canvas_data_display, text="Time").grid(row=0, column=0, sticky="nw")
        cdp_time = tk.Label(frame_canvas_data_display, text='', width=10, anchor='ne',
                            relief='sunken', textvariable=self.str_cdp_time) \
            .grid(row=0, column=1, sticky="nesw", padx=5, pady=5)
        cdp_accomp_label = tk.Label(frame_canvas_data_display, text="Projected Accomplishment").grid(row=1, column=0, sticky='nw')
        cdp_accomp = tk.Label(frame_canvas_data_display, width=10, anchor='ne',
                              relief='sunken', textvariable=self.str_cdp_accomp) \
            .grid(row=1, column=1, sticky='nesw', padx=5, pady=5)
        cdp_actual_accomp_label = tk.Label(frame_canvas_data_display, text="Actual Accomplishment")\
            .grid(row=2, column=0, sticky='nw')
        cdp_accomp = tk.Label(frame_canvas_data_display, width=10, anchor='ne',
                              relief='sunken', textvariable=self.str_cdp_actual_accomp) \
            .grid(row=2, column=1, sticky='nesw', padx=5, pady=5)
        cdp_slippage_label = tk.Label(frame_canvas_data_display, text='Slippage').grid(row=3, column=0, sticky="nw")
        cdp_slippage = tk.Label(frame_canvas_data_display, width=10, anchor='ne',
                                relief='sunken', textvariable=self.str_cdp_slippage) \
            .grid(row=3, column=1, sticky='nesw', padx=5, pady=5)
        cdp_date_label = tk.Label(frame_canvas_data_display, text='Date').grid(row=4, column=0, sticky="nw")
        cdp_date = tk.Label(frame_canvas_data_display, width=10, anchor='ne',
                            relief='sunken', textvariable=self.str_cdp_date) \
            .grid(row=4, column=1, sticky='nesw', padx=5, pady=5)

        # Summary
        frame_summary = tk.LabelFrame(left_panel, text='Summary')
        frame_summary.grid(row=1, column=0, sticky='new', padx=10, pady=5)
        frame_summary.grid_columnconfigure(1, weight=1)

        summ_total_susp_days_label = tk.Label(frame_summary, text='Total Suspended Days') \
            .grid(row=0, column=0, sticky='nw')
        summ_total_susp = tk.Label(frame_summary, width=10, anchor='ne',
                                   relief='sunken', textvariable=self.str_summary_total_suspended) \
            .grid(row=0, column=1, padx=5, pady=5, sticky='nes')

        summ_total_susp_order_label = tk.Label(frame_summary, text='Total Suspension Orders') \
            .grid(row=1, column=0, sticky='nw')
        summ_total_susp_order = tk.Label(frame_summary, width=10, anchor='ne', relief='sunken',
                                         textvariable=self.str_summary_total_suspension_order) \
            .grid(row=1, column=1, padx=5, pady=5, sticky='nes')
        summ_orig_completion_days_label = tk.Label(frame_summary, text='Original Completion Days') \
            .grid(row=2, column=0, sticky='nw')
        summ_orig_completion_days = tk.Label(frame_summary, width=10, anchor='ne', relief='sunken',
                                             textvariable=self.str_summ_orig_completion_days) \
            .grid(row=2, column=1, padx=5, pady=5, sticky='nes')
        summ_rev_completion_days_label = tk.Label(frame_summary, text='Revised Completion Days') \
            .grid(row=3, column=0, sticky='nw')
        summ_rev_completion_days = tk.Label(frame_summary, width=10, anchor='ne', relief='sunken',
                                            textvariable=self.str_summ_rev_completion_days) \
            .grid(row=3, column=1, padx=5, pady=5, sticky='nes')
        summ_rev_completion_date_label = tk.Label(frame_summary, text='Revised Completion Date') \
            .grid(row=4, column=0, sticky='nw')
        summ_rev_completion_date = tk.Label(frame_summary, width=20, anchor='ne', relief='sunken',
                                            textvariable=self.str_summ_rev_completion_date) \
            .grid(row=4, column=1, padx=5, pady=5, sticky='nes')

        frame_inputs = tk.LabelFrame(left_panel, text='Inputs')
        frame_inputs.grid(row=2, column=0, sticky='nesw', padx=10, pady=5)
        frame_inputs.grid_columnconfigure(1, weight=1)

        inputs_start_date_label = tk.Label(frame_inputs, text='Start Date') \
            .grid(row=0, column=0, sticky='nsw')
        inputs_start_date = tk.Entry(frame_inputs, textvariable=self.str_start_date, justify='right') \
            .grid(row=0, column=1, sticky='nesw', padx=5, pady=5)
        inputs_vert_grid_interval_label = tk.Label(frame_inputs, text='Vertical Grid Interval') \
            .grid(row=1, column=0, sticky='nsw')
        self.inputs_vert_grid_interval = ttk.Combobox(frame_inputs, values=['Decadal', '30 Day Period', 'None'],
                                                      justify='right', textvariable=self.str_vert_grid_interval, state='disabled')
        self.inputs_vert_grid_interval.grid(row=1, column=1, sticky='nesw', padx=5, pady=5)
        self.inputs_vert_grid_interval.bind('<<ComboboxSelected>>', self.cbo_vert_grid_selected)

        self.inputs_calculate_btn = tk.Button(frame_inputs, text='Calculate', command=self.calculate_btn_pressed, state='disabled')
        self.inputs_calculate_btn.grid(row=100, column=1, sticky='nes', padx=5, pady=5)

        # ==========================================================
        # Canvas
        # canvas_frame = tk.Frame(self)
        # canvas_frame.grid(column=1, row=1)
        self.canvas = tk.Canvas(self, cursor='cross')
        self.canvas.configure(width=self.canvas_width, height=self.canvas_height, bg="#ffffff")
        self.canvas.grid(column=1, row=1, sticky='nesw')
        self.canvas.bind('<Motion>', self.canvas_hover)
        # ==========================================================
        # Status bar
        frame_status_bar = tk.Frame(self, bd=1, relief='sunken')
        frame_status_bar.grid(row=100, column=0, columnspan=2, sticky='nesw', padx=10, pady=10)

        status_message_label = tk.Label(frame_status_bar, text='Status: ', anchor='nw', justify='left')\
            .grid(row=0, column=0, sticky='nesw')
        status_message = tk.Label(frame_status_bar, textvariable=self.str_status_message,
                                  anchor='nw', justify = 'left')\
            .grid(row=0, column=1)

    def recalculate(self):
        """
        Recalculates the graph for projected and actual timeline to be plotted
        by incorporating all the suspensions.
        """
        # Check for the total number of suspension orders
        if len(self.suspensions) == 1:
            if self.suspensions[0]['duration'] == 0:
                self.str_summary_total_suspension_order.set(0)
            else:
                self.str_summary_total_suspension_order.set(len(self.suspensions))
        else:
            self.str_summary_total_suspension_order.set(len(self.suspensions))

        self.str_summ_orig_completion_days \
            .set(self.projected_accomplishment[len(self.projected_accomplishment) - 1]['time'])

        temp_projected = []
        self.total_suspension_duration = 0
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
                t2 = self.projected_accomplishment[j + 1]['time']
                accomp2 = self.projected_accomplishment[j + 1]['accomp']

                temp_projected.append({
                    "time": t1 + total_suspensions,
                    "accomp": accomp1
                })

                if (t1 < start_suspended) and (start_suspended <= t2):
                    total_suspensions += duration_suspended

                    # Now, calculate the corresponding accomplishment
                    accomp = (accomp2 - accomp1) / (t2 - t1) * (start_suspended - t1) + accomp1

                    # Append to new list
                    temp_projected.append({
                        "time": start_suspended,
                        "accomp": accomp  # To be calculated by interpolation
                    })
                    temp_projected.append({
                        "time": start_suspended + duration_suspended,
                        "accomp": accomp
                    })

            # Add the last node
            temp_projected.append({
                "time": self.projected_accomplishment[len(self.projected_accomplishment) - 1][
                            'time'] + total_suspensions,
                "accomp": 100
            })

            self.projected_accomplishment = temp_projected
        self.str_summary_total_suspended.set(self.total_suspension_duration)
        # Total number of days to complete

        total_days = int(self.str_summ_orig_completion_days.get())
        if temp_projected is not None and (len(temp_projected) > 0):
            total_days = temp_projected[len(temp_projected) - 1]['time']
        self.str_summ_rev_completion_days.set(total_days)

    def plot_timeline(self):
        """
        Plot everything.
        """
        self.recalculate()
        self.display_grid()
        self.plot(self.projected_accomplishment, self.LINE_COLOR_PROJECTED)
        self.plot(self.actual_accomplishment, self.LINE_COLOR_ACTUAL)

    def display_grid(self):
        """
        Displays the grid lines of the graph.
        """
        grid_color = '#808080'
        can = self.canvas
        grid_count_vertical = 10
        grid_height = (self.canvas_height - self.canvas_top_margin - self.canvas_bottom_margin) / grid_count_vertical

        w = self.canvas_width

        # Display the horizontaal grid lines
        for i in range(1, grid_count_vertical):
            can.create_line(self.canvas_left_margin,
                            i * grid_height + self.canvas_top_margin,
                            w - self.canvas_right_margin,
                            i * grid_height + self.canvas_top_margin,
                            fill=grid_color,
                            dash=(2, 2), width=0.01)
            can.create_text(10, self.canvas_height - (i + 1) * grid_height, text=i * 10, anchor='nw', offset='15, 0')
        can.create_text(10, self.canvas_height - (grid_count_vertical + 1) * grid_height, text=100, anchor='nw',
                        offset='5, 0')

        # Display borders
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

        can.create_text(self.canvas_width - self.canvas_right_margin + 10,
                        self.canvas_height/2,
                        text='Accomplishment (%)',
                        angle=90)

        can.create_text(self.canvas_width/2,
                        self.canvas_height - self.canvas_bottom_margin + 10,
                        text='Time')

        self.display_legend()

    def display_legend(self):
        can = self.canvas
        # Display Legends
        can.create_line(self.canvas_left_margin + 10,
                        self.canvas_top_margin + 30,
                        self.canvas_left_margin + 100,
                        self.canvas_top_margin + 30,
                        fill=self.LINE_COLOR_PROJECTED,
                        tags=['legend'])

        can.create_text(self.canvas_left_margin + 110,
                        self.canvas_top_margin + 30,
                        text='Projected', anchor='w', fill=self.LINE_COLOR_PROJECTED,
                        tags=['legend'])

        can.create_line(self.canvas_left_margin + 10,
                        self.canvas_top_margin + 60,
                        self.canvas_left_margin + 100,
                        self.canvas_top_margin + 60,
                        fill=self.LINE_COLOR_ACTUAL,
                        tags=['legend'])

        can.create_text(self.canvas_left_margin + 110,
                        self.canvas_top_margin + 60,
                        text='Actual', anchor='w', fill=self.LINE_COLOR_ACTUAL,
                        tags=['legend'])

    def plot(self, data, line_fill_color):
        """
        Plot a given data, either the projected or actual accomplishment.
        :param data: The data to be plotted (e.g. projected accomplishment).
        :param line_fill_color: The desired color for the line segments.
        """
        can = self.canvas

        min_y = data[0]['accomp']
        max_y = 100

        diff_y = max_y - min_y

        # Minimum abscissa shall always be the taken from the first time entry of projected
        min_x = data[0]['time']
        # Maximum width shall always be the timeline of projected
        max_x = self.projected_accomplishment[len(self.projected_accomplishment) - 1]['time']
        diff_x = max_x - min_x

        if diff_x == 0:
            return

        height_factor = (self.canvas_height - (self.canvas_top_margin + self.canvas_bottom_margin)) / diff_y

        width_factor = (self.canvas_width - (self.canvas_left_margin + self.canvas_right_margin)) / diff_x
        self.width_factor = width_factor

        left_margin = self.canvas_left_margin
        bottom_margin = self.canvas_bottom_margin

        rows = len(data)
        for i in range(rows - 1):
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
                "point": pt,
                "time": x1,
                "accomp": y1
            })
        # Plot the last node
        x1 = data[rows - 1]['time']
        y1 = data[rows - 1]['accomp']
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

    def calculate_slippage(self, time):
        """
        Calculates the slippage (positive or negative) at a given point
        in time.
        :param time: The number of days elapsed from the start of the project.
        """
        actual = self.get_accomplishment_at(time, self.actual_accomplishment)
        projected = self.get_accomplishment_at(time, self.projected_accomplishment)

        if (actual is None) or (projected is None):
            return 0

        # Check if actual time elapsed reached the given time
        if self.actual_accomplishment[len(self.actual_accomplishment)-1]['time'] < time:
            self.slippage = 0
        else:
            self.slippage = round((actual - projected), 2)
        return self.slippage

    def get_accomplishment_at(self, time, accomplishment_list):
        # Calculates accomplishment by interpolation
        for i in range(len(accomplishment_list) - 1):
            t1 = accomplishment_list[i]['time']
            a1 = accomplishment_list[i]['accomp']
            t2 = accomplishment_list[i + 1]['time']
            a2 = accomplishment_list[i + 1]['accomp']
            if (time >= t1) and (time <= t2):
                if time == t1:
                    return a1
                elif time == t2:
                    return a2
                else:
                    return (time - t1) / (t2 - t1) * (a2 - a1) + a1

    def valid_start_date(self):
        """
        Check if the supplied format for the start date is valid
        :return: bool. True if the format is valid.
        """
        str_start_date = self.str_start_date.get()
        if '/' in str_start_date and (str_start_date.count('/') == 2):
            _date = str_start_date.split('/')
            _date = date(int(_date[2]), int(_date[0]), int(_date[1]))

            # Check if the type is correct
            if type(_date) is datetime.date:
                return True

        return False

    def get_new_date(self, start, duration):
        """
        Calculates the future date by adding number of days from
        a given start date.
        :param start: Start Date (valid string mm/dd/yyyy date format)
        :param duration: Number of days to be added
        :return: New date in the form mm/dd/yyyy
        """
        start_date = start.split('/')
        start_date = date(int(start_date[2]), int(start_date[0]), int(start_date[1]))
        new_date = start_date + datetime.timedelta(days=duration-1)
        return date.strftime(new_date, '%B %d, %Y')

    # ===========================================================
    # Binding methods

    def hover(self, event):
        """
        To be called when the cursor is over an element in the
        canvas.
        :param event:
        :return:
        """
        self.slippage = 0
        point = (event.widget.find_closest(event.x, event.y))[0]
        data = None
        for p in self.points:
            if p['point'] == point:
                data = p
        if data is not None:
            time = data['time']
            self.str_cdp_time.set(data['time'])
            self.str_cdp_accomp.set(round(data['accomp'], 2))
            # Check if time is within the actual accomplishment range
            actual_time_elapsed = self.actual_accomplishment[len(self.actual_accomplishment) - 1]['time']
            if time <= actual_time_elapsed:
                self.calculate_slippage(time)
            self.str_cdp_slippage.set(self.slippage)
            # Get the start date
            if self.str_start_date.get() != '':
                # Start date is not empty, display current date
                curr_date = self.str_start_date.get()
                if '/' in curr_date:
                    start_date = curr_date.split('/')
                    start_date = date(int(start_date[2]), int(start_date[0]), int(start_date[1]))
                    curr_date = start_date + datetime.timedelta(days=int(time))
                    curr_date = date.strftime(curr_date, "%B %d, %Y")
                    self.str_cdp_date.set(curr_date)

    def save_scurve(self):
        """
        Saves the canvas content to an image file.
        """
        fn = fd.asksaveasfilename(initialdir='',
                                  title='Save S-Curve File',
                                  filetypes=[("Postscript files", "*.ps")])
        ps = self.canvas.postscript(file=fn, colormode='color',
                                    rotate=1)
        root = fn[:-2]
        img_file = root + 'jpg'
        import os
        result = os.system('convert ' + fn + ' +antialias ' + img_file)
        print(result)

    def open_project(self):
        fn = fd.askopenfilename(initialdir='/',
                                title='Open Project',
                                filetypes=[("JSON files", "*.json")])
        proj_file = open(fn, 'r')
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

        self.projected_accomplishment = projected_imeplementation
        self.actual_accomplishment = actual_implementation
        self.suspensions = suspensions
        self.canvas.delete('all')
        self.plot_timeline()

        # Trigger the vertical grid option and select the first option
        self.inputs_vert_grid_interval.current(0)
        self.inputs_vert_grid_interval.event_generate('<<ComboboxSelected>>')

        # Enable some controls that are disabled on startup
        self.inputs_vert_grid_interval.config(state='active')
        self.inputs_calculate_btn.config(state='active')

        self.project_opened = True
        self.project_filename = fn

    def reopen_project(self):
        proj_file = open(self.project_filename, 'r')
        proj_file_lines = proj_file.readlines()
        json_string = ''
        for line in proj_file_lines:
            json_string += line
        json_project = json.loads(json_string)
        # Retrieve the projected object timeline
        projected_implementation = json_project['projected']

        # Retrieve actual object timeline
        actual_implementation = json_project['actual']

        # Retrieve suspensions
        suspensions = json_project['suspensions']

        self.projected_accomplishment = projected_implementation
        self.actual_accomplishment = actual_implementation
        self.suspensions = suspensions
        self.canvas.delete('all')
        self.plot_timeline()

        # Trigger the vertical grid option and select the first option
        # self.inputs_verti_grid_interval.current(0)
        self.inputs_vert_grid_interval.event_generate('<<ComboboxSelected>>')

        # Enable some controls that are disabled on startup
        self.inputs_vert_grid_interval.config(state='active')
        self.inputs_calculate_btn.config(state='active')

    def new_project(self):
        fn = fd.asksaveasfilename(initialdir='',
                                  title='New Project',
                                  filetypes=[("JSON File", "*.json")])
        data = {}
        data['projected'] = []

        data['projected'].append({
            'time': 0,
            'accomp': 0
        })

        data['actual'] = []

        data['actual'].append({
            'time': 0,
            'accomp': 0
        })
        data['suspensions'] = []

        data['suspensions'].append({
            'start': 0,
            'duration': 0
        })

        with open(fn, 'w') as output_file:
            json.dump(data, output_file, indent=4)

        self.project_filename = fn

        self.display_grid()

    def edit_actual(self):
        self.dlg = actual_dialog.ActualAccomplishmentDialog(self.parent)
        self.dlg.show(self.project_filename)
        if self.dlg.top is not None:
            self.dlg.top.bind('<FocusIn>', self.actual_table_focused)
            self.dlg.top.protocol('WM_DELETE_WINDOW', self.actual_editor_closed)

    def edit_projected(self):
        self.dlg = projected_dialog.ProjectedAccomplishmentDialog(self.parent)
        self.dlg.show(self.project_filename)
        if self.dlg.top is not None:
            self.dlg.top.bind('<FocusIn>', self.projected_table_focused)
            self.dlg.top.protocol('WM_DELETE_WINDOW', self.projected_editor_closed)

    def edit_suspensions(self):
        self.dlg = suspensions_dialog.SuspensionsDialog(self.parent)
        self.dlg.show(self.project_filename)
        if self.dlg.top is not None:
            self.dlg.top.bind('<FocusIn>', self.suspensions_table_focused)
            self.dlg.top.protocol('WM_DELETE_WINDOW', self.suspensions_editor_closed)

    def projected_editor_closed(self):
        # Reopen the file
        self.reopen_project()

        # Close the editor
        self.dlg.top.destroy()

    def actual_editor_closed(self):
        self.reopen_project()
        self.dlg.top.destroy()

    def suspensions_editor_closed(self):
        self.reopen_project()
        self.dlg.top.destroy()

    def suspensions_table_focused(self, evt):
        data = self.dlg.model.getData()
        temp_suspensions = []
        for i in range(self.dlg.table.rows):
            if ('start' in data[i]) and ('duration' in data[i]):
                s = converter.convert_to_int(data[i]['start'])
                d = converter.convert_to_int(data[i]['duration'])
                temp_suspensions.append({
                    'start': s[0],
                    'duration': d[0]
                })

                self.str_status_message.set(s[1] + ' ' + d[1])

        self.dlg.project_json['suspensions'] = temp_suspensions

        self.dlg.write_data(self.dlg.project_json)

        self.reopen_project()

    def actual_table_focused(self, evt):
        data = self.dlg.model.getData()
        temp_actual = []
        for i in range(self.dlg.table.rows):
            if ('time' in data[i]) and ('accomp' in data[i]):
                t = converter.convert_to_int(data[i]['time'])
                a = converter.convert_to_float(data[i]['accomp'])

                temp_actual.append({
                    'time': t[0],
                    'accomp': a[0]
                })

                self.str_status_message.set(t[1] + ' ' + a[1])

        self.dlg.project_json['actual'] = temp_actual

        self.dlg.write_data(self.dlg.project_json)

        self.reopen_project()

    def projected_table_focused(self, evt):
        data = self.dlg.model.getData()

        temp_projected = []

        for i in range(self.dlg.table.rows):
            if ('time' in data[i]) and ('accomp' in data[i]):
                t = converter.convert_to_int(data[i]['time'])
                a = converter.convert_to_float(data[i]['accomp'])

                temp_projected.append({
                    'time': t[0],
                    'accomp': a[0]
                })

                self.str_status_message.set(t[1] + ' ' + a[1])

        self.dlg.project_json['projected'] = temp_projected

        self.dlg.write_data(self.dlg.project_json)

        self.reopen_project()

    def calculate_btn_pressed(self):
        # For the start date
        str_start_date = self.str_start_date.get()

        # if '/' in str_start_date:
        if self.valid_start_date():
            # Separates the month, day and year
            # start_date = str_start_date.split('/')

            # Convert to date
            # start_date = date(int(start_date[2]), int(start_date[0]), int(start_date[1]))

            # Sets the final duration to the larger of
            # original and revised based on suspensions.
            if int(self.str_summ_orig_completion_days.get()) > int(self.str_summ_rev_completion_days.get()):
                duration = int(self.str_summ_orig_completion_days.get())
            else:
                duration = int(self.str_summ_rev_completion_days.get())

            # end_date = start_date + datetime.timedelta(days=duration - 1)
            end_date = self.get_new_date(str_start_date, duration)
            # self.str_summ_rev_completion_date.set(end_date.strftime("%B %d, %Y"))
            self.str_summ_rev_completion_date.set(end_date)

        else:
            messagebox.showerror('Input Error', 'Invalid date format.\nFormat shall be in the form of \'mm/dd/yyyy\'')

    def cbo_vert_grid_selected(self, event):
        # Draw the vertical grid
        self.canvas.delete('vert_grid')
        vert_grid_interval = self.inputs_vert_grid_interval.current()

        num_of_days = int(self.str_summ_rev_completion_days.get())

        if vert_grid_interval == 0:
            # Interval is every 10 days
            interval = 10
            grid_qty = int(num_of_days / 10)
            for i in range(grid_qty):
                self.canvas.create_line((i + 1) * interval * self.width_factor + self.canvas_left_margin,
                                        self.canvas_top_margin,
                                        (i + 1) * interval * self.width_factor + self.canvas_left_margin,
                                        self.canvas_height - self.canvas_bottom_margin,
                                        fill='#808080',
                                        dash=(2, 2),
                                        tag='vert_grid')
                self.canvas.create_text(i * interval * self.width_factor + self.canvas_left_margin,
                                        self.canvas_top_margin - 20,
                                        text=str(i * interval), tag='vert_grid')
            self.canvas.create_text(num_of_days * self.width_factor + self.canvas_left_margin,
                                    self.canvas_top_margin - 20,
                                    text=str(num_of_days), tag='vert_grid')

        elif vert_grid_interval == 1:
            interval = 30
            # Interval is every 30 days (fixed)
            grid_qty = int(num_of_days / interval)
            for i in range(grid_qty+1):
                self.canvas.create_line((i + 1) * interval * self.width_factor + self.canvas_left_margin,
                                        self.canvas_top_margin,
                                        (i + 1) * interval * self.width_factor + self.canvas_left_margin,
                                        self.canvas_height - self.canvas_bottom_margin,
                                        fill='#808080',
                                        dash=(2, 2),
                                        tag='vert_grid')
                self.canvas.create_text(i * interval * self.width_factor + self.canvas_left_margin,
                                        self.canvas_top_margin - 20,
                                        text=str(i * interval), tag='vert_grid')
            self.canvas.create_text(num_of_days * self.width_factor + self.canvas_left_margin,
                                    self.canvas_top_margin - 20,
                                    text=str(num_of_days), tag='vert_grid')

    def canvas_hover(self, event):
        # TODO: Check time cutting during the addition of suspensions in the graph
        # TODO: Check bug -> Date of last day not showing on canvas hover display
        if (event.x > self.canvas_left_margin) and (event.x < (self.canvas_width - self.canvas_right_margin)):
            if (event.y > self.canvas_top_margin) and (event.y < (self.canvas_height - self.canvas_bottom_margin)) and\
                    self.project_opened:

                # Draw a vertical line
                self.canvas.delete('current_time_indicator')
                self.canvas.create_line(event.x,
                                        self.canvas_top_margin,
                                        event.x,
                                        self.canvas_height - self.canvas_bottom_margin,
                                        fill='green',
                                        tag='current_time_indicator')
                # Find overlaps
                # overlappers = self.canvas.find_overlapping(event.x-10, event.y-10, event.x+10, event.y+10)
                # for o in overlappers:
                #    self.canvas.tag_raise(o)
                self.canvas.tag_lower('current_time_indicator')

                time = self.canvas_location_to_time(event.x)
                self.str_cdp_time.set(time)

                actual_accomp = self.get_accomplishment_at(time, self.actual_accomplishment)
                if type(actual_accomp) == float:
                    self.actual_accomp = round(actual_accomp, 2)
                self.str_cdp_actual_accomp.set(self.actual_accomp)

                projected_accomp = self.get_accomplishment_at(time, self.projected_accomplishment)
                if projected_accomp is not None:
                    self.str_cdp_accomp.set(round(projected_accomp))

                slippage = self.calculate_slippage(time)
                self.str_cdp_slippage.set(slippage)

                curr_date = ''

                if self.valid_start_date():
                    curr_date = self.get_new_date(self.str_start_date.get(), time)
                    self.str_cdp_date.set(curr_date)

                # Show date on cursor
                self.canvas.delete('current_date')
                if event.x / self.canvas_width < 0.8:
                    date_text_anchor = 'sw'
                else:
                    date_text_anchor = 'se'

                self.canvas.create_text(event.x, event.y,
                                        text=curr_date,
                                        anchor=date_text_anchor,
                                        fill='green',
                                        tag='current_date')

    def canvas_location_to_time(self, x):
        """
        Converts the canvas relative x location measured from time = 0 to time
        :return:
        """
        w = self.canvas_width - self.canvas_left_margin - self.canvas_right_margin
        elapsed_x = x - self.canvas_left_margin
        percentage_elapsed = elapsed_x / w
        total_duration = int(self.str_summ_rev_completion_days.get())
        elapsed_time = int(percentage_elapsed * total_duration)

        return elapsed_time