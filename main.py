"""Something here"""
import tkinter as tk
from tkinter import ttk, messagebox as mb, filedialog
import csv
from datetime import datetime, date

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
        self.tabs.add(self.timer_tab, text="Pomodoro Timer")
        self.tabs.pack(expand=True, fill="both")
        self.tabs.bind("<<NotebookTabChanged>>", self.calculate_percent)

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.create_dashboard()
        self.create_task_manager()
        self.create_timer()

        self.load(self.PATH)
        self.sort(event=None)

    def create_dashboard(self):
        #Dash Board
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
        self.p_label.pack()

        progress = ttk.Progressbar(self.dashboard_tab, 
                                    orient="horizontal", 
                                    length=850, 
                                    mode='determinate'
                                    )
        progress.pack(padx=5)
    
    def create_task_manager(self):
        """This method create all of the widget inside the task manager."""
        top = ttk.LabelFrame(self.todo_tab, text="➕ Add New Task")
        top.pack(fill="x", padx=10, pady=5)

        ttk.Label(top, text="Title").grid(row=0, column=0, padx=5)
        self.title_entry = ttk.Entry(top, width=30)
        self.title_entry.grid(row=0, column=1, padx=5)
        
        # Priority selector
        ttk.Label(top, text="Priority").grid(row=0, column=2, padx=5)
        self.priority_entry = ttk.Combobox(top, 
                                           values=['Low', 'Medium', 'High'],
                                           state='readonly',
                                           )
        self.priority_entry.grid(row=0, column=3, padx=5)
        self.priority_entry.current(0)
        self.priority_entry.bind("<<ComboboxSelected>>", self.combo_colour)
        style_name_1 = f"Combo1_{id(self.priority_entry)}.TCombobox"
        self.priority_entry.configure(style=style_name_1)

        # Due Date enter
        ttk.Label(top, text="Due Date").grid(row=1, column=0, padx=5)
        self.date_entry = ttk.Entry(top, width=30)
        self.date_entry.grid(row=1, column=1, padx=5)
        
        self.add_bt = ttk.Button(top, text="✅Add Task", command=self.add)
        self.add_bt.grid(row=1, column=3, padx=5)
        
        button_bar = ttk.Frame(self.todo_tab)
        button_bar.pack(fill="x", padx=10, pady=5)

        delete_bt = ttk.Button(button_bar, text="✖️Delete"
                               ,command=self.remove
                               )
        delete_bt.pack(side="left", padx=10)

        delete_all_bt = ttk.Button(button_bar, text="⚠Delete All",
                                   command=self.clear_all
                                   )
        delete_all_bt.pack(side="left", padx=10)
        
        SORT_CATE = ['Name', 'Date', 'Highest Priority', 'Lowest Priority', 
                    'Completed', 'Incomplete', 'Overdue'
                    ]
        ttk.Label(button_bar, text="Sort by:").pack(side="left")
        self.sort_bar = ttk.Combobox(button_bar, values=SORT_CATE,
                                      state="readonly",
                                     )
        self.sort_bar.pack(side="left", padx=10)
        self.sort_bar.current(0)
        self.sort_bar.bind("<<ComboboxSelected>>", self.sort)

        load_bt = ttk.Button(button_bar, text="Import⬇️",
                            command=self.load
                            ).pack(side="left", padx=10)
            
        export_bt = ttk.Button(button_bar, text="Export⬆️", 
                                command=self.export
                                ).pack(side="left", padx=10)

        table_cols = ('Title', 'Due Date', 'Priority', 'State')
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
    
    def create_timer(self):
        #Pomodoro Timer
        tk.Label(self.timer_tab, text="25:00", 
                 font=("Segoe UI", 60, "bold"),
                 borderwidth=2, relief="solid"
                 ).place(anchor="center", x=450, y=75)

        preset_short = tk.Radiobutton(self.timer_tab, text="Short",
                                      value="Short", indicatoron=0,
                                      height=2, width=9,
                                      background="light blue", 
                                        borderwidth=2, relief="solid")
        preset_short.place(anchor="center", x=275, y=175)

        preset_long = tk.Radiobutton(self.timer_tab, text="Long",
                                      value="Long", indicatoron=0,
                                      background="light blue", 
                                      height=2, width=9,
                                        borderwidth=2, relief="solid")
        preset_long.place(anchor="center", x=450, y=175)

        custom = tk.Radiobutton(self.timer_tab, text="Custom",
                                      value="Custom", indicatoron=0,
                                      height=2, width=9,
                                      background="light blue", 
                                        borderwidth=2, relief="solid")
        custom.place(anchor="center", x=675, y=175)

        pause_bt = ttk.Button(self.timer_tab, text="⏸️", command=self.pause)
        pause_bt.place(anchor="center", x=450, y=275)

        skip_bt = ttk.Button(self.timer_tab, text="⏭", command=self.skip)
        skip_bt.place(anchor="center", x=675, y=275)

        restart_bt = ttk.Button(self.timer_tab, text="⟲", command=self.restart)
        restart_bt.place(anchor="center", x=275, y=275)

        status_label = tk.Label(self.timer_tab, text="Status: On Break")
        status_label.place(anchor="center", x=450, y=375)

    def refresh(self):
        """This method updates the table rows by removing everything
        then reinsert items from the list.""" 
        # Update table
        rows = self.table.get_children()
        for row in rows:
            self.table.delete(row)
        for i in range(len(self.tasks)):
            task = self.tasks[i]
            value=(task["title"], task["due"], task["priority"], task["state"])
            tag=(task["priority"] if task["state"] == "☐" else "Done")
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


    def calculate_percent(self, event = None):
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
            completed_percent = int(100 * completed / (incompleted + completed))
            self.p_label['text'] = f"{completed_percent}% Completed"

    def add(self):
        """The method get the title an due date
        then validate the data, added the new task to the 
        list above and refresh it"""
        title = self.title_entry.get()
        title.strip()

        due_date = self.date_entry.get()
        due_date.strip()

        priority = self.priority_entry.get()

        if not title:
            mb.showerror("Missing input", "Title required")
            return
        
        if not due_date:
            mb.showerror("Missing Input", "No Due Date")
            return
        
        self.tasks.append({
            "title":    title,
            "due":   due_date,
            "priority": priority,
            "state": "☐"
            })
        
        self.refresh()
        self.date_entry.delete(0, tk.END)
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
        new_path = filedialog.asksaveasfilename(filetypes=[("CSV file","*.csv")])

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
            #'Date': (),
            'Highest Priority': (lambda task: p_order.index(task['priority']), 
                                 False
                                ),
            'Lowest Priority': (lambda task: p_order.index(task['priority']), 
                                True
                                ),
            'Completed': (lambda task: task['state'], True),
            'Incomplete': (lambda task: task['state'], False),
            #'Overdue': (),
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
            # prevent program from returning data of label column
            return
        
        else:
            for task in self.tasks:
                if task.get("id") == item:
                    if task["state"] == "☐":
                            task["state"] = "✅"
                    else:
                        task["state"] = "☐"

        self.refresh()    
        print("Marked done")
        
    def pause(self):
        print("pause")

    def skip(self):
        print("Skipped")

    def restart(self):
        print("Restart timer")


if __name__ == "__main__":
    root = tk.Tk()
    app = Todo_app(root)
    root.mainloop()



