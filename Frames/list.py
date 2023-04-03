import tkinter as tk
from tkinter import ttk
from treeview_upgrade import MyTreeview
import json
from mal import Anime
from Frames.item import Item
import threading
from animecache import get_cached_anime

class ListFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        options = {'padx': 5, 'pady': 5}
        self.container = container
        self.load()
    
    def load(self):
        options = {'padx': 5, 'pady': 5}
        #delete all children
        for i in self.winfo_children():
            i.destroy()
        self.personal_list = json.load(open("animelist.json"))
        self.personal_list = self.personal_list["Accounts"][self.container.account]["List"]


        self.title = ttk.Label(self, text="Anime List")
        self.title.pack(**options)

        self.category_buttons = self.CategoryButtons(self)
        self.category_buttons.pack(**options)

        columns = ("name", "episodes", "score", "status", "id")
        self.anilist = MyTreeview(self, columns=columns, show="headings")
        self.anilist.heading("name", text="Name", sort_by="name")
        self.anilist.heading("episodes", text="Episodes", sort_by="name")
        self.anilist.heading("score", text="Score", sort_by="num")
        self.anilist.heading("status", text="Status", sort_by="name")
        self.anilist.heading("id", text="ID", sort_by="num")
        self.anilist["displaycolumns"] = ("name", "episodes", "score", "status")

        self.adjusted_list = []
        scores = []
        status = []
        for i, j in enumerate(self.personal_list):
            self.adjusted_list.append(get_cached_anime(j[0]))
            scores.append(self.personal_list[i][3])
            status.append(self.personal_list[i][1])
    
        status = list(map(lambda x: ["Watching", "Completed", "On Hold", "Dropped", "Plan to Watch"][x], status))
        self.adjusted_list = list(zip(self.adjusted_list, scores, status))[:]

        for i, j, k in self.adjusted_list:
            self.anilist.insert("", "end", values=(i.title, i.episodes, j, k, i.mal_id))

        self.anilist.bind('<<TreeviewSelect>>', lambda _: threading.Thread(target=self.item_selected).start())
        self.anilist.pack(**options)
    
    def item_selected(self):
        if not self.anilist.selection():
            return
        item = self.anilist.selection()[0]
        self.container.add(Item(self.container,
                                self.anilist.item(item, "values")[4]),
                           text=self.anilist.item(item, "values")[0])
    
    class CategoryButtons(ttk.LabelFrame):
        def __init__(self, container, *args, **kwargs):
            super().__init__(container, *args, **kwargs)
            options = {'padx': 5, 'pady': 5}
            self.container = container
            self.title = ttk.Label(self, text="Categories")
            self.title.pack(**options)
            self.buttons = []
            self.category = tk.IntVar()
            categories = [("All", 5), ("Watching", 0), ("Completed", 1), ("On Hold", 2), ("Dropped", 3), ("Plan to Watch", 4)]
            for i in categories:
                self.buttons.append(ttk.Radiobutton(self, text=i[0], variable=self.category, value=i[1], command=self.callback))
                self.buttons[-1].pack(side=tk.LEFT, **options)
            
            self.category.set(5)

            #erase all items in treeview
            #add items that match category
        def callback(self):
            self.container.anilist.delete(*self.container.anilist.get_children())
            for i in list(self.container.adjusted_list):
                i = i[0]
                adjusted_list = list(filter(lambda x: x[0] == i.mal_id, self.container.personal_list))
                adjusted = adjusted_list[0]
                if self.category.get() == 5:
                    j = ["Watching", "Completed", "On Hold", "Dropped", "Plan to Watch"][adjusted[1]]
                    k = adjusted[3]
                    self.container.anilist.insert("", "end", values=(i.title, i.episodes, k, j, i.mal_id))

                if adjusted[1] == self.category.get():
                    j = ["Watching", "Completed", "On Hold", "Dropped", "Plan to Watch"][adjusted[1]]
                    k = adjusted[3]
                    self.container.anilist.insert("", "end", values=(i.title, i.episodes, k, j, i.mal_id))

        