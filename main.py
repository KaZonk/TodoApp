"""Something here"""
import tkinter as tk
from tkinter import ttk, messagebox as mb, filedialog
import csv
from datetime import datetime, date

class Todo_app:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDoMate")
        self.root.geometry("900x550")
        self.root.resizable(width=False, height=False)

        self.tabs = ttk.Notebook(root)
        dashboard_tab = ttk.Frame(self.tabs)
        self.todo_tab = ttk.Frame(self.tabs)
        timer_tab = ttk.Frame(self.tabs)

        self.tasks = []
        self.PATH = "todo_file.csv"

        self.tabs.add(dashboard_tab, text="Dashboard")
        self.tabs.add(self.todo_tab, text="To-Do List")
        self.tabs.add(timer_tab, text="Pomodoro Timer")
        self.tabs.pack(expand=True, fill="both")

        self.style = ttk.Style()
        self.style.theme_use('clam')

        #Dash Board
        ttk.Label(
                    dashboard_tab,
                    text="📊Dashboard",
                    font=("Segoe UI", 18, "bold")
                ).pack(pady=50)
        ttk.Label(
                    dashboard_tab,
                    text="X % completed",
                    font=("Segoe UI", 12)
                ).pack()

        progress = ttk.Progressbar(dashboard_tab, 
                                    orient="horizontal", 
                                    length=850, 
                                    mode='determinate'
                                    )
        progress.pack(padx=5)
        
        #Tasks Manager
        top = ttk.LabelFrame(self.todo_tab, text="➕ Add New Task")
        top.pack(fill="x", padx=10, pady=5)

        ttk.Label(top, text="Title").grid(row=0, column=0, padx=5)
        self.title_entry = ttk.Entry(top, width=30)
        self.title_entry.grid(row=0, column=1, padx=5)

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
        
        sort_cat = ['Date', 'Priority', 'Completed', 'Incomplete', 'Overdue']
        ttk.Label(button_bar, text="Sort by:").pack(side="left")
        self.filter_bt = ttk.Combobox(button_bar, values=sort_cat,
                                      state="readonly",
                                     )
        self.filter_bt.pack(side="left", padx=10)
        self.filter_bt.current(0)

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
        self.table.bind("<Double-1>", self.mark_done)
        # Colour code task based on priority
        self.table.tag_configure("Medium", background="yellow")
        self.table.tag_configure("High", background="orange")
        self.table.tag_configure("Done", background="#94C748")

        #Pomodoro Timer
        tk.Label(timer_tab, text="25:00", 
                 font=("Segoe UI", 60, "bold"),
                 borderwidth=2, relief="solid"
                 ).place(anchor="center", x=450, y=75)

        preset_short = tk.Radiobutton(timer_tab, text="Short",
                                      value="Short", indicatoron=0,
                                      height=2, width=9,
                                      background="light blue", 
                                        borderwidth=2, relief="solid")
        preset_short.place(anchor="center", x=275, y=175)

        preset_long = tk.Radiobutton(timer_tab, text="Long",
                                      value="Long", indicatoron=0,
                                      background="light blue", 
                                      height=2, width=9,
                                        borderwidth=2, relief="solid")
        preset_long.place(anchor="center", x=450, y=175)

        custom = tk.Radiobutton(timer_tab, text="Custom",
                                      value="Custom", indicatoron=0,
                                      height=2, width=9,
                                      background="light blue", 
                                        borderwidth=2, relief="solid")
        custom.place(anchor="center", x=675, y=175)

        pause_bt = ttk.Button(timer_tab, text="⏸️", command=self.pause)
        pause_bt.place(anchor="center", x=450, y=275)

        skip_bt = ttk.Button(timer_tab, text="⏭", command=self.skip)
        skip_bt.place(anchor="center", x=675, y=275)

        restart_bt = ttk.Button(timer_tab, text="⟲", command=self.restart)
        restart_bt.place(anchor="center", x=275, y=275)

        status_label = tk.Label(timer_tab, text="Status: On Break")
        status_label.place(anchor="center", x=450, y=375)

        self.load(self.PATH)

    def refresh(self):

        rows = self.table.get_children()
        for row in rows:
            self.table.delete(row)
        for i in range(len(self.tasks)):
            t = self.tasks[i]
            row_id = self.table.insert(
                "", "end",
                values=(t["title"], t["due"], t["priority"], t["state"]),
                tags=(t["priority"] if t["state"] == "☐" else "Done")
            )
            self.tasks[i]["id"] = row_id

        fieldnames = ('due', 'title', 'id', 'priority', 'state')
        with open(self.PATH, "w", newline='', encoding='utf-8') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(fieldnames)
            for u in self.tasks:
                val = (u['due'], u['title'], u['id'], u['priority'], u['state'])
                print(val)
                csv_writer.writerow(val)

        print("Refreshed")

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
            print("All tasks deleted")
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
        the path and take in the information from the provided file"""
        if Path is None:
            Path = filedialog.askopenfilename( filetypes= (("text files","*.csv"),
                                                ("all files","*.*")))
            # if no file given: return

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
        except (TypeError, FileNotFoundError) as e:
            print(f"Error: Could not open file '{Path}'. ({e})")
            return
            

    def export(self):
        for stuff in self.tasks:
            print(stuff)

    def sort(self):
        pass

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


    """
        with open(self.PATH, mode = "r", encoding='utf-8') as f:
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
         """       