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
        todo_tab = ttk.Frame(self.tabs)
        timer_tab = ttk.Frame(self.tabs)

        self.tasks = []

        self.tabs.add(dashboard_tab, text="Dashboard")
        self.tabs.add(todo_tab, text="To-Do List")
        self.tabs.add(timer_tab, text="Pomodoro Timer")
        self.tabs.pack(expand=True, fill="both")

        #Dash Board
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
        
        #Tasks List

        #Pomodoro Timer

    def add(self):
        pass
    
    def remove(self):
        pass

    def clear_all(self):
        pass

    def load(self):
        pass

    def export(self):
        pass

    def search(self):
        pass

    def sort(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = Todo_app(root)
    root.mainloop()