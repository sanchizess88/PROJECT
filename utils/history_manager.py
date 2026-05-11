import json
import os
import time

class HistoryManager:
    def __init__(self, filename="history.json"):
        self.filename = filename
        self.history = self.load()
    
    def load(self):
        """Загрузка истории из файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save(self):
        """Сохранение истории в файл"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def add(self, task):
        """Добавление в историю"""
        self.history.append({
            'task': task,
            'time': time.time()
        })
        # Оставляем последние 50 записей
        if len(self.history) > 50:
            self.history = self.history[-50:]
        self.save()
    
    def get_all(self):
        """Получение всей истории"""
        return self.history
    
    def clear(self):
        """Очистка истории"""
        self.history = []
        self.save()