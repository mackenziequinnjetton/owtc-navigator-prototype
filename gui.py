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

        self.root = tk.Tk()
        self.root.title('Course Timeboxer')
        self.root.resizable(False, False)

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
        # and adds them to self.course_options as selectable course options
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

        # If the current day is a weekend, starts calculating the due date
        # from midnight on the next Monday
        if datetime_now.weekday() == 5:
            datetime_now += rd.relativedelta(days=2)
            datetime_now = datetime_now.replace(hour=0, minute=0, 
            second=0, microsecond=0)
        elif datetime_now.weekday() == 6:
            datetime_now += rd.relativedelta(days=1)
            datetime_now = datetime_now.replace(hour=0, minute=0, 
            second=0, microsecond=0)

        for module_tuple in module_list:
            hour_total += module_tuple[1]

        new_module_list = []
        
        for module_tuple in module_list:

            weeks_to_complete = module_tuple[1] / weekly_hours

            week_delta = rd.relativedelta(weeks=weeks_to_complete)

            due_date = datetime_now + week_delta
            
            # Adds extra days to the due date to ensure the student is not
            # required to work on weekends
            '''if week_delta.days < 7 and due_date.day < datetime_now.day:
                print('Condition 1 triggered')
                due_date += rd.relativedelta(days=2)
                print(f"Due date adjusted for passing weekends: {due_date.strftime('%a, %b %#d, %Y')}")
            else:
                print('Condition 2 triggered')
                full_weeks = week_delta.days // 7
                days_left = week_delta.days % 7
                due_date += rd.relativedelta(days=2 * full_weeks)
                if due_date.day + days_left > 6:
                    print('Condition 3 triggered')
                    due_date += rd.relativedelta(days=2)
                print(f"Due date adjusted for passing weekends: {due_date.strftime('%a, %b %#d, %Y')}")'''
            
            # If the due date will be on a weekend, moves the due date
            # to the next Monday
            '''if due_date.weekday() == 5:
                due_date += rd.relativedelta(days=2)
                week_delta += rd.relativedelta(days=2)
                print(f"Due date adjusted for landing on weekend: {due_date.strftime('%a, %b %#d, %Y')}")
            elif due_date.weekday() == 6:
                due_date += rd.relativedelta(days=1)
                week_delta += rd.relativedelta(days=1)
                print(f"Due date adjusted for landing on weekend: {due_date.strftime('%a, %b %#d, %Y')}")'''

            new_module_list.append((module_tuple[0], due_date
            .strftime('%a, %b %#d, %Y')))

            datetime_now += week_delta

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
