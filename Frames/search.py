import tkinter as tk
from tkinter import ttk
import json
import treeview_upgrade

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
        self.results = treeview_upgrade.MyTreeview(self, columns=headings, show="headings")
        self.results.heading("name", text="Name", sort_by="name")
        self.results.heading("genre", text="Genre", sort_by="name")
        self.results.heading("score", text="Score", sort_by="num")
        j = json.load(open("animelist.json"))
        for i in j["List"]:
            self.results.insert("", "end", values=(i["Name"], i["Genre"], i['Rating']))
        self.results.pack(**options)
        # add a scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.results.yview)
        self.results.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)