import tkinter as tk
from tkinter import ttk
import json
import treeview_upgrade
from tkinter import messagebox
from Frames.item import Item


class Search(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)
        # field options
        options = {'padx': 5, 'pady': 5}
        self.container = container

        self.search_bar = ttk.Entry(self, text="Please input the anime name.")
        self.search_bar.pack(**options)
        self.anime_list = json.load(open("masterlist.json"))
        self.search_bar.bind('<KeyRelease>', self.update)

        headings = ("name", "genre", "score", "id")
        self.results = treeview_upgrade.MyTreeview(self,
                                                   columns=headings,
                                                   show="headings")
        self.results.heading("name", text="Name", sort_by="name")
        self.results.heading("genre", text="Genre", sort_by="name")
        self.results.heading("score", text="Average Score", sort_by="num")
        self.results.heading("id", text="ID", sort_by='num')
        self.results["displaycolumns"] = ("name", "genre", "score")
        j = self.anime_list
        for i in j["List"]:
            self.results.insert("",
                                "end",
                                values=(i["Name"], i["Genre"], i['Rating'],
                                        i["ID"]))
        self.results.pack(**options)
        # add a scrollbar
        self.scrollbar = ttk.Scrollbar(self,
                                       orient=tk.VERTICAL,
                                       command=self.results.yview)
        self.results.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results.bind('<<TreeviewSelect>>', self.item_selected)

    def update(self, event):
        self.results.delete(*self.results.get_children())
        j = self.anime_list
        matches = []
        for i in j["List"]:
            if self.search_bar.get().lower() in i["Name"].lower():
                if i["Name"].lower().startswith(self.search_bar.get().lower()):
                    self.results.insert("",
                                        "end",
                                        values=(i["Name"], i["Genre"],
                                                i['Rating']))
                else:
                    matches.append(i)
        for i in matches:
            self.results.insert("",
                                "end",
                                values=(i["Name"], i["Genre"], i['Rating']))

    def item_selected(self, event):
        item = self.results.selection()[0]
        self.container.add(Item(self.container,
                                self.results.item(item, "values")[3]),
                           text="Item")
