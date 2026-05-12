"""Something here"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime, date

class Todo_app:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDoMate")
        self.root.geometry("900x550")

        self.tabs = ttk.Notebook(root)
        dashboard_tab = ttk.Frame(self.tabs)
        self.todo_tab = ttk.Frame(self.tabs)
        timer_tab = ttk.Frame(self.tabs)

        self.tasks = []

        self.tabs.add(dashboard_tab, text="Dashboard")
        self.tabs.add(self.todo_tab, text="To-Do List")
        self.tabs.add(timer_tab, text="Pomodoro Timer")
        self.tabs.pack(expand=True, fill="both")

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
        
        #Tasks List
        top = ttk.LabelFrame(self.todo_tab, text="➕ Add New Task")
        top.pack(fill="x", padx=10, pady=5)

        ttk.Label(top, text="Title").grid(row=0, column=0, padx=5)
        self.title_entry = ttk.Entry(top, width=30)
        self.title_entry.grid(row=0, column=1, padx=5)

        ttk.Label(top, text="Priority").grid(row=0, column=2, padx=5)
        self.priority_entry = ttk.Combobox(top, 
                                           values=['Low', 'Medium', 'High'],
                                           state="readonly"
                                           )
        self.priority_entry.grid(row=0, column=3, padx=5)
        self.priority_entry.current(1)

        ttk.Label(top, text="Due Date").grid(row=1, column=0, padx=5)
        self.date_entry = ttk.Entry(top, width=30)
        self.date_entry.grid(row=1, column=1, padx=5)

        self.add_bt = ttk.Button(top, text="✅Add Task", command=self.add)
        self.add_bt.grid(row=1, column=3, padx=5)
        
        button_bar = ttk.Frame(self.todo_tab)
        button_bar.pack(fill="x", padx=10, pady=5)

        delete_bt = ttk.Button(button_bar, text="Delete",command=self.remove).pack(side="left", padx=10)
        delete_all_bt = ttk.Button(button_bar, text="Delete All",command=self.clear_all).pack(side="left", padx=10)

        ttk.Label(button_bar, text="Sort by:").pack(side="left")
        self.filter_bt = ttk.Combobox(button_bar, values= ['Date', 'Priority'],
                                        state="readonly"
                                        )
        self.filter_bt.pack(side="left", padx=10)
        self.filter_bt.current(0)

        table_cols = ('Name', 'Due Date', 'Priority', 'State')
        self.table = ttk.Treeview(self.todo_tab, 
                                  columns= table_cols,
                                  show="headings",
                                  height=18)
        for column in table_cols:
            self.table.heading(column, text=column)
            self.table.column(column, anchor="center")
        self.table.pack(fill="both", expand=True, padx=10)

        # Colour code task based on priority
        self.table.tag_configure("High", background="red")
        self.table.tag_configure("Done", background="green")

        #Pomodoro Timer
        tk.Label(timer_tab, text="25:00", 
                 font=("Segoe UI", 60, "bold"),
                 borderwidth=2, relief="solid"
                 ).pack(pady=50, anchor="center")
        
        mid_frame = tk.Frame(timer_tab)
        mid_frame.pack(fill="both",padx=5)

        preset_short = tk.Radiobutton(mid_frame, text="Short",
                                      value="Short", indicatoron=0,
                                      height=2, width=9,
                                      background="light blue", 
                                        borderwidth=2, relief="solid")
        preset_short.grid(row=0 , column=0, sticky="w", padx= 90)

        preset_long = tk.Radiobutton(mid_frame, text="Long",
                                      value="Long", indicatoron=0,
                                      background="light blue", 
                                      height=2, width=9,
                                        borderwidth=2, relief="solid")
        preset_long.grid(row=0 , column=1, sticky="w", padx=90)

        custom = tk.Radiobutton(mid_frame, text="Custom",
                                      value="Custom", indicatoron=0,
                                      height=2, width=9,
                                      background="light blue", 
                                        borderwidth=2, relief="solid")
        custom.grid(row=0 , column=2, sticky="w", padx=90)

        pause_bt = ttk.Button(mid_frame, text="⏸️", command=self.pause)
        pause_bt.grid(row=1, column=0, padx=90, pady=5)

        skip_bt = ttk.Button(mid_frame, text="⏭", command=self.skip)
        skip_bt.grid(row=1, column=1, padx=90, pady=5)

        restart_bt = ttk.Button(mid_frame, text="⟲", command=self.restart)
        restart_bt.grid(row=1, column=2, padx=90, pady=5)



    def add(self):
        print("Add task")
    
    def remove(self):
        print("task removed")

    def clear_all(self):
        print("All tasks deleted")

    def load(self):
        pass

    def export(self):
        pass

    def search(self):
        pass

    def sort(self):
        pass

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