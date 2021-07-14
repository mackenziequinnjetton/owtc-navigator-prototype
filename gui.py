import tkinter as tk
from tkinter import ttk
import psycopg2 as ppg

class Gui:
    def __init__(self):
        conn = ppg.connect(
            database='COURSE', user='postgres', password='vYiSKlo8OOYH0PCjIUFI', host='localhost'
        )

        self.root = tk.Tk()
        self.root.title('Course Timeboxer')

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)

        ## self.main_frame = ttk.Frame()

        self.hours_label = ttk.Label(self.root, text='Enter your number of hours enrolled per week:')
        self.hours_label.grid(column=0, row=0)

        self.hours

        tk.mainloop()
