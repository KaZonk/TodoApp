"""This is a to-do program to let student keep track of their task."""

# Libraries:
import tkinter as tk
from tkinter import ttk, messagebox as mb, filedialog
import csv
from datetime import datetime as dt, date, timedelta


class TodoApp:
    def __init__(self, root):
        """Intialise the root, set up the window's geometry and tabs."""
        self.root = root
        self.root.title("ToDoApp")
        self.root.geometry("900x550")
        self.root.resizable(width=False, height=False)

        # Create the 3 tabs.
        self.tabs = ttk.Notebook(root)
        self.dashboard_tab = ttk.Frame(self.tabs)
        self.todo_tab = ttk.Frame(self.tabs)
        self.timer_tab = ttk.Frame(self.tabs)

        self.tasks = []
        self.PATH = "todo_file.csv"
        
        # Give a task name and pack it.
        self.tabs.add(self.dashboard_tab, text="Dashboard")
        self.tabs.add(self.todo_tab, text="To-Do List")
        self.tabs.add(self.timer_tab, text="Timer")
        self.tabs.pack(expand=True, fill="both")
        self.tabs.bind("<<NotebookTabChanged>>", self.calc_percent)

        # Intitalising clam style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure(
                             'custom.Horizontal.TProgressbar', 
                             background='#18bc9c', 
                             troughcolor='#ecf0f1'
                            )

        # Create the UI, splitted into three methods.
        self.create_dashboard()
        self.create_task_manager()
        self.create_timer()

        # Load in saved tasks and sort it in default order.
        self.load(self.PATH)
        self.sort(event=None)

    def create_dashboard(self):
        """Create the dashboard.
        It contain the progress bar with percentage of tasks completed.
        """
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
        # Define values for combo-boxes and treeview.
        SORT_CATE = [
                'Name', 'Due Date', 'Highest Priority', 'Lowest Priority', 
                'Completed', 'Incomplete'
                    ]
        DAYS = [f"{d:02d}" for d in range(1, 31+1)]  # day 1-31.
        MONTH = [f"{m:02d}" for m in range(1, 12+1)]  # month 1-12.
        P_ORDER = ['Low', 'Medium', 'High']
        table_cols = ('Title', 'Due Date', 'Priority', 'State')
        today = dt.now()

        top = ttk.LabelFrame(self.todo_tab, text="➕ Add New Task")
        top.pack(fill="x", padx=10, pady=5)
        
        # Title entry
        ttk.Label(top, text="Title").grid(row=0, column=0, padx=5)
        self.title_entry = ttk.Entry(top, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Priority selector with a unique style ID.
        ttk.Label(top, text="Priority").grid(row=0, column=2, padx=5)
        self.priority_entry = ttk.Combobox(top, 
                                           values=P_ORDER,
                                           state='readonly',
                                           )
        self.priority_entry.grid(row=0, column=3, padx=5, pady=5)
        self.priority_entry.current(0)
        self.priority_entry.bind("<<ComboboxSelected>>", self.remove_highlight)
        style_name_1 = f"Combo1_{id(self.priority_entry)}.TCombobox"
        self.priority_entry.configure(style=style_name_1)
        
        # Due Date entries allow the user to pick dates in dd-MM-YYYY.
        ttk.Label(top, text="Due Date:").grid(row=1, column=0, padx=5)
        due_date_frame = ttk.Frame(top)
        due_date_frame.grid(row=1, column=1, padx=5, pady=5)

        # Date entry, default value set as today's date.
        ttk.Label(due_date_frame, text="DD:").pack(side="left", padx=5)
        self.date_entry = ttk.Combobox(due_date_frame, 
                                       values=DAYS,
                                       width=3)
        self.date_entry.pack(side="left", padx=5, pady=5)
        self.date_entry.set(today.strftime("%d"))
        self.date_entry.bind("<<ComboboxSelected>>", self.remove_highlight)
        
        # Month Entry, default value set as current month.
        ttk.Label(due_date_frame, text="MM:").pack(side="left", padx=5)
        self.month_entry = ttk.Combobox(due_date_frame, 
                                       values=MONTH,
                                       width=3)
        self.month_entry.pack(side="left", padx=5, pady=5)
        self.month_entry.set(today.strftime("%m"))
        self.month_entry.bind("<<ComboboxSelected>>", self.remove_highlight)
        
        # Year entry, default value set as current year.
        ttk.Label(due_date_frame, text="YYYY:").pack(side="left", padx=5)
        self.year_entry = ttk.Entry(due_date_frame,
                                    width=6)
        self.year_entry.pack(side="left", padx=5, pady=5)
        self.year_entry.insert(0, today.strftime("%Y"))

        self.add_bt = ttk.Button(top, text="✅Add Task", command=self.add)
        self.add_bt.grid(row=1, column=3, padx=5, pady=5)
        
        # delete, sort, import, export and configuring the treeview(table).
        button_bar = ttk.Frame(self.todo_tab)
        button_bar.pack(fill="x", padx=10, pady=5)
        
        delete_bt = ttk.Button(button_bar, text="✖️Delete",
                               command=self.remove
                              )
        delete_bt.pack(side="left", padx=10, pady=5)

        delete_all_bt = tk.Button(button_bar, text="⚠Delete All",
                                  command=self.clear_all
                                 )
        delete_all_bt.pack(side="right", padx=10, pady=5)
        
        # Sorting method
        ttk.Label(button_bar, text="Sort by:").pack(side="left")
        self.sort_bar = ttk.Combobox(button_bar, values=SORT_CATE,
                                    state="readonly"
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

        # User can double click to mark a task done.
        self.table.bind("<Double-1>", self.mark_done)

        # Colour code task based on priority.
        self.table.tag_configure("Medium", background="yellow")
        self.table.tag_configure("High", background="orange")
        self.table.tag_configure("Done", background="#94C748")
        self.table.tag_configure("Overdue", background="red")
    
    def create_timer(self):
        """Create timer tab.
        Help the user focus on completing their tasks.
        """
        # Defining timing varibles:
        FONT = ("Segoe UI", 60, "bold")
        self.hour=tk.StringVar(value="00")
        self.minute=tk.StringVar(value="00")
        self.second=tk.StringVar(value="00")
        self.timer_running = False
        self.Duration = 0
        self.last_saved_t = 0

        self.hourEntry= ttk.Entry(
                                self.timer_tab, width=3, font=FONT, 
                                textvariable=self.hour
                                )
        self.hourEntry.place(x=210,y=75, width=120)

        ttk.Label(self.timer_tab, width=3, 
                  font=FONT, text=":").place(x=350, y=75)

        self.minuteEntry= ttk.Entry(
                               self.timer_tab, width=3, font=FONT,
                               textvariable=self.minute
                               )
        self.minuteEntry.place(x=390, y=75, width=120)

        ttk.Label(self.timer_tab, width=3, 
                  font=FONT, text=":").place(x=530,y=75)

        self.secondEntry= ttk.Entry(
                               self.timer_tab, width=3, font=FONT, 
                               textvariable=self.second
                               )
        self.secondEntry.place(x=570, y=75, width=120)

        # The pause button should have it's text between ▶ and ⏸️ symbols.
        self.pause_bt = ttk.Button(
                                   self.timer_tab, text="Start▶", 
                                   command=self.pause
                                  )
        self.pause_bt.place(anchor="center", x=450, y=300)

        skip_bt = ttk.Button(
                            self.timer_tab, text="Skip⏭", 
                            command=self.end_timer
                            )
        skip_bt.place(anchor="center", x=625, y=300)

        restart_bt = ttk.Button(
                                self.timer_tab, text="Restart⟲", 
                                command=self.restart
                                )
        restart_bt.place(anchor="center", x=275, y=300)

        self.status_label = tk.Label(
                                self.timer_tab, 
                                text=("Timer not in progress")
                                )
        self.status_label.place(anchor="center", x=450, y=400)

    def refresh(self):
        """Updates the table and CSV file.
        The method remove everything in table,
        and reinstate them from the updated tasks list.
        Write the CSV file with values in the tasks list.
        """ 
        current_date = dt.now().date()

        # Update table
        rows = self.table.get_children()
        for row in rows:
            self.table.delete(row)
        for i in range(len(self.tasks)):
            task = self.tasks[i]
            value=(task['title'], task['due'], task['priority'], task['state'])
            # Convert due_date to datetime-type object.
            due_date = dt.strptime(task['due'], "%d-%m-%Y").date() 
            if task['state'] == "✅":
                tag='Done'
            elif due_date < current_date:            
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
                val = (
                        task['due'], task['title'], task['id'], 
                        task['priority'], task['state']
                      )
                csv_writer.writerow(val)

    def calc_percent(self, event=None):
        """Calculate the percentage of completed against incompleted tasks."""
        event.widget.focus_set()  # Remove highlight when switching tabs.
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
                completed_percent = int(100 
                                        * completed 
                                        / (incompleted + completed))
            except ZeroDivisionError:
                self.p_label['text'] = "0% tasks completed"
                self.progress['value'] = 0
            else:
                self.p_label['text'] = f"{completed_percent}% Completed"
                self.progress['value'] = completed_percent
    
    def add(self):
        """Gather values and add tasks to tasks list.

        Method get title, due date and priority, validate them and,
        add them to the tasks list.
        """
        title = self.title_entry.get()
        priority = self.priority_entry.get()
        title.strip()
        MAX_FUTURE_DATE = 360
        d = self.date_entry.get()
        M = self.month_entry.get()
        Y = self.year_entry.get()
        due_date = f"{d}-{M}-{Y}"
        today = dt.now().date()
        max_due_date = today + timedelta(days=MAX_FUTURE_DATE)

        # Validate datetime and title.
        try:
            parsed_due_date = dt.strptime(due_date, "%d-%m-%Y").date() 

            validator = {
                (not title): ("Missing Input", "Please input a title"),
                (parsed_due_date < today): (
                                        "Error", 
                                        "Cannot input due date in the past"
                                           ),
                (parsed_due_date > max_due_date): (
                                "Date too Far", 
                                f"This due date exceeds {MAX_FUTURE_DATE} days"
                                " in the future, please input a sooner date."
                                                  )
            }

            # Check for error by finding what makes if-statement true, if any.
            if error := validator.get(True):
                return mb.showerror(*error)

        except ValueError as e:
            # Return incorrect datetime format.
            return mb.showerror("Something went wrong", str(e))
        
        # Add it to the tasks list.
        self.tasks.append(
            {
            "title":    title,
            "due":   due_date,
            "priority": priority,
            "state": "☐"
            }
        )
        
        self.refresh()  # Refresh table and CSV file.
        self.title_entry.delete(0, tk.END)  # Clear title.

    def remove(self):
        """Remove selected task from tasks list.

        The method get the ID of the selected tasks.
        Ask for confirmation if the user is deleting more than 3 tasks
        then remove it from the table
        """
        selected_task = self.table.selection()
        no_selected = len(self.table.selection())
        
        # Ask for confirmation if user delete more than 3 tasks simultaneously.
        if no_selected >= 3:
            message = ("You are deleting 3 tasks or more, "
                        "Are you sure you want to proceed?")
            if not mb.askyesno("Warning", message):
                return
        
        # Delete tasks.
        if no_selected > 0:
            for item in selected_task:
                    for task in self.tasks:
                        if task.get("id") == item:
                            self.tasks.remove(task)
            self.refresh() 
        
        

    def clear_all(self):
        """Remove everything from tasks list and refresh."""
        if mb.askyesno("Warning, this action cannot be undo!",
                        "Are you sure you want to DELETE ALL existing tasks?"):
            self.tasks.clear()
            self.refresh()
        else:
            return
        
    def remove_highlight(self, event):
        """Remove Hightlight off combo box.
        Map styling colour to combo box (Currently only used for priority_entry)
        """
        event.widget.selection_clear()
        current = event.widget.get()
        style_name = event.widget.cget("style")
        if current == "High":
            bg_color = "orange"
        elif current == "Medium":
            bg_color = "yellow"
        else:
            bg_color = "white"
        
        self.style.map(style_name, 
                    fieldbackground=[('readonly', bg_color)],
                    background=[('readonly', bg_color)],
                    foreground=[('readonly', 'black')]
                    )

    def load(self, Path=None):
        """Open the file provided and copy the data into the tasks list.

        Args:
            File path. If it's not provided then the user is asked for one.

        Return:
            Open the file , then take it's information and write it into the
            tasks list. Display messagebox if there's an error
        """
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
                        self.tasks.append(
                                        {"title":  line['title'],
                                        "due":   line['due'],
                                        "id":     task_id,
                                        "priority": line['priority'],
                                        "state": line['state']
                                        }
                                        )
                self.refresh()
        except (TypeError, FileNotFoundError, KeyError) as e:
            mb.showerror("Error", 
                         f"Error: Could not open file '{Path}'. ({e})"
                        )
            return
            
    def export(self):
        """Export a CSV file to a location of user's choice."""
        new_path = filedialog.asksaveasfilename(
                                            defaultextension=".csv",
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
                    values = (
                              task['due'], task['title'], task['id'], 
                              task['priority'], task['state']
                             )
                    csv_writer.writerow(values)

    def sort(self, event):
        """Sort tasks based on category.
        Sort the task with the dictionary rules."""
        p_order = ['High', 'Medium', 'Low']
        sorting_rules = {
            # Category: (sorting key, true/false to reverses order)
            'Name': (lambda task: task['title'], False),
            'Due Date': (lambda task: dt.strptime(task['due'], '%d-%m-%Y'),
                        False
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
            self.tasks = sorted(self.tasks, key=key_function, 
                                reverse=should_reverse)
        self.refresh()

    def mark_done(self, event):
        """Mark the task as completed.
        Find the task's ID and then give it the tick."""
        try:
            item = self.table.selection()[0]
        except IndexError:
            # prevent program from returning data of header column.
            return
        else:
            for task in self.tasks:
                if task.get("id") == item:
                    task["state"] = "✅" if task["state"] == "☐" else "☐"
        self.refresh()    

    def update_timer(self):
        """Update the timer every 1 second."""
        if not self.timer_running:
            return

        self.Duration -= 1

        if self.Duration < 0:
            # end timer when duration is zero.
            self.end_timer()
            mb.showinfo("Countdown Timer", "Time is up!")
            return

        # Calculate remaining time.
        new_hour, new_min, new_sec = self.time_calc(self.Duration)

        # Update GUI.
        self.set_time(f"{new_hour:02d}", f"{new_min:02d}", f"{new_sec:02d}")
        in_progress_message = "Timer in progress, wait for it to finish " \
                            "OR skip to be able to input new timing."
        self.status_label['text'] = in_progress_message
        
        # Schedule next update(1000ms or 1 second).
        self.root.after(1000, self.update_timer)
        

    def pause(self):
        """Start, pause or continue the timer based on it's current state."""
        # Case 1: Timer is running, Pause it.
        if self.timer_running:
            self.timer_running = False
            self.pause_bt['text'] = "▶"
            return

        # Case 2: Timer is finished, start a new timer.
        if self.Duration == 0:
            H = self.hour.get()
            M = self.minute.get()
            S = self.second.get()
            input_length = (len(str(H)), len(str(M)), len(str(S)))
            # Validate length of timer input to 2 character.
            if max(input_length) > 2:
                timer_mess = "Error, you cannot enter more than two characters"
                self.set_time() # reset to 00:00:00.
                mb.showerror("Input Error", timer_mess)
                return
            try:
                self.Duration = (3600 * int(H) 
                                + 60 * int(M) 
                                + int(S)
                                )
                self.last_saved_t = self.Duration 
            except ValueError:
                mb.showerror("Error", "Please enter valid numbers")
                return

            if self.Duration <= 0:
                mb.showwarning("Warning", "Please set a time greater than 0")
                return

        # Case 3: Resuming a paused timer OR successfully started a new one.
        self.timer_running = True
        self.disable_entries()
        self.pause_bt['text'] = "⏸"
        self.update_timer()

    def end_timer(self):
        """Stops and resets the timer completely."""
        self.timer_running = False
        self.Duration = 0
        self.set_time("00", "00", "00")
        self.enable_entries()
        self.pause_bt['text'] = "▶"
        self.status_label['text'] = "Timer not in progress"

    def restart(self):
        """Resets the timer back to the original starting time."""
        self.timer_running = False
        self.Duration = self.last_saved_t
        new_h, new_m, new_s = self.time_calc(self.Duration)
        self.set_time(f"{new_h:02d}", f"{new_m:02d}", f"{new_s:02d}")
        self.pause_bt['text'] = "▶"
    
    def disable_entries(self):
        """Prevent user from inputting time."""
        self.secondEntry['state'] = "readonly"
        self.minuteEntry['state'] = "readonly"
        self.hourEntry['state'] = "readonly"
    
    def enable_entries(self):
        """Enable user to input time."""
        self.secondEntry['state'] = "normal"
        self.minuteEntry['state'] = "normal"
        self.hourEntry['state'] = "normal"
    
    def time_calc(self, total_t=int):
        """Calculate the amount of hour, minute, second to display.

        Arg: 
            Integer number of seconds.
        
        Return:
            hour, minute, and second.
        """
        new_hour = total_t // 3600
        new_minute = (total_t // 60) % 60
        new_second = total_t % 60
        return new_hour, new_minute, new_second 

    def set_time(self, hour="00", minute="00", second="00"):
        """This method set the time in the stringVar, default is 00"""
        self.hour.set(hour)
        self.minute.set(minute)
        self.second.set(second)
    
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
