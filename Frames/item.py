import tkinter as tk
from tkinter import ttk
import json
from enum import Enum
from tkinter import messagebox


class EStatus(Enum):
    WATCHING = 0
    COMPLETED = 1
    ON_HOLD = 2
    DROPPED = 3
    PLAN_TO_WATCH = 4


class Item(ttk.Frame):

    def __init__(self, container, id):
        super().__init__(container)
        # field options
        options = {'padx': 5, 'pady': 5}
        self.container = container

        anilist = json.load(open("animelist.json"))
        self.item = [
            i for i in anilist['Accounts'][0]["List"] if i[0] == int(id)
        ]
        if self.item:
            self.item = self.item[0]
        masterlist = json.load(open("masterlist.json"))
        self.masteritem = [
            i for i in masterlist['List'] if i["ID"] == int(id)
        ][0]
        self.title = ttk.Label(self, text=self.masteritem["Name"])
        self.title.pack(**options)

        def quit():
            self.tabID = self.container.index("current")
            self.container.forget(self.tabID)

        self.settings = Settings(self)
        self.settings.pack(anchor=tk.NW, **options)
        self.quit_button = ttk.Button(self, text="Quit", command=quit)
        self.quit_button.pack(side=tk.BOTTOM, **options)
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


    def save(self, option, value):  
        anilist = json.load(open("animelist.json"))
        for i, e in enumerate(anilist['Accounts'][0]["List"]):
            if e[0] == self.masteritem["ID"]:
                anilist['Accounts'][0]["List"][i][option] = value
        
        json.dump(anilist, open("animelist.json", "w"), indent=4)

class Settings(ttk.LabelFrame):

    def __init__(self, container):
        super().__init__(container, text="Settings")
        # field options
        options = {'padx': 5, 'pady': 5}
        self.container = container
        self.item = self.container.item
        self.masteritem = self.container.masteritem

        self.values = [
            "Watching", "Completed", "On Hold", "Dropped", "Plan to Watch"
        ]
        self.values_enum = [
            EStatus.WATCHING, EStatus.COMPLETED, EStatus.ON_HOLD, EStatus.DROPPED, EStatus.PLAN_TO_WATCH
        ]
        def callback(event):
            self.container.save(1, self.values_enum[self.values.index(self.init_status.get())].value)
        
        self.init_status = tk.StringVar()
        self.status = ttk.Combobox(self,
                                   values=self.values,
                                   textvariable=self.init_status,
                                   width=15,
                                   state="readonly",
                                   )
        self.status.bind("<<ComboboxSelected>>", callback)
        if self.item:
            print(self.item)
            self.status.current(self.item[1])
        self.status.pack(**options)

        class Score(ttk.LabelFrame):

            def __init__(self, container):
                super().__init__(container, text="Score")
                self.container = container
                self.init_score = tk.StringVar()
                def update():
                    if not self.init_score.get() == "":
                        self.container.container.save(3, int(self.init_score.get()))
                self.score = ttk.Spinbox(self,
                                         from_=0,
                                         to=10,
                                         textvariable=self.init_score,
                                         state="readonly",
                                         width=2,
                                         command=update)
                if self.container.item:
                    self.init_score.set(self.container.item[3])
                
                self.score.pack(side=tk.LEFT, **options)
                self.max_score = ttk.Label(self, text="/10")
                self.max_score.pack(side=tk.RIGHT, **options)

        class Progress(ttk.LabelFrame):

            def __init__(self, container):
                super().__init__(container, text="Episodes")
                self.container = container
                episodes = self.container.masteritem["Episodes"]
                self.init_progress = tk.StringVar()
                def update():
                    if not self.init_progress.get() == "":
                        self.container.container.save(2, int(self.init_progress.get()))
                self.progress = ttk.Spinbox(self,
                                            from_=0,
                                            to=episodes,
                                            textvariable=self.init_progress,
                                            state="readonly",
                                            width=4,
                                            command=update)
                if self.container.item:
                    self.init_progress.set(self.container.item[2])
                self.progress.pack(side=tk.LEFT, **options)

                self.total_episodes = ttk.Label(self, text=f"/{episodes}")
                self.total_episodes.pack(side=tk.RIGHT, **options)

        self.score = Score(self)
        self.score.pack(anchor=tk.N, **options)
        self.progress = Progress(self)
        self.progress.pack(anchor=tk.S, **options)

        class AddRemove(ttk.LabelFrame):

            def __init__(self, container):
                super().__init__(container)
                self.container = container
                def add():
                    if len(self.container.item) == 0:
                        anilist = json.load(open("animelist.json"))
                        anilist['Accounts'][0]["List"].append([self.container.masteritem["ID"], self.container.values_enum[self.container.values.index(self.container.init_status.get())].value, int(self.container.progress.init_progress.get()), int(self.container.score.init_score.get())])
                        json.dump(anilist, open("animelist.json", "w"), indent=4)
                    else:
                        print("This anime is already in your list.")
                        messagebox.showerror(title="Error", message="This anime is already in your list.")

                self.add_button = ttk.Button(self, text="+", command=add)
                self.add_button.pack(side=tk.LEFT, **options)
                self.remove_button = ttk.Button(self, text="-")
                self.remove_button.pack(side=tk.RIGHT, **options)

        self.add_remove = AddRemove(self)
        self.add_remove.pack(**options)

