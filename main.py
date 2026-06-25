"""Something here"""
import tkinter as tk
from tkinter import ttk, messagebox as mb, filedialog
import csv
from datetime import datetime as dt
import time


class Todo_app:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDoApp")
        self.root.geometry("900x550")
        self.root.resizable(width=False, height=False)

        self.tabs = ttk.Notebook(root)
        self.dashboard_tab = ttk.Frame(self.tabs)
        self.todo_tab = ttk.Frame(self.tabs)
        self.timer_tab = ttk.Frame(self.tabs)

        self.tasks = []
        self.PATH = "todo_file.csv"

        self.tabs.add(self.dashboard_tab, text="Dashboard")
        self.tabs.add(self.todo_tab, text="To-Do List")
        self.tabs.add(self.timer_tab, text="Timer")
        self.tabs.pack(expand=True, fill="both")
        self.tabs.bind("<<NotebookTabChanged>>", self.calc_percent)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('custom.Horizontal.TProgressbar', 
                             background='#18bc9c', 
                             troughcolor='#ecf0f1'
                            )

        self.create_dashboard()
        self.create_task_manager()
        self.create_timer()

        self.load(self.PATH)
        self.sort(event=None)

    def create_dashboard(self):
        """The method create the dashboard"""
        ttk.Label(
                    self.dashboard_tab,
                    text="📊Dashboard",
                    font=("Segoe UI", 18, "bold")
                ).pack(pady=50)
        self.p_label = ttk.Label(
                    self.dashboard_tab,
                    text="X % completed",
                    font=("Segoe UI", 12)
                )
        self.p_label.pack(padx=5)

        self.progress = ttk.Progressbar(self.dashboard_tab, 
                                    orient="horizontal", 
                                    length=850, 
                                    mode='determinate',
                                    style='custom.Horizontal.TProgressbar'
                                    )
        self.progress.pack(padx=5)
    
    def create_task_manager(self):
        """This method create all of the widget inside the task manager."""

        SORT_CATE = ['Name', 'Due Date', 'Highest Priority', 'Lowest Priority', 
                    'Completed', 'Incomplete'
                    ]
        DAYS = [d for d in range(1, 31+1)]
        MONTH = [m for m in range(1, 12+1)]
        P_ORDER = ['Low', 'Medium', 'High']
        table_cols = ('Title', 'Due Date', 'Priority', 'State')
        today = dt.now()

        
        top = ttk.LabelFrame(self.todo_tab, text="➕ Add New Task")
        top.pack(fill="x", padx=10, pady=5)

        ttk.Label(top, text="Title").grid(row=0, column=0, padx=5)
        self.title_entry = ttk.Entry(top, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Priority selector
        ttk.Label(top, text="Priority").grid(row=0, column=2, padx=5)
        self.priority_entry = ttk.Combobox(top, 
                                           values=P_ORDER,
                                           state='readonly',
                                           )
        self.priority_entry.grid(row=0, column=3, padx=5, pady=5)
        self.priority_entry.current(0)
        self.priority_entry.bind("<<ComboboxSelected>>", self.combo_colour)
        style_name_1 = f"Combo1_{id(self.priority_entry)}.TCombobox"
        self.priority_entry.configure(style=style_name_1)
        
        # Create the Due Date entry so the user can choose date in dd-MM-YYYY
        ttk.Label(top, text="Due Date:").grid(row=1, column=0, padx=5)
        due_date_frame = ttk.Frame(top)
        due_date_frame.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(due_date_frame, text="DD:").pack(side="left", padx=5)
        self.date_entry = ttk.Combobox(due_date_frame, 
                                       values= DAYS,
                                       width= 3)
        self.date_entry.pack(side="left", padx=5, pady=5)
        self.date_entry.set(today.strftime("%d"))
        
        ttk.Label(due_date_frame, text="MM:").pack(side="left", padx=5)
        self.month_entry = ttk.Combobox(due_date_frame, 
                                       values=MONTH,
                                       width= 3)
        self.month_entry.pack(side="left", padx=5, pady=5)
        self.month_entry.set(today.strftime("%m"))
        
        ttk.Label(due_date_frame, text="YYYY:").pack(side="left", padx=5)
        self.year_entry = ttk.Entry(due_date_frame,
                                    width=6)
        self.year_entry.pack(side="left", padx=5, pady=5)
        self.year_entry.insert(0, today.strftime("%Y"))

        # add button
        self.add_bt = ttk.Button(top, text="✅Add Task", command=self.add)
        self.add_bt.grid(row=1, column=3, padx=5, pady=5)
        
        # delete, sort, import, export and configuring the treeview(table)
        button_bar = ttk.Frame(self.todo_tab)
        button_bar.pack(fill="x", padx=10, pady=5)

        delete_bt = ttk.Button(button_bar, text="✖️Delete"
                               ,command=self.remove
                               )
        delete_bt.pack(side="left", padx=10, pady=5)

        delete_all_bt = tk.Button(button_bar, text="⚠Delete All",
                                   command=self.clear_all
                                   )
        delete_all_bt.pack(side="right", padx=10, pady=5)
        
        ttk.Label(button_bar, text="Sort by:").pack(side="left")
        self.sort_bar = ttk.Combobox(button_bar, values=SORT_CATE,
                                      state="readonly",
                                     )
        self.sort_bar.pack(side="left", padx=10, pady=5)
        self.sort_bar.current(0)
        self.sort_bar.bind("<<ComboboxSelected>>", self.sort)

        load_bt = ttk.Button(button_bar, text="Import⬇️",
                            command=self.load
                            ).pack(side="left", padx=10, pady=5)
            
        export_bt = ttk.Button(button_bar, text="Export⬆️", 
                                command=self.export
                                ).pack(side="left", padx=10, pady=5)

        self.table = ttk.Treeview(self.todo_tab, 
                                  columns= table_cols,
                                  show="headings",
                                  height=18)
        for column in table_cols:
            self.table.heading(column, text=column)
            self.table.column(column, anchor="center")
        self.table.pack(fill="both", expand=True, padx=10)

        # User can double click to mark a task done
        self.table.bind("<Double-1>", self.mark_done)
        # Colour code task based on priority
        self.table.tag_configure("Medium", background="yellow")
        self.table.tag_configure("High", background="orange")
        self.table.tag_configure("Done", background="#94C748")
        self.table.tag_configure("Overdue", background="red")
    
    def create_timer(self):
        """ Pomodoro Timer"""
        FONT = ("Segoe UI", 60, "bold")
        self.hour=tk.StringVar(value="00")
        self.minute=tk.StringVar(value="00")
        self.second=tk.StringVar(value="00")
        self.timer_running = False
        self.Duration = 0
        self.last_saved_t = 0

        self.hourEntry= ttk.Entry(self.timer_tab, width=3, font=FONT, 
                             textvariable=self.hour
                             )
        self.hourEntry.place(x=210,y=75, width=120)

        ttk.Label(self.timer_tab, width=3, font=FONT, text=":").place(x=350, y=75)

        self.minuteEntry= ttk.Entry(self.timer_tab, width=3, font=FONT,
                               textvariable=self.minute
                               )
        self.minuteEntry.place(x=390, y=75, width=120)

        ttk.Label(self.timer_tab, width=3, font=FONT, text=":").place(x=530,y=75)

        self.secondEntry= ttk.Entry(self.timer_tab, width=3, font=FONT, 
                               textvariable=self.second
                               )
        self.secondEntry.place(x=570, y=75, width=120)

        # ▶  ⏸️
        self.pause_bt = ttk.Button(self.timer_tab, text="▶", command=self.pause)
        self.pause_bt.place(anchor="center", x=450, y=300)

        skip_bt = ttk.Button(self.timer_tab, text="⏭", command=self.end_timer)
        skip_bt.place(anchor="center", x=625, y=300)

        restart_bt = ttk.Button(self.timer_tab, text="⟲", command=self.restart)
        restart_bt.place(anchor="center", x=275, y=300)


        self.status_label = tk.Label(self.timer_tab, 
                                     text=(f"Saved time:{self.last_saved_t}")
                                    )
        self.status_label.place(anchor="center", x=450, y=400)

    def refresh(self):
        """This method updates the table rows by removing everything
        then reinsert items from the list.""" 
        current_date = dt.now().strftime("%d-%m-%Y")

        # Update table
        rows = self.table.get_children()
        for row in rows:
            self.table.delete(row)
        for i in range(len(self.tasks)):
            task = self.tasks[i]
            value=(task['title'], task['due'], task['priority'], task['state'])
            if task['state'] == "✅":
                tag='Done'
            elif task['due'] < current_date:
                tag='Overdue'
            else:
                tag=task['priority']
            row_id = self.table.insert(
                "", "end",
                values=value,
                tags=tag
            )
            self.tasks[i]["id"] = row_id

        
        # Update CSV file
        fieldnames = ('due', 'title', 'id', 'priority', 'state')
        with open(self.PATH, "w", newline='', encoding='utf-8') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(fieldnames)
            for task in self.tasks:
                val = (task['due'], task['title'], task['id'], task['priority'], 
                       task['state']
                       )
                csv_writer.writerow(val)

    def calc_percent(self, event = None):
        """The method make sure the cursor isn't automatically put on and 
        highlight entry box w/ focus_set(). It also calculate the percentage 
        of completed task if clicked on the dashboard(frame0)"""
        event.widget.focus_set()
        dashboard = '.!notebook.!frame'
        completed = 0
        incompleted = 0
        current_tab = self.tabs.select()
        if current_tab == dashboard:
            for task in self.tasks:
                if task['state'] == '✅':
                    completed += 1
                else:
                    incompleted += 1
            try:
            
                completed_percent = int(100 * completed / (incompleted + completed))
            except ZeroDivisionError:
                self.p_label['text'] = "0%"
                self.progress['value'] = 0
            else:
                self.p_label['text'] = f"{completed_percent}% Completed"
                self.progress['value'] = completed_percent
    
    def validate_dt(self, date_text, date_format="%d-%m-%Y"):
        """The method check the date_text and compare it
        to the date_format, return true false."""
        try:
            dt.strptime(date_text, date_format)
            return True
        except ValueError as e:
            mb.showerror("Something went wrong", e)
            return False
    
    def add(self):
        """The method get the title an due date
        then validate the data, added the new task to the 
        list above and refresh it"""
        title = self.title_entry.get()
        title.strip()

        d = self.date_entry.get()
        M = self.month_entry.get()
        Y = self.year_entry.get()
        due_date = f"{d}-{M}-{Y}"

        priority = self.priority_entry.get()

        if not title:
            mb.showerror("Missing input", "Title required")
            return
        
        if not self.validate_dt(due_date):
            return
        
        self.tasks.append({
            "title":    title,
            "due":   due_date,
            "priority": priority,
            "state": "☐"
            })
        
        self.refresh()
        self.date_entry.delete(0, tk.END)
        self.month_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.title_entry.delete(0, tk.END) 

    def remove(self):
        """This method get the ID from the selected children
        in the table. Then it compare the ID to tasks
        dictionary and remove matches task"""
        for item in self.table.selection():
            for task in self.tasks:
                if task.get("id") == item:
                    self.tasks.remove(task)
        self.refresh()

    def clear_all(self):
        """The Method ask a confirmation before deleting
        all the entries in the tasks dictionary"""
        if mb.askyesno("Warning, this action cannot be undo!",
                        "Are you sure you want to DELETE ALL existing tasks?"):
            self.tasks.clear()
            self.refresh()
        else:
            return
        
    def combo_colour(self, event):
        """This method get the style of the widget then changes it base
        on the current value, used to indicate for the priority selector"""
        widget = event.widget
        current = widget.get()
        style_name = widget.cget("style")
        if current == "High":
            bg_color = "orange"
        elif current == "Medium":
            bg_color = "yellow"
        else:
            bg_color = "white"
        
        self.style.map(style_name, 
                    fieldbackground=[('readonly', bg_color)],
                    background=[('readonly', bg_color)])

    def load(self, Path=None):
        """This method have the path as none type for default 
        to let the method continue if no path was provided. It then try to open
        the path and take in the information from the provided file.
        If there's a an error with a file, it is shown in message box"""
        if Path is None:
            Path = filedialog.askopenfilename(filetypes=[("CSV file","*.csv")]
                                             )
            if not Path:
                return

        exist_id = {task.get('id') for task in self.tasks}
        try:
            with open(Path, mode = "r", encoding='utf-8') as f:
                csv_writer = csv.DictReader(f)
                for line in csv_writer:
                    task_id = line['id']
                    if line['id'] not in exist_id:
                        self.tasks.append({
                                        "title":  line['title'],
                                        "due":   line['due'],
                                        "id":     task_id,
                                        "priority": line['priority'],
                                        "state": line['state']
                                        })
                self.refresh()
        except (TypeError, FileNotFoundError, KeyError) as e:
            mb.showerror("Error", 
                         f"Error: Could not open file '{Path}'. ({e})"
                        )
            return
            
    def export(self):
        """This method save a path to user choosing and write
        that like a csv file"""
        new_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv")],
                                            title="Save File As CSV"
                                               )

        if not new_path:
            return

        else:
            fieldnames = ('due', 'title', 'id', 'priority', 'state')
            with open(new_path, "w", newline='', encoding='utf-8') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(fieldnames)
                for task in self.tasks:
                    values = (task['due'], task['title'], task['id'], 
                              task['priority'], task['state']
                             )
                    csv_writer.writerow(values)

    def sort(self, event):
        """The method get the category from the sort bar
        then use the sorted function to organise the list of tasks"""
        p_order = ['High', 'Medium', 'Low']

        sorting_rules = {
            #category : (key function for sorting, should reverse)
            'Name': (lambda task: task['title'], False),
            'Due Date': (lambda task: dt.strptime(task['due'], '%d-%m-%Y'),False
                        ),
            'Highest Priority': (lambda task: p_order.index(task['priority']), 
                                 False
                                ),
            'Lowest Priority': (lambda task: p_order.index(task['priority']), 
                                True
                                ),
            'Completed': (lambda task: task['state'], True),
            'Incomplete': (lambda task: task['state'], False),
            }
        category = self.sort_bar.get()
        rule = sorting_rules.get(category)

        if rule:
            key_function, should_reverse = rule
            self.tasks = sorted(self.tasks, key=key_function, reverse=should_reverse)
        self.refresh()

    def mark_done(self, event):
        """This method get the ID. Then check for any selection
        outside the tree's index. Finally, it checks through
        the existing task for ID and replace the state"""
        try:
            item = self.table.selection()[0]

        except IndexError:
            # prevent program from returning data of header column
            return
        
        else:
            for task in self.tasks:
                if task.get("id") == item:
                    task["state"] = "✅" if task["state"] == "☐" else "☐"

        self.refresh()    
    
    def set_time(self, hour="00", minute="00", second="00"):
        """This method set the time in the stringVar, default is 00"""
        self.hour.set(hour)
        self.minute.set(minute)
        self.second.set(second)

    def update_timer(self):
        """This method update the timer every 1 second"""
        if not self.timer_running:
            return

        # Decrement the duration directly
        self.Duration -= 1

        if self.Duration < 0:
            self.timer_running = False
            self.last_saved_t = 0
            self.set_time("00", "00", "00")
            self.enable_entries() 
            self.pause_bt['text'] = "▶"
            mb.showinfo("Countdown Timer", "Time is up!")
            return

        # Calculate remaining time
        new_H = self.Duration // 3600
        new_M = (self.Duration // 60) % 60
        new_S = self.Duration % 60

        # Update GUI
        self.set_time(f"{new_H:02d}", f"{new_M:02d}", f"{new_S:02d}")
        self.status_label['text'] = f"Saved time:{self.last_saved_t}"
        
        # Schedule next tick
        self.root.after(1000, self.update_timer)
        

    def pause(self):
        """The method toggles between resume and pausing"""
        """Handles starting, pausing, and resuming from a single button."""
        # Case 1: Timer is running, Pause it
        if self.timer_running:
            self.timer_running = False
            self.pause_bt['text'] = "▶"
            self.enable_entries()
            return

        # Case 2: Timer is stopped, and duration is 0,  Start a brand new timer
        if self.Duration == 0:
            try:
                self.Duration = (3600 * int(self.hour.get()) + 
                                60 * int(self.minute.get()) + 
                                int(self.second.get()))
                self.last_saved_t = self.Duration 
            except ValueError:
                mb.showerror("Error", "Please enter valid numbers")
                return

            if self.Duration <= 0:
                mb.showwarning("Warning", "Please set a time greater than 0")
                return

        # Case 3: Resuming a paused timer OR successfully started a new one
        self.timer_running = True
        self.disable_entries()
        self.pause_bt['text'] = "⏸"
        self.update_timer()

    def end_timer(self):
        """Stops and resets the timer completely."""
        self.timer_running = False
        self.Duration = 0
        self.last_saved_t = 0
        self.set_time("00", "00", "00")
        self.enable_entries()
        self.pause_bt['text'] = "▶"
        self.status_label['text'] = f"Saved time:{self.last_saved_t}"

    def restart(self):
        """Resets the timer back to the original starting time."""
        self.timer_running = False
        self.Duration = self.last_saved_t
        
        new_H = self.Duration // 3600
        new_M = (self.Duration // 60) % 60
        new_S = self.Duration % 60
        
        self.set_time(f"{new_H:02d}", f"{new_M:02d}", f"{new_S:02d}")
        self.enable_entries()
        self.pause_bt['text'] = "▶"
    
    def disable_entries(self):
        self.secondEntry['state'] = "readonly"
        self.minuteEntry['state'] = "readonly"
        self.year_entry['state'] = "readonly"
    
    def enable_entries(self):
        self.secondEntry['state'] = "normal"
        self.minuteEntry['state'] = "normal"
        self.year_entry['state'] = "normal"


if __name__ == "__main__":
    root = tk.Tk()
    app = Todo_app(root)
    root.mainloop()



