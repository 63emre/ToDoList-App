import os
import json
import tkinter as tk
from tkinter import ttk, messagebox

# Language dictionaries
TURKISH = {
    "app_title": "Görev Yönetim Uygulaması",
    "task_list": "Görev Listesi",
    "add_task": "Görev Ekle",
    "edit_task": "Düzenle",
    "delete_task": "Sil",
    "task_entry_label": "Görev Metni:",
    "due_date_label": "Son Tarih (YYYY-MM-DD):",
    "priority_label": "Öncelik:",
    "add_button": "Ekle",
    "edit_button": "Düzenle",
    "delete_button": "Sil",
    "change_lang": "İngilizce'ye Geç",
    "empty_task": "Boş görev eklenemez!",
    "task_added": "Görev eklendi.",
    "task_edited": "Görev düzenlendi.",
    "task_deleted": "Görev silindi.",
    "select_task": "Lütfen bir görev seçin.",
    "file_error": "Dosya işlemi sırasında bir hata oluştu: ",
    "confirm_delete": "Silme Onayı",
    "confirm_delete_msg": "Bu görevi silmek istediğinizden emin misiniz?",
    "yes": "Evet",
    "no": "Hayır",
    "completed": "Tamamlandı",
    "sort_by": "Sıralama:",
    "sort_by_name": "İsim",
    "sort_by_priority": "Öncelik",
    "sort_by_date": "Tarih",
    "low_priority": "Düşük",
    "medium_priority": "Orta",
    "high_priority": "Yüksek",
    "invalid_date": "Geçersiz tarih formatı! YYYY-MM-DD formatını kullanın."
}

ENGLISH = {
    "app_title": "Task Management Application",
    "task_list": "Task List",
    "add_task": "Add Task",
    "edit_task": "Edit",
    "delete_task": "Delete",
    "task_entry_label": "Task Text:",
    "due_date_label": "Due Date (YYYY-MM-DD):",
    "priority_label": "Priority:",
    "add_button": "Add",
    "edit_button": "Edit",
    "delete_button": "Delete",
    "change_lang": "Switch to Turkish",
    "empty_task": "Cannot add empty task!",
    "task_added": "Task added.",
    "task_edited": "Task edited.",
    "task_deleted": "Task deleted.",
    "select_task": "Please select a task.",
    "file_error": "An error occurred during file operation: ",
    "confirm_delete": "Delete Confirmation",
    "confirm_delete_msg": "Are you sure you want to delete this task?",
    "yes": "Yes",
    "no": "No",
    "completed": "Completed",
    "sort_by": "Sort by:",
    "sort_by_name": "Name",
    "sort_by_priority": "Priority",
    "sort_by_date": "Date",
    "low_priority": "Low",
    "medium_priority": "Medium",
    "high_priority": "High",
    "invalid_date": "Invalid date format! Please use YYYY-MM-DD format."
}

class Task:
    def __init__(self, text, due_date=None, priority="medium", completed=False):
        self.text = text
        self.due_date = due_date
        self.priority = priority
        self.completed = completed
    
    def to_dict(self):
        return {
            "text": self.text,
            "due_date": self.due_date,
            "priority": self.priority,
            "completed": self.completed
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            text=data["text"],
            due_date=data.get("due_date"),
            priority=data.get("priority", "medium"),
            completed=data.get("completed", False)
        )
    
    def __str__(self):
        status = "✓ " if self.completed else "□ "
        priority_markers = {"low": "⬇️", "medium": "➡️", "high": "⬆️"}
        priority_mark = priority_markers.get(self.priority, "➡️")
        
        date_str = ""
        if self.due_date:
            date_str = f" [{self.due_date}]"
        
        return f"{status}{priority_mark} {self.text}{date_str}"

class TodoAppGUI:
    def __init__(self, root):
        self.root = root
        self.tasks = []
        self.language = TURKISH  # Default language
        self.file_name = "tasks.json"
        self.selected_index = None
        self.task_labels = []
        self.sort_by = "name"  # Default sort by name
        
        # Load tasks
        self.load_tasks()
        
        # Set up the UI
        self.setup_ui()
        
    def setup_ui(self):
        # Configure the root window
        self.root.title(self.language["app_title"])
        self.root.geometry("700x500")
        self.root.minsize(600, 450)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Language button (top right)
        lang_button = ttk.Button(
            main_frame, 
            text=self.language["change_lang"],
            command=self.change_language
        )
        lang_button.pack(side=tk.TOP, anchor=tk.E, pady=(0, 10))
        self.lang_button = lang_button
        
        # Sort options frame
        sort_frame = ttk.Frame(main_frame)
        sort_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))
        
        # Sort label
        self.sort_label = ttk.Label(sort_frame, text=self.language["sort_by"])
        self.sort_label.pack(side=tk.LEFT, padx=5)
        
        # Sort combobox
        self.sort_combobox = ttk.Combobox(
            sort_frame, 
            values=[
                self.language["sort_by_name"],
                self.language["sort_by_priority"],
                self.language["sort_by_date"]
            ],
            width=10,
            state="readonly"
        )
        self.sort_combobox.current(0)  # Default to name
        self.sort_combobox.pack(side=tk.LEFT, padx=5)
        self.sort_combobox.bind("<<ComboboxSelected>>", self.on_sort_change)
        
        # Task list frame (left side)
        list_frame = ttk.LabelFrame(main_frame, text=self.language["task_list"])
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.list_frame = list_frame
        
        # Task listbox with scrollbar
        task_listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE, font=("Arial", 10))
        task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.task_listbox = task_listbox
        
        # Scrollbar for listbox
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=task_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        task_listbox.config(yscrollcommand=scrollbar.set)
        
        # Bind listbox selection event
        task_listbox.bind('<<ListboxSelect>>', self.on_task_select)
        
        # Task entry frame (right side)
        entry_frame = ttk.Frame(main_frame)
        entry_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Task entry
        self.task_entry_label = ttk.Label(entry_frame, text=self.language["task_entry_label"])
        self.task_entry_label.pack(anchor=tk.W, pady=(10, 5))
        task_entry = ttk.Entry(entry_frame, width=40, font=("Arial", 10))
        task_entry.pack(fill=tk.X, pady=(0, 5))
        self.task_entry = task_entry
        
        # Due date entry
        self.due_date_label = ttk.Label(entry_frame, text=self.language["due_date_label"])
        self.due_date_label.pack(anchor=tk.W, pady=(10, 5))
        self.due_date_entry = ttk.Entry(entry_frame, width=20)
        self.due_date_entry.pack(anchor=tk.W, pady=(0, 5))
        
        # Priority selection
        self.priority_label = ttk.Label(entry_frame, text=self.language["priority_label"])
        self.priority_label.pack(anchor=tk.W, pady=(10, 5))
        self.priority_var = tk.StringVar(value="medium")
        
        priority_frame = ttk.Frame(entry_frame)
        priority_frame.pack(anchor=tk.W, pady=(0, 5), fill=tk.X)
        
        ttk.Radiobutton(priority_frame, text=self.language["low_priority"], 
                        variable=self.priority_var, value="low").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(priority_frame, text=self.language["medium_priority"], 
                        variable=self.priority_var, value="medium").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(priority_frame, text=self.language["high_priority"], 
                        variable=self.priority_var, value="high").pack(side=tk.LEFT, padx=5)
        
        # Completed checkbox
        self.completed_var = tk.BooleanVar(value=False)
        self.completed_check = ttk.Checkbutton(
            entry_frame, 
            text=self.language["completed"],
            variable=self.completed_var
        )
        self.completed_check.pack(anchor=tk.W, pady=(5, 10))
        
        # Buttons frame
        button_frame = ttk.Frame(entry_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        # Add button
        add_button = ttk.Button(
            button_frame,
            text=self.language["add_button"],
            command=self.add_task
        )
        add_button.pack(side=tk.LEFT, padx=5)
        self.add_button = add_button
        
        # Edit button
        edit_button = ttk.Button(
            button_frame,
            text=self.language["edit_button"],
            command=self.edit_task,
            state=tk.DISABLED
        )
        edit_button.pack(side=tk.LEFT, padx=5)
        self.edit_button = edit_button
        
        # Delete button
        delete_button = ttk.Button(
            button_frame,
            text=self.language["delete_button"],
            command=self.delete_task,
            state=tk.DISABLED
        )
        delete_button.pack(side=tk.LEFT, padx=5)
        self.delete_button = delete_button
        
        # Track UI elements that need language updates
        self.task_labels = [
            self.task_entry_label,
            self.due_date_label,
            self.priority_label,
            self.sort_label,
            self.completed_check
        ]
        
        # Populate the listbox
        self.populate_task_list()
    
    def on_sort_change(self, event):
        selection = self.sort_combobox.get()
        if selection == self.language["sort_by_name"]:
            self.sort_by = "name"
        elif selection == self.language["sort_by_priority"]:
            self.sort_by = "priority"
        elif selection == self.language["sort_by_date"]:
            self.sort_by = "date"
        
        self.populate_task_list()
    
    def is_valid_date(self, date_str):
        if not date_str:
            return True  # Empty date is allowed
        
        try:
            # Check format YYYY-MM-DD
            if len(date_str) != 10:
                return False
            
            year, month, day = date_str.split('-')
            if len(year) != 4 or len(month) != 2 or len(day) != 2:
                return False
            
            # Check if they are numbers
            int(year)
            int(month)
            int(day)
            
            return True
        except:
            return False
    
    def sort_tasks(self):
        if self.sort_by == "name":
            return sorted(self.tasks, key=lambda t: t.text.lower())
        elif self.sort_by == "priority":
            priority_order = {"low": 0, "medium": 1, "high": 2}
            return sorted(self.tasks, key=lambda t: priority_order.get(t.priority, 1), reverse=True)
        elif self.sort_by == "date":
            # Sort by due date with None values at the end
            return sorted(self.tasks, key=lambda t: (t.due_date is None, t.due_date or "9999-12-31"))
        
        return self.tasks
    
    def populate_task_list(self):
        # Clear the listbox
        self.task_listbox.delete(0, tk.END)
        
        # Sort tasks
        sorted_tasks = self.sort_tasks()
        
        # Add tasks to the listbox
        for task in sorted_tasks:
            self.task_listbox.insert(tk.END, str(task))
    
    def on_task_select(self, event):
        # Get selected indices
        selection = self.task_listbox.curselection()
        if selection:
            # Get the selected index
            index = selection[0]
            sorted_tasks = self.sort_tasks()
            selected_task = sorted_tasks[index]
            
            # Find the actual index in the original tasks list
            self.selected_index = self.tasks.index(selected_task)
            
            # Enable edit and delete buttons
            self.edit_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
            
            # Display the selected task in the entry fields
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, selected_task.text)
            
            # Set the due date
            self.due_date_entry.delete(0, tk.END)
            if selected_task.due_date:
                self.due_date_entry.insert(0, selected_task.due_date)
            
            # Set the priority
            self.priority_var.set(selected_task.priority)
            
            # Set completed status
            self.completed_var.set(selected_task.completed)
        else:
            self.selected_index = None
            self.edit_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
    
    def get_task_from_form(self):
        # Get task text
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("", self.language["empty_task"])
            return None
        
        # Get due date
        due_date_str = self.due_date_entry.get().strip()
        if due_date_str and not self.is_valid_date(due_date_str):
            messagebox.showwarning("", self.language["invalid_date"])
            return None
        
        # Get priority
        priority = self.priority_var.get()
        
        # Get completed status
        completed = self.completed_var.get()
        
        return Task(task_text, due_date_str if due_date_str else None, priority, completed)
    
    def add_task(self):
        # Get task from form
        task = self.get_task_from_form()
        if task is None:
            return
        
        # Add task
        self.tasks.append(task)
        self.save_tasks()
        
        # Update listbox
        self.populate_task_list()
        
        # Clear entry fields
        self.task_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.priority_var.set("medium")
        self.completed_var.set(False)
        
        # Show confirmation
        messagebox.showinfo("", self.language["task_added"])
    
    def edit_task(self):
        # Check if a task is selected
        if self.selected_index is None:
            messagebox.showwarning("", self.language["select_task"])
            return
        
        # Get task from form
        task = self.get_task_from_form()
        if task is None:
            return
        
        # Update task
        self.tasks[self.selected_index] = task
        self.save_tasks()
        
        # Update listbox
        self.populate_task_list()
        
        # Show confirmation
        messagebox.showinfo("", self.language["task_edited"])
    
    def delete_task(self):
        # Check if a task is selected
        if self.selected_index is None:
            messagebox.showwarning("", self.language["select_task"])
            return
        
        # Confirm deletion
        if not messagebox.askyesno(
            self.language["confirm_delete"], 
            self.language["confirm_delete_msg"]
        ):
            return
        
        # Delete task
        del self.tasks[self.selected_index]
        self.save_tasks()
        
        # Update listbox
        self.populate_task_list()
        
        # Clear selection and entry
        self.selected_index = None
        self.task_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.priority_var.set("medium")
        self.completed_var.set(False)
        self.edit_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)
        
        # Show confirmation
        messagebox.showinfo("", self.language["task_deleted"])
    
    def change_language(self):
        # Switch language
        if self.language == TURKISH:
            self.language = ENGLISH
        else:
            self.language = TURKISH
        
        # Update UI texts
        self.root.title(self.language["app_title"])
        self.list_frame.config(text=self.language["task_list"])
        self.lang_button.config(text=self.language["change_lang"])
        self.add_button.config(text=self.language["add_button"])
        self.edit_button.config(text=self.language["edit_button"])
        self.delete_button.config(text=self.language["delete_button"])
        
        # Update labels
        self.task_entry_label.config(text=self.language["task_entry_label"])
        self.due_date_label.config(text=self.language["due_date_label"])
        self.priority_label.config(text=self.language["priority_label"])
        self.sort_label.config(text=self.language["sort_by"])
        self.completed_check.config(text=self.language["completed"])
        
        # Update sort combobox
        current_index = self.sort_combobox.current()
        self.sort_combobox.config(values=[
            self.language["sort_by_name"],
            self.language["sort_by_priority"],
            self.language["sort_by_date"]
        ])
        self.sort_combobox.current(current_index)
    
    def save_tasks(self):
        """Save tasks to a file"""
        try:
            tasks_data = [task.to_dict() for task in self.tasks]
            with open(self.file_name, 'w', encoding='utf-8') as file:
                json.dump(tasks_data, file, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("", f"{self.language['file_error']}{str(e)}")
    
    def load_tasks(self):
        """Load tasks from a file"""
        try:
            if os.path.exists(self.file_name):
                with open(self.file_name, 'r', encoding='utf-8') as file:
                    tasks_data = json.load(file)
                    
                    # Convert old format if needed
                    if tasks_data and isinstance(tasks_data[0], str):
                        self.tasks = [Task(text=text) for text in tasks_data]
                    else:
                        self.tasks = [Task.from_dict(task_dict) for task_dict in tasks_data]
        except Exception as e:
            messagebox.showerror("", f"{self.language['file_error']}{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoAppGUI(root)
    root.mainloop() 