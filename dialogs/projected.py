import tkinter as tk


class ProjectedAccomplishmentDialog(tk.Toplevel):
    def __init__(self, parent, data, title=None):

        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        # Set the title
        if title:
            self.title(title)
        else:
            self.title('Projected Accomplishment')

        self.parent = parent
        self.result = None

        body = tk.Frame(self)
        self.initial_focus = self.body(body)

