import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import json

class Search(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # field options
        options = {'padx': 5, 'pady': 5}

        self.search_bar = ttk.Entry(self, text="Please input the anime name.")
        self.search_bar.pack(**options)

        def update(event):
            self.results.delete(*self.results.get_children())
            j = json.load(open("animelist.json"))
            matches = []
            for i in j["List"]:
                if self.search_bar.get().lower() in i["Name"].lower():
                    if i["Name"].lower().startswith(self.search_bar.get().lower()):
                        self.results.insert("", "end", values=(i["Name"], i["Genre"], i['Rating']))
                    else:
                        matches.append(i)
            for i in matches:
                self.results.insert("", "end", values=(i["Name"], i["Genre"], i['Rating']))
        self.search_bar.bind('<KeyRelease>', update)

        headings = ("name", "genre", "score")
        self.results = ttk.Treeview(self, columns=headings, show="headings")
        self.results.heading("name", text="Name")
        self.results.heading("genre", text="Genre")
        self.results.heading("score", text="Score")
        j = json.load(open("animelist.json"))
        for i in j["List"]:
            self.results.insert("", "end", values=(i["Name"], i["Genre"], i['Rating']))
        self.results.pack(**options)