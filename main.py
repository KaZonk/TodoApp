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

        progress = ttk.Progressbar(dashboard_tab, 
                                    orient="horizontal", 
                                    length=850, 
                                    mode='determinate'
                                    )
        progress.pack(padx=5)
        
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

        delete_bt = ttk.Button(button_bar, text="✖️Delete",command=self.remove)
        delete_bt.pack(side="left", padx=10)

        delete_all_bt = ttk.Button(button_bar, text="⚠Delete All",command=self.clear_all)
        delete_all_bt.pack(side="left", padx=10)

        ttk.Label(button_bar, text="Sort by:").pack(side="left")
        self.filter_bt = ttk.Combobox(button_bar, values= ['Date', 'Priority'],
                                      state="readonly"
                                     )
        self.filter_bt.pack(side="left", padx=10)
        self.filter_bt.current(0)

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
        self.table.tag_configure("High", background="red")
        self.table.tag_configure("Done", background="green")

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

        status_label = tk.Label(timer_tab, text="Status: On Break").place(anchor="center", x=450, y=375)

    def refresh(self):
        tasks = self.table.get_children()
        for row in tasks:
            self.table.delete(row)

        items = self.tasks.copy()
        for t in items:
            self.table.insert(
                "", "end",
                values=(t["title"], t["due"], t["priority"], t["state"]),
                tags=(t["priority"])
            )
        print("Refreshed")

    def add(self):
        """The function get the title an due date
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
        print("Add task")

    
    def remove(self):
        print("task removed")

    def clear_all(self):

        if mb.askyesno("Warning!", "Are you sure you want to delete all tasks?"):
            self.tasks.clear
            self.refresh()
            print("All tasks deleted")
        else:
            return

        

    def load(self):
        pass

    def export(self):
        pass

    def sort(self):
        pass

    def mark_done(self, event):
        """This function that the ID of the selected
        children in the table, then check if the title matches
        If it does, then change the task state to done.
        If the task was already marked done, then this undo it"""
        
        for ITEM_ID in self.table.selection():
            for task in self.table:
                if ITEM_ID == self.table:
                    pass

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