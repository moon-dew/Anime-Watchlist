import tkinter as tk
from tkinter import ttk
import json
import treeview_upgrade
from tkinter import messagebox
from Frames.item import Item
from mal import AnimeSearch
import threading
import time

current_call = None
rate_limit = time.perf_counter()

class RateLimitedSearch(AnimeSearch):
    def __init__(self, query, timeout=0.5):
        #create a rate limited search
        global current_call 
        global rate_limit
        current_call = query
        while time.perf_counter() - rate_limit < timeout:
            time.sleep(0.1)
        
        if current_call != query:
            return
        super().__init__(current_call)
        current_call = None
        
        rate_limit = time.perf_counter()


class Search(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)
        # field options
        options = {'padx': 5, 'pady': 5}
        self.container = container

        self.search_bar = ttk.Entry(self, text="Please input the anime name.")
        self.search_bar.pack(**options)


        self.search_bar.bind('<KeyRelease>', lambda _: threading.Thread(target=self.update).start())

        headings = ("name", "episodes", "score", "id")
        self.results = treeview_upgrade.MyTreeview(self,
                                                   columns=headings,
                                                   show="headings")
        self.results.heading("name", text="Name", sort_by="name")
        self.results.heading("episodes", text="Episodes", sort_by="num")
        self.results.heading("score", text="Average Score", sort_by="num")
        self.results.heading("id", text="ID", sort_by='num')
        self.results["displaycolumns"] = ("name", "episodes", "score")
        for i in AnimeSearch("cowboy bebop").results:
            self.results.insert("",
                                "end",
                                values=(i.title, i.episodes, i.score, i.mal_id))
        self.results.pack(**options)
        # add a scrollbar
        self.scrollbar = ttk.Scrollbar(self,
                                       orient=tk.VERTICAL,
                                       command=self.results.yview)
        self.results.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results.bind('<<TreeviewSelect>>', lambda _: threading.Thread(target=self.item_selected).start())

    def item_selected(self):
        item = self.results.selection()[0]
        self.container.add(Item(self.container,
                                self.results.item(item, "values")[3]),
                           text=self.results.item(item, "values")[0])

    def update(self):
        self.results.delete(*self.results.get_children())
        try:
            search = RateLimitedSearch(self.search_bar.get())
            for i in search.results:
                #add to tree
                self.results.insert("",
                                    "end",
                                    values=(i.title, i.episodes, i.score, i.mal_id))
        except Exception as e:
            pass