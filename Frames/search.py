import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

class Search(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # field options
        options = {'padx': 5, 'pady': 5}

        self.search_bar = ttk.Entry(self, text="Please input the anime name.")
        self.search_bar.pack(**options)

        def update(self):
            showinfo("Testing", "testing")
            
        self.search_bar.bind('<KeyRelease>', update)

        headings = ("name", "date")
        self.results = ttk.Treeview(self, columns=headings, show="headings")
        self.results.heading("name", text="Name")
        self.results.heading("date", text="Release Date")
        self.results.pack(**options)