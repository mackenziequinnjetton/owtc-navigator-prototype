import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import psycopg2 as ppg
from datetime import datetime as dt
from dateutil import relativedelta as rd
import math

# I know embedding the password here commits it to the GitHub 
# repository. This will be fixed and the password changed
# in a future commit, before the repository goes public.
conn = ppg.connect(
    database='postgres', user='postgres', 
    password='vYiSKlo8OOYH0PCjIUFI', host='localhost' 
)
cur = conn.cursor()

class Gui:

    def __init__(self):

        """# I know embedding the password here commits it to the GitHub 
        # repository. This will be fixed and the password changed
        # in a future commit, before the repository goes public.
        conn = ppg.connect(
            database='postgres', user='postgres', 
            password='vYiSKlo8OOYH0PCjIUFI', host='localhost' 
        )
        cur = conn.cursor()"""

        self.root = tk.Tk()
        self.root.title('Course Timeboxer')
        # self.root.geometry('350x300')
        self.root.resizable(False, False)

        # self.root.columnconfigure(0, weight=1)
        # self.root.columnconfigure(1, weight=2)

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(column=0, row=0)

        self.hours_label = ttk.Label(self.main_frame, 
        text='Enter your number of hours\nenrolled per week (from 6 to 30):')
        self.hours_label.grid(column=0, row=0, padx=5, pady=5)

        self.hours_stringvar = tk.StringVar(value=30)
        self.hours_spinbox = ttk.Spinbox(self.main_frame, from_=6, 
        to=30, textvariable=self.hours_stringvar)
        self.hours_spinbox.grid(column=1, row=0, padx=5)

        self.course_label = ttk.Label(self.main_frame, 
        text='Select your course:')
        self.course_label.grid(column=0, row=1)

        self.course_stringvar = tk.StringVar(value='')
        self.course_options = []

        # Retrieves all the table names in the database 
        # and adds them to self.course_options as selectable options
        cur.execute("""SELECT table_name FROM information_schema.tables 
        WHERE table_schema = 'COURSE'""")
        for table_name in cur.fetchall():
            self.course_options.append(table_name)

        self.course_optionmenu = ttk.OptionMenu(self.main_frame, 
        self.course_stringvar, self.course_options[0], 
        *self.course_options)
        self.course_optionmenu.grid(column=1, row=1)

        self.submit_button = ttk.Button(self.main_frame, text='Submit', 
        command=self.validate_hours)
        self.submit_button.grid(column=0, row=2, columnspan=2, pady=10)

        self.root.bind('<Return>', self.validate_hours)

        '''cur.close()
        conn.close()'''

        tk.mainloop()

    def validate_hours(self, event=True):
        try:
            int(self.hours_stringvar.get())
        except Exception:
            mb.showerror('Invalid entry', 
            'Please enter a number of hours between 6 and 30.')
        else:
            if (int(self.hours_stringvar.get()) < 6 
            or int(self.hours_stringvar.get()) > 30):
                mb.showerror('Invalid entry', 
                'Please select a number of hours between 6 and 30.')
            else:
                self.create_schedule(int(self.hours_stringvar.get()))

    def create_schedule(self, weekly_hours):
        cur.execute(f'''select "Name", hours from "COURSE".
        {self.course_stringvar.get().lstrip("('").rstrip("',)")}''')
        
        module_list = cur.fetchall()
        hour_total = 0
        datetime_now = dt.now()

        for module_tuple in module_list:
            hour_total += module_tuple[1]

        remaining_days = 0
        new_module_list = []
        
        for module_tuple in module_list:
            weeks_to_complete = math.ceil((module_tuple[1] 
            + remaining_days) / weekly_hours)

            # The due date for each module is assumed to be the Saturday of 
            # the week when the module is due
            week_delta = rd.relativedelta(weeks=weeks_to_complete, 
            weekday=rd.SA(1))

            new_module_list.append((module_tuple[0], (datetime_now 
            + week_delta).strftime('%a, %b %w, %Y')))

            datetime_now = datetime_now + week_delta

            remaining_days = (module_tuple[1] + remaining_days) % weekly_hours

        self.create_schedule_treeview(new_module_list)

    def create_schedule_treeview(self, module_list):
        self.treeview_columns = ('#1', '#2')

        self.schedule_treeview = ttk.Treeview(self.root, 
        columns=self.treeview_columns, show='headings')

        self.schedule_treeview.heading('#1', text='Module')
        self.schedule_treeview.heading('#2', text='Due Date')

        for module_tuple in module_list:
            self.schedule_treeview.insert('', tk.END, values=module_tuple)

        self.schedule_treeview.grid(column=0, row=3, columnspan=2)

    def close_db_conn(self):
        cur.close()
        conn.close()
