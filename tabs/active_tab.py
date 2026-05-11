import tkinter as tk
from tkinter import messagebox
import time

class ActiveTab:
    def __init__(self, parent):
        self.parent = parent
        
        # Заголовок
        tk.Label(parent, text="Активные напоминания", font=("Arial", 12)).pack(pady=5)
        
        # Список с прокруткой
        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side='right', fill='y')
        
        self.listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, height=15)
        self.listbox.pack(side='left', fill='both', expand=True)
        
        scrollbar.config(command=self.listbox.yview)
        
        # Храним соответствие между позициями в списке и напоминаниями
        self.items = []
    
    def update_list(self, reminders, cancel_callback):
        """Обновление списка активных напоминаний"""
        self.listbox.delete(0, tk.END)
        self.items = []
        
        if not reminders:
            self.listbox.insert(tk.END, "Нет активных напоминаний")
            return
        
        current_time = time.time()
        
        for rem in reminders:
            remaining = int(rem["end_time"] - current_time)
            text = f"{rem['task']} - осталось {remaining} сек."
            self.listbox.insert(tk.END, text)
            self.items.append(rem)
        
        # Привязываем обработчик двойного клика для отмены
        def on_double_click(event):
            selection = self.listbox.curselection()
            if selection and selection[0] < len(self.items):
                reminder = self.items[selection[0]]
                if messagebox.askyesno("Отмена", f"Отменить '{reminder['task']}'?"):
                    cancel_callback(reminder)
        
        self.listbox.bind('<Double-Button-1>', on_double_click)