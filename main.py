import json
import os

from main_window import *

if __name__ == '__main__':
    root = tk.Tk()

    # root.iconbitmap(os.getcwd() + '\\res\\icons\\icon.ico')

    timeline = Timeline(root)
    timeline.pack(fill='both', expand='yes')

    root.mainloop()
