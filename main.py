import customtkinter as tk
import re
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import ttk

from translator import run_translate
from subCreatorByRole import create_subs_with_actors
import json


def handle_drop(event):
    file = event.data.replace('{', '').replace('}', '')
    if file and file.lower().endswith(".ass"):
        try:
            status_label.configure(text="Почав перекладати)", fg_color="green")
            run_translate()
            status_label.configure(text="Переклад завершено)", fg_color="blue")
        except:
            status_label.configure(text="Якась помилка з ШІ", fg_color="grey")
    else:
        status_label.configure(text="Щось не добре(", fg_color="red")


def handle_drop2(event):
    try:
        file_path = event.data.replace('{', '').replace('}', '')
        if file_path and file_path.lower().endswith(".ass"):
            create_subs_with_actors(file_path)
            status_label2.configure(text="Конвертовано)", fg_color="green")
        else:
            status_label2.configure(text="Помилковий формат файлу. Потрібен .ass", fg_color="red")
    except json.JSONDecodeError:
        status_label2.configure(text="Помилка при обробці даних", fg_color="red")


root = TkinterDnD.Tk()
root.title("Перетягніть файл .ass")
window_width = 400
window_height = 300

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Создаем виджет вкладок
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Создаем первую вкладку
frame1 = ttk.Frame(notebook)
notebook.add(frame1, text="Вкладка 1")

# Создаем вторую вкладку
frame2 = ttk.Frame(notebook)
notebook.add(frame2, text="Вкладка 2")

# Создаем метку для отображения статуса
status_label = tk.CTkLabel(frame1, text="Перетягніть файл .ass сюди", font=("Helvetica", 14), bg_color="black")
status_label.pack(pady=20, fill="both")

status_label2 = tk.CTkLabel(frame2, text="Перетягніть файл .ass сюди щоб створити srt по акторам",
                            font=("Helvetica", 14), bg_color="black")
status_label2.pack(pady=20, fill="both")

# Добавляем обработчик события перетаскивания
frame1.drop_target_register(DND_FILES)
frame1.dnd_bind('<<Drop>>', handle_drop)

frame2.drop_target_register(DND_FILES)
frame2.dnd_bind('<<Drop>>', handle_drop2)

root.mainloop()
