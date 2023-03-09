import tkinter as tk
from tkinter import ttk

class Item(ttk.Frame):
    def __init__(self, container, name, genre, score):
        super().__init__(container)
        # field options
        options = {'padx': 5, 'pady': 5}
        self.container = container

        self.title = ttk.Label(self, text=name)
        self.title.pack(**options)
        def quit():
            self.tabID = self.container.index("current")
            self.container.forget(self.tabID)
        
        self.settings = Settings(self)
        self.settings.pack(anchor=tk.NW, **options)
        self.quit_button = ttk.Button(self, text="Quit", command=quit)
        self.quit_button.pack(side=tk.BOTTOM, **options)


class Settings(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # field options
        options = {'padx': 5, 'pady': 5}
        self.container = container

        self.title = ttk.Label(self, text="Settings")
        self.title.pack(**options)

        self.status = ttk.Combobox(self, values=["Watching", "Completed", "On Hold", "Dropped", "Plan to Watch"])
        self.status.pack(**options)

        self.score = ttk.Spinbox(self, from_=0, to=10)
        self.score.pack(**options)

        episodes = 24
        self.progress = ttk.Spinbox(self, from_=0, to=episodes)
        self.progress.pack(**options)

        self.add_button = ttk.Button(self, text="+")
        self.add_button.pack(side=tk.LEFT, **options)
        self.remove_button = ttk.Button(self, text="-")
        self.remove_button.pack(side=tk.RIGHT, **options)