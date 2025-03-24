import tkinter as tk
from tkinter import messagebox
import json
import os 

FILE = "todo.json"

def load_contacts():
    if os.path.exists(FILE):  # Check if file exists
        with open(FILE, "r") as f:
            try:
                data = f.read().strip()  # Read file content and remove whitespace
                return json.loads(data) if data else {}  # Load JSON only if file is not empty
            except json.JSONDecodeError:  # Handle corrupt JSON
                print("Warning: contacts.json is corrupted. Resetting file.")
                return {}  # Return empty dictionary instead of crashing
    return {}  # Return empty dictionary if file doesn't exist

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("To-Do List Manager")
        self.geometry("300x450")
        self.resizable(False, False)

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (MainScreen, addTask, removeTask, taskComplete, viewTask):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainScreen)

    def show_frame(self, screen):
        frame = self.frames[screen]

        if isinstance(frame, (taskComplete, viewTask, removeTask)):
            frame.load_task()

        frame.tkraise()

class MainScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        container = tk.Frame(self)
        container.grid(row=0, column=0)

        label = tk.Label(self, text="Main Screen", font=("Arial", 16), anchor="center", justify="center")
        label.grid(row=0, column=0, pady=20)

        button1 = tk.Button(self, text="Add Task", command=lambda: controller.show_frame(addTask))
        button1.grid(row=1, column=0, pady=5)

        button2 = tk.Button(self, text="Remove Task", command=lambda: controller.show_frame(removeTask))
        button2.grid(row=2, column=0, pady=5)

        button3 = tk.Button(self, text="Task Complete?", command=lambda: controller.show_frame(taskComplete))
        button3.grid(row=3, column=0, pady=5)
        
        button4 = tk.Button(self, text="View Task", command=lambda: controller.show_frame(viewTask))
        button4.grid(row=4, column=0, pady=5)

        container.place(relx=0.5, rely=0.5, anchor="center")

class addTask(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Add Task", font=("Arial", 16), anchor="center", justify="center")
        label.pack(pady=20)

        add_label = tk.Label(self, text="Task:")
        add_label.pack(pady=5)

        self.add_entry = tk.Entry(self)
        self.add_entry.pack(pady=5)

        add_button = tk.Button(self, text="Add Task", command=self.addTask)
        add_button.pack(pady=5)

        button = tk.Button(self, text="Back", command=lambda: controller.show_frame(MainScreen))
        button.pack(pady=10)

    def addTask(self):
        task = self.add_entry.get().strip()

        try:
            with open(FILE, "r") as f:
                ctask = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            ctask = {}

        if task:
            ctask[task] = False
            with open(FILE, "w") as f:
                json.dump(ctask, f, indent=4)
            
            messagebox.showinfo("Success", "Task Successfully Added!")
            self.controller.show_frame(MainScreen)
        else:
            messagebox.showwarning("Warning", "Task Cannot be empty.")
        
class removeTask(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Remove Task", font=("Arial", 16), anchor="center", justify="center")
        label.pack(pady=20)

        self.task_list = tk.Listbox(self, width=50, height=10)
        self.task_list.pack(pady=10)

        self.load_task()  # Load existing tasks into the listbox

        remove_button = tk.Button(self, text="Remove Selected Task", command=self.remove_selected_task)
        remove_button.pack(pady=5)

        button = tk.Button(self, text="Back", command=lambda: controller.show_frame(MainScreen))
        button.pack(pady=10)

    def load_task(self):
        """Loads tasks from JSON and populates the listbox"""
        self.task_list.delete(0, tk.END)  # Clear the listbox

        if os.path.exists(FILE):
            try:
                with open(FILE, "r") as f:
                    tasks = json.load(f)
                    if isinstance(tasks, dict):
                        for task in tasks.keys():
                            self.task_list.insert(tk.END, task)
                    else:
                        print("⚠ Warning: tasks.json is not formatted correctly. Resetting file.")
            except json.JSONDecodeError:
                print("⚠ Warning: tasks.json is corrupted. Resetting file.")

    def remove_selected_task(self):
        """Removes the selected task from JSON file"""
        selected_index = self.task_list.curselection()
        
        if not selected_index:
            messagebox.showwarning("Warning", "No task selected.")
            return
        
        selected_task = self.task_list.get(selected_index)

        # Load current tasks from file
        try:
            with open(FILE, "r") as f:
                tasks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            tasks = {}

        if selected_task in tasks:
            del tasks[selected_task]  # Remove task from dictionary
            
            # Overwrite the JSON file with updated tasks
            with open(FILE, "w") as f:
                json.dump(tasks, f, indent=4)

            messagebox.showinfo("Success", f"Task '{selected_task}' removed successfully!")

            self.task_list.delete(selected_index)  # Remove from UI
            self.controller.frames[viewTask].load_task()  # Refresh the View Task screen
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Remove Task", font=("Arial", 16), anchor="center", justify="center")
        label.pack(pady=20)

        self.task_list = tk.Listbox(self, width=50, height=10)
        self.task_list.pack(pady=10)

        self.load_task()

        remove_button = tk.Button(self, text="Remove Selected Task", command=self.remove_selected_task)
        remove_button.pack(pady=5)

        button = tk.Button(self, text="Back", command=lambda: controller.show_frame(MainScreen))
        button.pack(pady=10)

    def load_task(self):
        self.task_list.delete(0, tk.END) 

        if os.path.exists(FILE):
            try:
                with open(FILE, "r") as f:
                    tasks = json.load(f)
                    if isinstance(tasks, dict):
                        for task in tasks.keys():
                            self.task_list.insert(tk.END, task)
                    else:
                        print("⚠ Warning: tasks.json is not formatted correctly. Resetting file.")
            except json.JSONDecodeError:
                print("⚠ Warning: tasks.json is corrupted. Resetting file.")

    def remove_selected_task(self):
        selected_index = self.task_list.curselection()
        
        if not selected_index:
            messagebox.showwarning("Warning", "No task selected.")
            return
        
        selected_task = self.task_list.get(selected_index)

        try:
            with open(FILE, "r") as f:
                tasks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            tasks = {}

        if selected_task in tasks:
            del tasks[selected_task] 

            with open(FILE, "w") as f:
                json.dump(tasks, f, indent=4)

            messagebox.showinfo("Success", f"Task '{selected_task}' removed successfully!")

            self.task_list.delete(selected_index)
            self.controller.frames[viewTask].load_task()

class taskComplete(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Mark Task Complete", font=("Arial", 16), anchor="center", justify="center")
        label.pack(pady=20)

        self.task_list = tk.Listbox(self, width=50, height=10)
        self.task_list.pack(pady=10)

        self.load_task()  # Load tasks into the listbox

        complete_button = tk.Button(self, text="Toggle Completion", command=self.mark_task_complete)
        complete_button.pack(pady=5)

        button = tk.Button(self, text="Back", command=lambda: controller.show_frame(MainScreen))
        button.pack(pady=10)

    def load_task(self):
        """Loads tasks from JSON and populates the listbox with their completion status"""
        self.task_list.delete(0, tk.END)  # Clear the listbox

        if os.path.exists(FILE):
            try:
                with open(FILE, "r") as f:
                    tasks = json.load(f)
                    if isinstance(tasks, dict):
                        for task, status in tasks.items():
                            status_text = "✓" if status else "✗"
                            self.task_list.insert(tk.END, f"{status_text} {task}")
                    else:
                        print("⚠ Warning: tasks.json is not formatted correctly. Resetting file.")
            except json.JSONDecodeError:
                print("⚠ Warning: tasks.json is corrupted. Resetting file.")

    def mark_task_complete(self):
        """Toggles the completion status of the selected task"""
        selected_index = self.task_list.curselection()
        
        if not selected_index:
            messagebox.showwarning("Warning", "No task selected.")
            return
        
        selected_task = self.task_list.get(selected_index)
        task_name = selected_task[2:]  # Remove the ✓ or ✗ symbol

        # Load current tasks from file
        try:
            with open(FILE, "r") as f:
                tasks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            tasks = {}

        if task_name in tasks:
            tasks[task_name] = not tasks[task_name]  # Toggle the completion status
            
            # Save the updated dictionary back to the file
            with open(FILE, "w") as f:
                json.dump(tasks, f, indent=4)

            new_status = "completed" if tasks[task_name] else "not completed"
            messagebox.showinfo("Success", f"Task '{task_name}' marked as {new_status}.")

            self.load_task()  # Refresh the listbox immediately
            self.controller.frames[viewTask].load_task()  # Refresh the View Task screen
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Mark Task Complete", font=("Arial", 16), anchor="center", justify="center")
        label.pack(pady=20)

        self.task_list = tk.Listbox(self, width=50, height=10)
        self.task_list.pack(pady=10)

        self.load_task()  # Load tasks into the listbox

        complete_button = tk.Button(self, text="Mark Selected as Complete", command=self.mark_task_complete)
        complete_button.pack(pady=5)

        button = tk.Button(self, text="Back", command=lambda: controller.show_frame(MainScreen))
        button.pack(pady=10)

    def load_task(self):
        self.task_list.delete(0, tk.END)  # Clear the listbox

        if os.path.exists(FILE):
            try:
                with open(FILE, "r") as f:
                    tasks = json.load(f)
                    if isinstance(tasks, dict):
                        for task, status in tasks.items():
                            status_text = "✓" if status else "✗"
                            self.task_list.insert(tk.END, f"{status_text} {task}")
                    else:
                        print("⚠ Warning: tasks.json is not formatted correctly. Resetting file.")
            except json.JSONDecodeError:
                print("⚠ Warning: tasks.json is corrupted. Resetting file.")

    def mark_task_complete(self):
        selected_index = self.task_list.curselection()
        
        if not selected_index:
            messagebox.showwarning("Warning", "No task selected.")
            return
        
        selected_task = self.task_list.get(selected_index)
        task_name = selected_task[2:]

        try:
            with open(FILE, "r") as f:
                tasks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            tasks = {}

        if task_name in tasks:
            tasks[task_name] = not tasks[task_name]
            
            with open(FILE, "w") as f:
                json.dump(tasks, f, indent=4)

            new_status = "completed" if tasks[task_name] else "not completed"
            messagebox.showinfo("Success", f"Task '{task_name}' marked as {new_status}.")

            self.load_task()  # Refresh the listbox immediately
            self.controller.frames[viewTask].load_task()

class viewTask(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="View Task", font=("Arial", 16), anchor="center", justify="center")
        label.pack(pady=20)

        self.task_list = tk.Listbox(self, width=50, height=10)
        self.task_list.pack(pady=10)

        self.load_task()

        button = tk.Button(self, text="Back", command=lambda: controller.show_frame(MainScreen))
        button.pack(pady=10)

    def load_task(self):
        self.task_list.delete(0, tk.END)

        if os.path.exists(FILE):
            try:
                with open(FILE, "r") as f:
                    tasks = json.load(f)
                    if isinstance(tasks, dict):
                        for task, status in tasks.items():
                            status_text = "✓" if status else "✗"
                            self.task_list.insert(tk.END, f"{status_text} {task}")
                    else:
                        print("⚠ Warning: tasks.json is not formatted correctly. Resetting file.")
            except json.JSONDecodeError:
                print("⚠ Warning: tasks.json is corrupted. Resetting file.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
