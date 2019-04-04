import json
import os

from visualization_page import *

if __name__ == '__main__':
    root = tk.Tk()

    root.iconbitmap(os.getcwd() + '\\res\\icons\\icon.ico')

    timeline = Timeline(root)

    root.mainloop()
