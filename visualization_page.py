import tkinter as tk


class Visualizer(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        canvas = tk.Canvas(self)
        canvas.pack(side="top", fill="both", expand=True)
        canvas.config(width=640, height=480)
