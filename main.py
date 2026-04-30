"""Something here"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime, date


root = tk.Tk()
tabs = ttk.Notebook(root)
dashboard_tab = ttk.Frame(tabs)
todo_tab = ttk.Frame(tabs)
timer_tab = ttk.Frame(tabs)

tabs.add(dashboard_tab, text="Dashboard")
tabs.add(todo_tab, text="To-Do List")
tabs.add(timer_tab, text="Pomodore Timer")
tabs.pack(expand=True, fill="both")


ttk.Label(
            dashboard_tab,
            text="📊 ToDoMate Dashboard",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=50)

ttk.Label(
            dashboard_tab,
            text="Organise tasks • Manage priorities • Export data",
            font=("Segoe UI", 12)
        ).pack()

root.mainloop()