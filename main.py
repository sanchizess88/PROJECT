import tkinter as tk  # Основная библиотека для GUI
from tkinter import messagebox, ttk  # messagebox — окна, ttk — улучшенные виджеты
import time  # Работа со временем (таймеры)
from datetime import datetime  # Форматирование даты
import os
import sys

# Добавляем текущую папку в путь поиска модулей
# Это нужно, чтобы Python нашёл папки tabs и utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Импорт наших модулей
from tabs.create_tab import CreateTab
from tabs.active_tab import ActiveTab
from utils.history_manager import HistoryManager


class ReminderApp:
    def __init__(self, root):
        self.root = root  # Главное окно
        self.root.title("Напоминалка")  # Заголовок окна
        self.root.geometry("400x500")  # Размер окна
        
        # Создаём менеджер истории (отвечает за хранение выполненных задач)
        self.history_manager = HistoryManager()
        
        # Список активных напоминаний
        # Каждый элемент — словарь с задачей и временем окончания
        self.active_reminders = []
        
        # Что делать при закрытии окна
        self.root.protocol('WM_DELETE_WINDOW', self.root.quit)
        
        # Создаём контейнер вкладок (как в браузере)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # ВКЛАДКА 1: СОЗДАНИЕ
        self.create_frame = ttk.Frame(self.notebook)  # Создаём фрейм
        self.notebook.add(self.create_frame, text="Создать")  # Добавляем вкладку
        
        # Передаём функцию set_reminder — она вызовется при создании задачи
        self.create_tab = CreateTab(self.create_frame, self.set_reminder)
        
        # ВКЛАДКА 2: АКТИВНЫЕ
        self.active_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.active_frame, text="Активные")
        
        # Вкладка отображает текущие таймеры
        self.active_tab = ActiveTab(self.active_frame)
        
        # ВКЛАДКА 3: ИСТОРИЯ
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="История")
        
        self.setup_history_tab()  # Настраиваем её
        
        # Запускаем обновление таймеров (главный цикл логики)
        self.update_timers()
    

    def setup_history_tab(self):
        """Настройка вкладки истории"""
        
        # Кнопка очистки истории
        clear_btn = tk.Button(
            self.history_frame,
            text="Очистить историю",
            command=self.clear_history  # При нажатии вызывается функция
        )
        clear_btn.pack(pady=5)
        
        # Список (Listbox) для отображения истории
        self.history_listbox = tk.Listbox(self.history_frame, height=15)
        self.history_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Заполняем список
        self.update_history_display()
    

    def set_reminder(self, task_name, seconds):
        """Создание нового напоминания"""
        
        # Вычисляем время окончания (текущее время + секунды)
        end_time = time.time() + seconds
        
        # Добавляем в список активных
        self.active_reminders.append({
            "task": task_name,
            "end_time": end_time
        })
        
        # Показываем сообщение пользователю
        self.create_tab.show_message(f"Создано: {task_name}")
    

    def update_timers(self):
        """Обновление таймеров (вызывается каждую секунду)"""
        
        current_time = time.time()  # Текущее время
        
        still_active = []  # Новый список активных задач
        
        # Проверяем каждое напоминание
        for item in self.active_reminders:
            
            # Сколько осталось времени
            remaining = int(item["end_time"] - current_time)
            
            if remaining > 0:
                # Если ещё не время — оставляем
                still_active.append(item)
            else:
                # Если время вышло
                
                # Показываем уведомление
                messagebox.showinfo("Напоминание", f"Пора: {item['task']}")
                
                # Добавляем в историю
                self.history_manager.add(item['task'])
                
                # Обновляем отображение истории
                self.update_history_display()
        
        # Обновляем список активных задач
        self.active_reminders = still_active
        
        # Обновляем вкладку "Активные"
        # Передаём список и функцию отмены
        self.active_tab.update_list(self.active_reminders, self.cancel_reminder)
        
        # Планируем следующий запуск через 1 секунду (1000 мс)
        self.root.after(1000, self.update_timers)
    

    def cancel_reminder(self, reminder):
        """Отмена напоминания"""
        
        # Проверяем, есть ли оно в списке
        if reminder in self.active_reminders:
            self.active_reminders.remove(reminder)  # Удаляем
    

    def update_history_display(self):
        """Обновление списка истории"""
        
        # Очищаем список
        self.history_listbox.delete(0, tk.END)
        
        # Получаем всю историю
        history = self.history_manager.get_all()
        
        # Берём последние 10 записей и переворачиваем (новые сверху)
        for item in reversed(history[-10:]):
            
            # Форматируем время
            time_str = datetime.fromtimestamp(item['time']).strftime("%H:%M %d.%m")
            
            # Добавляем строку в список
            self.history_listbox.insert(tk.END, f"{time_str} - {item['task']}")
    

    def clear_history(self):
        """Очистка истории"""
        
        # Спрашиваем подтверждение
        if messagebox.askyesno("Подтверждение", "Очистить историю?"):
            
            # Очищаем данные
            self.history_manager.clear()
            
            # Обновляем интерфейс
            self.update_history_display()


# Запуск
if __name__ == "__main__":
    
    root = tk.Tk()  # Создаём главное окно
    
    app = ReminderApp(root)  # Создаём приложение
    
    root.mainloop()  # Запускаем главный цикл