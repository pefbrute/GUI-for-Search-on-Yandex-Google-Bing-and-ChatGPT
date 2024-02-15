import subprocess
import time
import re
from Xlib import X, display

def is_url(path):
    # Проверяем, начинается ли строка с "http"
    return path.startswith("http")

def open_path(path, browser="vivaldi"):
    if is_url(path):
        print("Да, это URL")
        try:
            subprocess.Popen([browser, "--new-window", path])
        except subprocess.CalledProcessError:
            print(f"Failed to open the URL in {browser}.")
        except Exception as e:
            print(f"Unexpected error when opening URL in {browser}: {e}")
    else:
        try:
            subprocess.Popen(path)
        except subprocess.CalledProcessError:
            print(f"Failed to open the application at {path}.")
        except Exception as e:
            print(f"Unexpected error when opening application at {path}: {e}")

def get_active_window():
    d = display.Display()
    root = d.screen().root
    window_id = root.get_full_property(d.intern_atom('_NET_ACTIVE_WINDOW'), X.AnyPropertyType).value[0]
    window = d.create_resource_object('window', window_id)
    return window

def resize_and_move_window(window, width, height, x, y):
    try:
        subprocess.call(["wmctrl", "-r", ":ACTIVE:", "-b", "remove,maximized_vert,maximized_horz"])
        window.configure(width=width, height=height, x=x, y=y)
        window.display.flush()
    except Exception as e:
        print(f"Failed to resize or move window. Error: {e}")

def manage_window(path, width, height, x, y, browser="vivaldi", browser_wait_time=1.5, app_wait_time=15):
    open_path(path, browser)
    
    if is_url(path):
        time.sleep(browser_wait_time)  # Используем значение по умолчанию или предоставленное пользователем для ожидания открытия ссылки
    else:
        time.sleep(app_wait_time)  # Используем значение по умолчанию или предоставленное пользователем для ожидания открытия приложения
        
    active_window = get_active_window()
    resize_and_move_window(active_window, width, height, x, y)

# Пример использования:
# manage_window("/usr/bin/gnome-calculator", 800, 600, 100, 100)  # Для запуска локального приложения
# manage_window("https://chat.openai.com/g/g-pT1I8F71Z-obsuditel-2000", 800, 800, 0, 0)  # Для открытия URL
