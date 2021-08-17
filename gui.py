import tkinter as tk
from tkinter import Menu, ttk
from tkinter import messagebox as mb
import psycopg2 as ppg
from datetime import datetime as dt
from dateutil import relativedelta as rd
from reportlab.platypus.tables import Table, TableStyle, colors
from tkcalendar import DateEntry
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate
from babel import numbers

# I know embedding the password here commits it to the GitHub 
# repository. This will be fixed and the password changed
# in a future commit, before the repository goes public.
conn = ppg.connect(
    database='postgres', user='postgres', 
    password='vYiSKlo8OOYH0PCjIUFI', host='localhost' 
)
cur = conn.cursor()

PROGRAMS = ['Software Technology', 'Software Development']

class Gui:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title('Course Timeboxer')
        self.root.resizable(False, False)

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(column=0, row=0)

        self.start_date_label = ttk.Label(self.main_frame, 
        text='Enter your start date (M-F):')
        self.start_date_label.grid(column=0, row=0, padx=5, pady=5)

        if dt.now().weekday() in {5, 6}:
            cal_start = dt.now() + rd.relativedelta(weekday=0)
        else:
            cal_start = dt.now()

        self.start_date_dateentry = DateEntry(self.main_frame, 
        firstweekday='sunday', mindate=cal_start, showweeknumbers=False)
        self.start_date_dateentry.grid(column=1, row=0, padx=5, pady=5)

        self.hours_label = ttk.Label(self.main_frame, 
        text='Enter your number of hours enrolled per weekday (0-6):')
        self.hours_label.grid(column=0, row=1, columnspan=2, pady=(0,5))

        self.weekdays_frame = ttk.Frame(self.main_frame)
        self.weekdays_frame.grid(column=0, row=2, columnspan=2)

        self.monday_label = ttk.Label(self.weekdays_frame,
        text = 'M')
        # self.monday_label.pack(side='left', fill='x')
        self.monday_label.grid(column=0, row=0)

        self.tuesday_label = ttk.Label(self.weekdays_frame,
        text = 'T')
        # self.tuesday_label.pack(side='left', fill='x')
        self.tuesday_label.grid(column=1, row=0)

        self.wednesday_label = ttk.Label(self.weekdays_frame,
        text = 'W')
        # self.wednesday_label.pack(side='left', fill='x')
        self.wednesday_label.grid(column=2, row=0)

        self.thursday_label = ttk.Label(self.weekdays_frame,
        text = 'Th')
        # self.thursday_label.pack(side='left', fill='x')
        self.thursday_label.grid(column=3, row=0)

        self.friday_label = ttk.Label(self.weekdays_frame,
        text = 'F')
        # self.friday_label.pack(side='left', fill='x')
        self.friday_label.grid(column=4, row=0)
        
        self.monday_stringvar = tk.StringVar(value=0)
        self.monday_spinbox = ttk.Spinbox(self.weekdays_frame, from_=0, 
        to=6, textvariable=self.monday_stringvar, width=2)
        self.monday_spinbox.grid(column=0, row=1)

        self.tuesday_stringvar = tk.StringVar(value=0)
        self.tuesday_spinbox = ttk.Spinbox(self.weekdays_frame, from_=0, 
        to=6, textvariable=self.tuesday_stringvar, width=2)
        self.tuesday_spinbox.grid(column=1, row=1, padx=(8,0))

        self.wednesday_stringvar = tk.StringVar(value=0)
        self.wednesday_spinbox = ttk.Spinbox(self.weekdays_frame, from_=0, 
        to=6, textvariable=self.wednesday_stringvar, width=2)
        self.wednesday_spinbox.grid(column=2, row=1, padx=(8,0))

        self.thursday_stringvar = tk.StringVar(value=0)
        self.thursday_spinbox = ttk.Spinbox(self.weekdays_frame, from_=0, 
        to=6, textvariable=self.thursday_stringvar, width=2)
        self.thursday_spinbox.grid(column=3, row=1, padx=(8,0))

        self.friday_stringvar = tk.StringVar(value=0)
        self.friday_spinbox = ttk.Spinbox(self.weekdays_frame, from_=0, 
        to=6, textvariable=self.friday_stringvar, width=2)
        self.friday_spinbox.grid(column=4, row=1, padx=(8,0))
        
        '''self.hours_label = ttk.Label(self.main_frame, 
        text='Enter your number of hours\nenrolled per week (from 6 to 30):')
        self.hours_label.grid(column=0, row=1, padx=5, pady=5)

        self.hours_stringvar = tk.StringVar(value=30)
        self.hours_spinbox = ttk.Spinbox(self.main_frame, from_=6, 
        to=30, textvariable=self.hours_stringvar)
        self.hours_spinbox.grid(column=1, row=1, padx=5, pady=5)'''

        self.program_label = ttk.Label(self.main_frame,
        text='Select your program:')
        self.program_label.grid(column=0, row=3)

        self.program_stringvar = tk.StringVar(value='')
        self.program_options = PROGRAMS

        self.program_optionmenu = ttk.OptionMenu(self.main_frame, 
        self.program_stringvar, '', *self.program_options, 
        command=self.select_program)
        self.program_optionmenu.grid(column=1, row=3)

        self.course_label = ttk.Label(self.main_frame, 
        text='Select your course:')
        self.course_label.grid(column=0, row=4, padx=5, pady=5)

        self.course_stringvar = tk.StringVar(value='')
        self.course_options = []

        # Retrieves all the table names in the database 
        # and adds them to self.course_options as selectable course options
        # cur.execute("""SELECT table_name FROM information_schema.tables 
        # WHERE table_schema = 'COURSE'""")
        # for table_name in cur.fetchall():
        #     self.course_options.append(table_name)

        self.course_optionmenu = ttk.OptionMenu(self.main_frame, 
        self.course_stringvar, '', *self.course_options)
        self.course_optionmenu.grid(column=1, row=4, padx=5, pady=5)

        self.submit_button = ttk.Button(self.main_frame, text='Submit', 
        command=self.validate_input)
        self.submit_button.grid(column=0, row=5, columnspan=2, pady=10)

        self.root.bind('<Return>', self.validate_input)

        tk.mainloop()

    def select_program(self, program_stringvar):
        for program in PROGRAMS:
            if program_stringvar == program:
                cur.execute(f"""SELECT table_name FROM 
                information_schema.tables WHERE 
                table_schema='{program}'""")
        
        # Resets the list contents, in case a different program is selected
        self.course_options = []
        
        for table_tuple in cur.fetchall():
            self.course_options.append(table_tuple[0])
        
        self.update_course_options(self.course_options)
    
    def update_course_options(self, course_options):
        course_menu = self.course_optionmenu['menu']
        course_menu.delete(0, 'end')
        for course in course_options:
            course_menu.add_command(label=course,
            command=lambda value=course: self.course_stringvar.set(value))

    def validate_input(self, event=True):

        if self.start_date_dateentry.get_date().weekday() in {5, 6}:
            mb.showerror('Invalid entry', 
            'Please enter a weekday start date.')
        else:
            weekday_stringvar_list = [self.monday_stringvar.get(), 
            self.tuesday_stringvar.get(), self.wednesday_stringvar.get(), 
            self.thursday_stringvar.get(), self.friday_stringvar.get()]
            
            continue_sentinel = True

            for i in range(len(weekday_stringvar_list)):
                try:
                    int_stringvar = int(weekday_stringvar_list[i])
                except Exception:
                    mb.showerror('Invalid entry', 
                    'Please enter a number of hours between 0 and 6.')
                    return False
                else:
                    weekday_stringvar_list[i] = int_stringvar
                    if int_stringvar not in range(7):
                        mb.showerror('Invalid entry',
                        'Please enter a number of hours between 0 and 6.')
                        return False
                
            if sum(weekday_stringvar_list) not in range(6, 31):
                mb.showerror('Invalid entry',
                'Please enter between 6 and 30 hours total.')
                continue_sentinel = False

            if continue_sentinel:

                # We append two 0's to the end as the hours 
                # attended on weekends
                weekday_stringvar_list.append(0)
                weekday_stringvar_list.append(0)

                self.create_schedule(weekday_stringvar_list)
            
            '''try:
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
                    self.create_schedule(int(self.hours_stringvar.get()))'''

    def create_schedule(self, week_schedule):
        cur.execute(f'''select "Name", hours from postgres."{self.program_stringvar.get().lstrip("('").rstrip("',)")}"."{self.course_stringvar.get().lstrip("('").rstrip("',)")}"''')
        
        module_list = cur.fetchall()
        # hour_total = 0
        # datetime_now = dt.now()
        start_date = self.start_date_dateentry.get_date()

        # If the current day is a weekend, starts calculating the due date
        # from midnight on the next Monday
        '''
        if datetime_now.weekday() == 5:
            datetime_now += rd.relativedelta(days=2)
            datetime_now = datetime_now.replace(hour=0, minute=0, 
            second=0, microsecond=0)
        elif datetime_now.weekday() == 6:
            datetime_now += rd.relativedelta(days=1)
            datetime_now = datetime_now.replace(hour=0, minute=0, 
            second=0, microsecond=0)
        '''

        '''for module_tuple in module_list:
            hour_total += module_tuple[1]'''

        hours_left_in_day = 0
        new_module_list = []
        current_day = self.start_date_dateentry.get_date()
        
        for module_tuple in module_list:
            remaining_module_hours = module_tuple[1]
            
            if hours_left_in_day > remaining_module_hours:
                new_module_list.append((module_tuple[0], current_day
                .strftime('%a, %b %#d, %Y')))
                hours_left_in_day -= remaining_module_hours
                remaining_module_hours = 0
                continue
            elif hours_left_in_day == remaining_module_hours:
                new_module_list.append((module_tuple[0], current_day
                .strftime('%a, %b %#d, %Y')))
                hours_left_in_day -= remaining_module_hours
                remaining_module_hours = 0
                current_day += rd.relativedelta(days=1)
                continue
            elif hours_left_in_day != 0:
                remaining_module_hours -= hours_left_in_day
                hours_left_in_day = 0
                current_day += rd.relativedelta(days=1)

            while True:
                if (remaining_module_hours 
                >= week_schedule[current_day.weekday()]):
                    remaining_module_hours \
                    -= week_schedule[current_day.weekday()]
                    if remaining_module_hours == 0:
                        new_module_list.append((module_tuple[0], current_day
                        .strftime('%a, %b %#d, %Y')))
                        break
                    current_day += rd.relativedelta(days=1)
                    continue
                elif remaining_module_hours != 0:
                    # current_day += rd.relativedelta(days=1)
                    hours_left_in_day = (week_schedule[current_day.weekday()]
                    - remaining_module_hours)
                    remaining_module_hours = 0
                    new_module_list.append((module_tuple[0], current_day
                    .strftime('%a, %b %#d, %Y')))
                    break
                else:
                    hours_left_in_day = 0
                    new_module_list.append((module_tuple[0], current_day
                    .strftime('%a, %b %#d, %Y')))
                    break
        
        '''for module_tuple in module_list:

            weeks_to_complete = module_tuple[1] / weekly_hours

            week_delta = rd.relativedelta(weeks=weeks_to_complete)

            due_date = start_date + week_delta'''
            
            # Adds extra days to the due date to ensure the student is not
            # required to work on weekends
        '''     if week_delta.days < 7 and due_date.day < datetime_now.day:
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
        '''     if due_date.weekday() == 5:
                due_date += rd.relativedelta(days=2)
                week_delta += rd.relativedelta(days=2)
                print(f"Due date adjusted for landing on weekend: {due_date.strftime('%a, %b %#d, %Y')}")
            elif due_date.weekday() == 6:
                due_date += rd.relativedelta(days=1)
                week_delta += rd.relativedelta(days=1)
                print(f"Due date adjusted for landing on weekend: {due_date.strftime('%a, %b %#d, %Y')}")'''

            

            # start_date += week_delta

        self.create_schedule_treeview(new_module_list)

    # Secondary module list so the below treeview's contents can be accessed
    # again later, after being appended to this list in below function
    outer_module_list = []

    def create_schedule_treeview(self, module_list):
        # Resets list contents to prevent unexpected results in the case where
        # user changes their course selection
        self.outer_module_list = []

        self.treeview_columns = ('#1', '#2')

        self.schedule_treeview = ttk.Treeview(self.root, 
        columns=self.treeview_columns, show='headings')

        self.schedule_treeview.heading('#1', text='Module')
        self.schedule_treeview.heading('#2', text='Due Date')

        for module_tuple in module_list:
            self.schedule_treeview.insert('', tk.END, values=module_tuple)
            self.outer_module_list.append(module_tuple)

        self.schedule_treeview.grid(column=0, row=6, columnspan=2, pady=10)

        self.create_pdf_button()

    def create_pdf_button(self):
        self.pdf_button = ttk.Button(self.main_frame, text='Export to PDF',
        command=self.create_pdf)

        # Removes the submit button so it can be re-placed
        # beside the new button
        self.submit_button.grid_forget()
        self.submit_button.grid(column=0, row=5, sticky='EW', padx=(8, 0))
        self.pdf_button.grid(column=1, row=5, sticky='EW', padx=(0, 8))

    def create_pdf(self):
        doc = SimpleDocTemplate('course_timeboxer_report.pdf', 
        pagesize=letter, leftMargin=72, rightMargin=72, topMargin=72, 
        bottomMargin=72)
        story = []
        data = []

        for module_tuple in self.outer_module_list:
            data.append([module_tuple[0], module_tuple[1]])

        t=Table(data)
        t.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.25, colors.black)]))

        story.append(t)
        doc.build(story)
        
        # Line below is a deliberate violation of PEP8, because breaking
        # the line causes a formatting error in the message
        mb.showinfo(title='PDF Created', 
        message='Your PDF has been successfully created in the same directory as this program.')

    def close_db_conn(self):
        cur.close()
        conn.close()
