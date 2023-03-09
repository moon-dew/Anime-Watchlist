import tkinter as tk
from tkinter import ttk

class ListFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        options = {'padx': 5, 'pady': 5}
        self.container = container

        self.title = ttk.Label(self, text="Anime List")
        self.title.pack(**options)