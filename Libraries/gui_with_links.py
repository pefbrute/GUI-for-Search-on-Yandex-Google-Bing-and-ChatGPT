# gui_with_links.py
import tkinter as tk
from tkinter import ttk

# Убедитесь, что путь к вашим библиотекам корректен
import sys
sys.path.append('/home/pefbrute/.config/autokey/data/My Phrases/Скрипты и прочее1/Библиотеки')
from window_manager import manage_window

def chunk_list(lst, n):
    """Разбивает список на подсписки по n элементов."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

class LinksApp:
    def __init__(self, root, tabs_and_links):
        self.root = root
        self.tabs_and_links = tabs_and_links
        self.root.title("Коллекция ссылок")
        self.root.geometry("1200x800")

        self.tab_control = ttk.Notebook(root)

        for tab_name, links in self.tabs_and_links.items():
            self.add_tab(tab_name, links)

        self.tab_control.pack(expand=1, fill="both")

    def add_tab(self, tab_name, links):
        new_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(new_tab, text=tab_name)

        for link_group in chunk_list(links, 4):
            link_group_frame = ttk.Frame(new_tab)
            link_group_frame.pack(pady=10)
            for link in link_group:
                self.add_link_button(link_group_frame, link)

    def add_link_button(self, frame, link):
        link_button = tk.Button(frame, text=link["name"], command=lambda: self.open_link(link))
        link_button.pack(side=tk.TOP)

    def open_link(self, link):
        url = link["url"]
        window_settings = link.get("window_settings", {})
        width = window_settings.get("width", 1200)
        height = window_settings.get("height", 800)
        x = window_settings.get("x", 50)
        y = window_settings.get("y", 50)
        browser = window_settings.get("browser", "vivaldi")
        open_wait = window_settings.get("open_wait", 10)
        app_wait = window_settings.get("app_wait", 5)
        
        manage_window(url, width, height, x, y, browser, open_wait, app_wait)
