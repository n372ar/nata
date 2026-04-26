import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

HISTORY_FILE = "history.json"

class RandomTaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("450x550")

        # 1. Предопределённые задачи
        self.tasks = [
            {"name": "Прочитать статью", "type": "учёба"},
            {"name": "Сделать зарядку", "type": "спорт"},
            {"name": "Написать отчёт", "type": "работа"},
            {"name": "Изучить новую тему", "type": "учёба"},
            {"name": "Пробежка 30 мин", "type": "спорт"},
            {"name": "Подготовить презентацию", "type": "работа"},
            {"name": "Решить 5 задач по Python", "type": "учёба"},
            {"name": "Растяжка и дыхание", "type": "спорт"},
            {"name": "Ответить на рабочие письма", "type": "работа"}
        ]

        self.history = []
        self.load_history()
        self.setup_ui()

    def setup_ui(self):
        main = ttk.Frame(self.root, padding="15")
        main.pack(fill=tk.BOTH, expand=True)

        # 4. Фильтр по типу
        filter_frame = ttk.Frame(main)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(filter_frame, text="Фильтр по типу:").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar(value="Все")
        ttk.Combobox(filter_frame, textvariable=self.filter_var,
                     values=["Все", "учёба", "спорт", "работа"], state="readonly").pack(side=tk.LEFT, padx=(5, 0))

        # 2. Кнопка генерации
        ttk.Button(main, text="🎲 Сгенерировать задачу", command=self.generate_task).pack(fill=tk.X, pady=10)

        # Отображение текущей задачи
        self.current_var = tk.StringVar(value="Нажмите кнопку для генерации...")
        ttk.Label(main, textvariable=self.current_var, font=("Segoe UI", 14, "bold"),
                  wraplength=400, justify="center").pack(pady=10)

        # 3. История задач
        ttk.Label(main, text="История сгенерированных задач:").pack(anchor=tk.W)
        self.history_list = tk.Listbox(main, height=10, font=("Segoe UI", 10))
        self.history_list.pack(fill=tk.BOTH, expand=True, pady=(5, 10))

        # Добавление новой задачи
        add_frame = ttk.LabelFrame(main, text="Добавить новую задачу", padding="10")
        add_frame.pack(fill=tk.X, pady=(5, 0))

        self.new_name_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_name_var).pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.new_type_var = tk.StringVar(value="учёба")
        ttk.Combobox(add_frame, textvariable=self.new_type_var,
                     values=["учёба", "спорт", "работа"], state="readonly", width=10).pack(side=tk.LEFT, padx=(5, 0))

        ttk.Button(add_frame, text="Добавить", command=self.add_new_task).pack(side=tk.RIGHT, padx=(5, 0))

        self.update_history_display()

    def get_filtered_tasks(self):
        f = self.filter_var.get()
        return self.tasks if f == "Все" else [t for t in self.tasks if t["type"] == f]

    def generate_task(self):
        available = self.get_filtered_tasks()
        if not available:
            self.current_var.set("❌ Нет задач для выбранного фильтра")
            return
        task = random.choice(available)
        self.history.append(task)
        self.current_var.set(f"✅ {task['name']} [{task['type']}]")
        self.save_history()
        self.update_history_display()

    def update_history_display(self):
        self.history_list.delete(0, tk.END)
        for idx, t in enumerate(reversed(self.history)):
            self.history_list.insert(tk.END, f"{idx+1}. {t['name']} ({t['type']})")
        if self.history:
            self.history_list.see(0)

    def add_new_task(self):
        # 6. Проверка корректности ввода
        name = self.new_name_var.get().strip()
        if not name:
            messagebox.showwarning("Ошибка ввода", "Название задачи не может быть пустым!")
            self.new_name_var.set("")
            return
        task_type = self.new_type_var.get()
        self.tasks.append({"name": name, "type": task_type})
        self.new_name_var.set("")
        messagebox.showinfo("Успех", f"Задача '{name}' добавлена в тип '{task_type}'")

    # 5. Сохранение в JSON
    def save_history(self):
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить историю: {e}")

    # 5. Загрузка из JSON
    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except (json.JSONDecodeError, Exception) as e:
                self.history = []
                messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить историю: {e}")
        else:
            self.history = []

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGeneratorApp(root)
    root.mainloop()
