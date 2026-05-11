import tkinter as tk
from datetime import datetime

class CreateTab:
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        
        # Приветствие
        current_hour = datetime.now().hour
        if current_hour < 12:
            greeting = "Доброе утро!"
        elif current_hour < 18:
            greeting = "Добрый день!"
        else:
            greeting = "Добрый вечер!"
        
        greeting_label = tk.Label(parent, text=greeting, font=("Arial", 14))
        greeting_label.pack(pady=10)
        
        # Дата
        date_label = tk.Label(parent, text=datetime.now().strftime("%d.%m.%Y"))
        date_label.pack()
        
        # Поля ввода
        tk.Label(parent, text="Что нужно сделать?").pack(pady=5)
        self.task_entry = tk.Entry(parent, width=30)
        self.task_entry.pack()
        self.task_entry.focus()
        
        tk.Label(parent, text="Через сколько секунд?").pack(pady=5)
        self.time_entry = tk.Entry(parent, width=10)
        self.time_entry.pack()
        
        # Кнопка
        self.create_btn = tk.Button(parent, text="Создать напоминание", 
                                   command=self.create_reminder,
                                   bg="lightblue", padx=10, pady=5)
        self.create_btn.pack(pady=20)
        
        # Метка для сообщений
        self.message_label = tk.Label(parent, text="", fg="green")
        self.message_label.pack()
        
        # Enter для быстрого ввода
        self.task_entry.bind('<Return>', lambda e: self.time_entry.focus())
        self.time_entry.bind('<Return>', lambda e: self.create_reminder())
    
    def create_reminder(self):
        """Создание напоминания"""
        task = self.task_entry.get().strip()
        if not task:
            task = "Напоминание"
        
        try:
            seconds = int(self.time_entry.get())
            if seconds <= 0:
                self.show_message("Время должно быть больше 0", "red")
                return
            
            self.callback(task, seconds)
            self.task_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)
            
        except ValueError:
            self.show_message("Введите число", "red")
    
    def show_message(self, text, color="green"):
        """Показать сообщение"""
        self.message_label.config(text=text, fg=color)
        self.parent.after(2000, lambda: self.message_label.config(text=""))