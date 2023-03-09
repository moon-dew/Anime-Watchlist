import tkinter as tk
from tkinter import ttk
from treeview_upgrade import MyTreeview
import json

class ListFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        options = {'padx': 5, 'pady': 5}
        self.container = container
        self.anime_list = json.load(open("masterlist.json"))
        self.personal_list = json.load(open("animelist.json"))

        self.title = ttk.Label(self, text="Anime List")
        self.title.pack(**options)

        columns = ("name", "genre", "score")
        self.anilist = MyTreeview(self, columns=columns, show="headings")
        self.anilist.heading("name", text="Name", sort_by="name")
        self.anilist.heading("genre", text="Genre", sort_by="name")
        self.anilist.heading("score", text="Score", sort_by="num")

        self.adjusted_list = [i for i in self.anime_list["List"] if i["ID"] in [j[0] for j in self.personal_list["Accounts"][0]["List"]]]
        scores = [j[1] for j in self.personal_list["Accounts"][0]["List"]]
        self.adjusted_list = zip(self.adjusted_list, scores)
        
        for i, j in self.adjusted_list:
            self.anilist.insert("", "end", values=(i["Name"], i["Genre"], j))

        self.anilist.pack(**options)