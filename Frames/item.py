import tkinter as tk
from tkinter import ttk

class Item(ttk.Frame):
    def __init__(self, container, name, genre, score):
        super().__init__(container)
        # field options
        options = {'padx': 5, 'pady': 5}
        self.container = container

        self.name = ttk.Label(self, text=name)
        self.name.pack(**options)

        self.quit_button = ttk.Button(self, text="Quit", command=self.container.forget(self))
        self.quit_button.pack(**options)