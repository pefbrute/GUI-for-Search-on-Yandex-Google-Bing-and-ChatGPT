import tkinter as tk
from tkinter import ttk
import subprocess
import pyperclip
import pyautogui
import time

import sys
sys.path.append('./Libraries/')
from window_manager import manage_window
from translator_module import translate_text_to_english

# Конфигурация режимов поиска
search_modes = {
    "Яндекс": {
        "Поиск, по ...": lambda selected_text: f"https://ya.ru/search?text={selected_text}&lr=213&rstr=-225&lang=ru",
        "Что такое ...?": lambda selected_text: f"https://ya.ru/search?text=Что такое {selected_text}?&lr=213&rstr=-225&lang=ru",
        "Изображения по ...": lambda selected_text: f"https://ya.ru/images/search?from=tabbar&text={selected_text}",
        "Как расшифровывается ...?": lambda selected_text: f"https://ya.ru/search?text=Как расшифровывается {selected_text}?&lr=213&rstr=-225&lang=ru",
        "От какого латинского слова происходит ...?": lambda selected_text: f"https://ya.ru/search?text=От какого латинского слова происходит {selected_text}?&lr=213&rstr=-225&lang=ru",
        "В чём разница между ...?": lambda selected_text: f"https://ya.ru/search?text=В чём разница между {selected_text}?&lr=213&rstr=-225&lang=ru",
        "Скачать ... pdf": lambda selected_text: f"https://ya.ru/search?text=Скачать {selected_text} pdf&lr=213&rstr=-225&lang=ru",
        "Переводчик ... (англ. в рус.)": lambda selected_text: f"https://translate.yandex.ru/?source_lang=en&target_lang=ru&text={selected_text}",
    },
    "Google": {
        "Русский": {
            "Поиск, по ...": lambda selected_text: f"https://www.google.com/search?q={selected_text}&sourceid=chrome&ie=UTF-8",
            "Что такое ...?": lambda selected_text: f"https://www.google.com/search?q=Что такое {selected_text}?&sourceid=chrome&ie=UTF-8",
            "Изображения, по ...": lambda selected_text: f"https://www.google.com/search?q={selected_text}&tbm=isch",
            "Ютуб-видео, по ...": lambda selected_text: f"https://www.youtube.com/results?search_query={selected_text}",
            "Локация на картах, по ...": lambda selected_text: f"https://www.google.com/maps/search/{selected_text}",
        },
        "Английский": {
            "Поиск, по ...": lambda selected_text: f"https://www.google.com/search?q={translate_text_to_english(selected_text)}&sourceid=chrome&ie=UTF-8",
            "What is ...?": lambda selected_text: f"https://www.google.com/search?q=What is {translate_text_to_english(selected_text)}?&sourceid=chrome&ie=UTF-8",
            "Изображения, по ...": lambda selected_text: f"https://www.google.com/search?q={translate_text_to_english(selected_text)}&tbm=isch",
            "Ютуб Видео, по ...": lambda selected_text: f"https://www.youtube.com/results?search_query={translate_text_to_english(selected_text)}",
            "Локация на Картах, по ...": lambda selected_text: f"https://www.google.com/maps/search/{translate_text_to_english(selected_text)}",
        },
    },
    "Бинг": {
        "Русский": {
            "Поиск, по ...": lambda selected_text: f"https://www.bing.com/search?q={selected_text}",
            "Что такое ...?": lambda selected_text: f"https://www.bing.com/search?q=Что такое {selected_text}?",
            "От какого латинского слова происходит ...?": lambda selected_text: f"https://www.bing.com/search?q=От какого латинского слова происходит слово {selected_text}?",
            "Изображения, по ...": lambda selected_text: f"https://www.bing.com/images/search?q={selected_text}",
        },
        "Английский": {
            "Поиск, по ...": lambda selected_text: f"https://www.bing.com/search?q={translate_text_to_english(selected_text)}",
            "What is ...?": lambda selected_text: f"https://www.bing.com/search?q=What is {translate_text_to_english(selected_text)}?",
            "From which latin (or other language) comes word ... ?": lambda selected_text: f"https://www.bing.com/search?q=From which latin (or other language) comes word {translate_text_to_english(selected_text)}?",
            "Изображения, по ...": lambda selected_text: f"https://www.bing.com/images/search?q={translate_text_to_english(selected_text)}",
        },
    },
    "ГПТшка": {
        "Вопрос по ...": lambda selected_text: search_in_GPT(selected_text),
        "Объясни, как пятилетке, что это такое ...?": lambda selected_text: search_in_GPT(f"Объясни, как пятилетке, что это такое '{selected_text}'?"),
        "Предложи 3 лучшие книги по этой теме ...": lambda selected_text: search_in_GPT(f"Предложи 3 лучшие книги по этой теме '{selected_text}'"),
        "В каких 3 книгах вероятнее всего могут быть упоминания по этой теме ...": lambda selected_text: search_in_GPT(f"В каких 3 книгах вероятнее всего могут быть упоминания по этой теме '{selected_text}'?"),
        "Придумай максимально понятное название для данной функции ...": lambda selected_text: search_in_GPT(f"Придумай максимально понятное название для данной функции, чтобы каждый мог примерно понять, какой будет результат после этой функции. Дай 5 идей. НАЗВАНИЕ ФУНКЦИЙ ДОЛЖНО БЫТЬ НА АНГЛИЙСКОМ\n '{selected_text}'?"),
    }
}

def search_in_GPT(text):
    pyperclip.copy(text)
    gpt_url = "https://chat.openai.com/g/g-pT1I8F71Z-obsuditel-2000"
    manage_window(gpt_url, 900, 800, 50, 50)
    time.sleep(3)
    pyautogui.hotkey('ctrl', 'v')

def open_website(url):
    try:
        if "http" in url:
            manage_window(url, 1400, 800, 50, 50)
    except Exception as e:
        print(str(e))

# Модифицируем функцию create_tab для использования общего поля ввода
def create_tab(tab, modes, input_text):
    font_specs = ("Arial", 12)
    
    for mode_name, mode_function in modes.items():
        button = tk.Button(tab, text=mode_name, font=font_specs,
                           command=lambda f=mode_function, it=input_text: open_website(f(it.get())))
        button.pack(pady=5)

# Функция для обработки закрытия окна
def on_close(root):
    root.destroy()

def create_gui():
    window = tk.Tk()
    window.title("Универсальный Поиск")
    window.geometry("1200x800")  # Размер окна может быть изменён по вашему усмотрению

    # Фрейм для поля ввода и кнопки очистки
    input_frame = tk.Frame(window)
    input_frame.pack(pady=10)

    # Общее поле ввода
    input_text = tk.Entry(input_frame, font=("Arial", 12))
    input_text.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

    # Функция для очистки поля ввода
    def clear_input():
        input_text.delete(0, tk.END)

    # Кнопка для очистки поля ввода
    clear_button = tk.Button(input_frame, text="Очистить", font=("Arial", 12), command=clear_input)
    clear_button.pack(side=tk.RIGHT)

    tab_control = ttk.Notebook(window)

    for platform_name, platform_modes in search_modes.items():
        # Проверяем, нужно ли создавать подвкладки для данной платформы
        if isinstance(next(iter(platform_modes.values())), dict):  # Предполагаем, что все элементы однородны
            # Создание вкладки для платформы с подвкладками
            platform_tab = ttk.Frame(tab_control)
            tab_control.add(platform_tab, text=platform_name)
            platform_tab_control = ttk.Notebook(platform_tab)  # Внутренний Notebook для подвкладок
            
            for sub_platform_name, sub_platform_modes in platform_modes.items():
                # Создание подвкладок внутри вкладки платформы
                sub_tab = ttk.Frame(platform_tab_control)
                platform_tab_control.add(sub_tab, text=sub_platform_name)
                create_tab(sub_tab, sub_platform_modes, input_text)
                
            platform_tab_control.pack(expand=1, fill="both")
        else:
            # Создание вкладки для платформы без подвкладок
            tab = ttk.Frame(tab_control)
            tab_control.add(tab, text=platform_name)
            create_tab(tab, platform_modes, input_text)

    tab_control.pack(expand=1, fill="both")
    
    window.mainloop()

create_gui()
