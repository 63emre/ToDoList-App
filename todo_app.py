import os
import json

# TODO: CONSOLE APP


# Language dictionaries
TURKISH = {
    "app_title": "Görev Yönetim Uygulaması",
    "menu_list": "1. Görevleri Listele",
    "menu_add": "2. Yeni Görev Ekle",
    "menu_edit": "3. Görev Düzenle",
    "menu_delete": "4. Görev Sil",
    "menu_language": "5. Dil Değiştir / Change Language",
    "menu_exit": "6. Çıkış",
    "menu_choice": "Seçiminizi yapın: ",
    "invalid_choice": "Geçersiz seçim! Lütfen tekrar deneyin.",
    "no_tasks": "Hiç görev bulunamadı!",
    "enter_task": "Görev metni: ",
    "empty_task": "Boş görev eklenemez!",
    "task_added": "Görev eklendi.",
    "enter_task_num": "Görev numarası: ",
    "invalid_task_num": "Geçersiz görev numarası!",
    "enter_new_task": "Yeni görev metni: ",
    "task_edited": "Görev düzenlendi.",
    "task_deleted": "Görev silindi.",
    "file_error": "Dosya işlemi sırasında bir hata oluştu: ",
    "goodbye": "Programdan çıkılıyor. Hoşçakalın!",
    "lang_changed": "Dil İngilizce olarak değiştirildi."
}

ENGLISH = {
    "app_title": "Task Management Application",
    "menu_list": "1. List Tasks",
    "menu_add": "2. Add New Task",
    "menu_edit": "3. Edit Task",
    "menu_delete": "4. Delete Task",
    "menu_language": "5. Change Language / Dil Değiştir",
    "menu_exit": "6. Exit",
    "menu_choice": "Enter your choice: ",
    "invalid_choice": "Invalid choice! Please try again.",
    "no_tasks": "No tasks found!",
    "enter_task": "Task text: ",
    "empty_task": "Cannot add empty task!",
    "task_added": "Task added.",
    "enter_task_num": "Task number: ",
    "invalid_task_num": "Invalid task number!",
    "enter_new_task": "New task text: ",
    "task_edited": "Task edited.",
    "task_deleted": "Task deleted.",
    "file_error": "An error occurred during file operation: ",
    "goodbye": "Exiting program. Goodbye!",
    "lang_changed": "Language changed to Turkish."
}

class TodoApp:
    def __init__(self):
        self.tasks = []
        self.language = TURKISH  # Default language
        self.file_name = "tasks.json"
        self.load_tasks()
    
    def display_menu(self):
        """Display the main menu in the current language"""
        print("\n" + "=" * 40)
        print(f"    {self.language['app_title']}    ")
        print("=" * 40)
        print(self.language["menu_list"])
        print(self.language["menu_add"])
        print(self.language["menu_edit"])
        print(self.language["menu_delete"])
        print(self.language["menu_language"])
        print(self.language["menu_exit"])
        print("-" * 40)
    
    def list_tasks(self):
        """List all tasks with numbers"""
        if not self.tasks:
            print(self.language["no_tasks"])
            return
        
        print("\n--- Tasks ---")
        for i, task in enumerate(self.tasks, 1):
            print(f"{i}. {task}")
    
    def add_task(self):
        """Add a new task"""
        task = input(self.language["enter_task"]).strip()
        if not task:
            print(self.language["empty_task"])
            return
        
        self.tasks.append(task)
        self.save_tasks()
        print(self.language["task_added"])
    
    def edit_task(self):
        """Edit an existing task"""
        self.list_tasks()
        if not self.tasks:
            return
        
        try:
            task_num = int(input(self.language["enter_task_num"]))
            if task_num < 1 or task_num > len(self.tasks):
                print(self.language["invalid_task_num"])
                return
            
            new_task = input(self.language["enter_new_task"]).strip()
            if not new_task:
                print(self.language["empty_task"])
                return
            
            self.tasks[task_num - 1] = new_task
            self.save_tasks()
            print(self.language["task_edited"])
        except ValueError:
            print(self.language["invalid_task_num"])
    
    def delete_task(self):
        """Delete a task"""
        self.list_tasks()
        if not self.tasks:
            return
        
        try:
            task_num = int(input(self.language["enter_task_num"]))
            if task_num < 1 or task_num > len(self.tasks):
                print(self.language["invalid_task_num"])
                return
            
            del self.tasks[task_num - 1]
            self.save_tasks()
            print(self.language["task_deleted"])
        except ValueError:
            print(self.language["invalid_task_num"])
    
    def change_language(self):
        """Switch between Turkish and English"""
        if self.language == TURKISH:
            self.language = ENGLISH
        else:
            self.language = TURKISH
        print(self.language["lang_changed"])
    
    def save_tasks(self):
        """Save tasks to a file"""
        try:
            with open(self.file_name, 'w', encoding='utf-8') as file:
                json.dump(self.tasks, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"{self.language['file_error']}{str(e)}")
    
    def load_tasks(self):
        """Load tasks from a file"""
        try:
            if os.path.exists(self.file_name):
                with open(self.file_name, 'r', encoding='utf-8') as file:
                    self.tasks = json.load(file)
        except Exception as e:
            print(f"{self.language['file_error']}{str(e)}")
    
    def run(self):
        """Main application loop"""
        while True:
            self.display_menu()
            choice = input(self.language["menu_choice"])
            
            if choice == '1':
                self.list_tasks()
            elif choice == '2':
                self.add_task()
            elif choice == '3':
                self.edit_task()
            elif choice == '4':
                self.delete_task()
            elif choice == '5':
                self.change_language()
            elif choice == '6':
                print(self.language["goodbye"])
                break
            else:
                print(self.language["invalid_choice"])

if __name__ == "__main__":
    app = TodoApp()
    app.run() 