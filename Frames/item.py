import tkinter as tk
from tkinter import ttk

class Item(ttk.Frame):
    def __init__(self, container, name, genre, score):
        super().__init__(container)
        # field options
        options = {'padx': 5, 'pady': 5}
        self.container = container

        self.title = ttk.Label(self, text=name)
        self.title.pack(**options)
        def quit():
            self.tabID = self.container.index("current")
            self.container.forget(self.tabID)
        
        self.settings = Settings(self)
        self.settings.pack(anchor=tk.NW, **options)
        self.quit_button = ttk.Button(self, text="Quit", command=quit)
        self.quit_button.pack(side=tk.BOTTOM, **options)


class Settings(ttk.LabelFrame):
    def __init__(self, container):
        super().__init__(container, text="Settings")
        # field options
        options = {'padx': 5, 'pady': 5}
        self.container = container

        self.init_status = tk.StringVar()
        self.status = ttk.Combobox(self, values=["Watching", "Completed", "On Hold", "Dropped", "Plan to Watch"], textvariable=self.init_status, width=15, state="readonly")
        self.status.current(0)
        self.status.pack(**options)

       
        class Score(ttk.LabelFrame):
            def __init__(self, container):
                super().__init__(container)
                self.init_score = tk.StringVar()
                self.score = ttk.Spinbox(self, from_=0, to=10, textvariable=self.init_score, state="readonly", width=2)
                self.init_score.set("10")
                self.score.pack(side=tk.LEFT, **options)
                self.max_score = ttk.Label(self, text="/10")
                self.max_score.pack(side=tk.RIGHT,**options)

        class Progress(ttk.LabelFrame):
            def __init__(self, container):
                super().__init__(container)
                episodes = 24
                self.init_progress = tk.StringVar()
                self.progress = ttk.Spinbox(self, from_=0, to=episodes, textvariable=self.init_progress, state="readonly", width=4)
                self.init_progress.set("10")
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
                self.add_button = ttk.Button(self, text="+")
                self.add_button.pack(side=tk.LEFT, **options)
                self.remove_button = ttk.Button(self, text="-")
                self.remove_button.pack(side=tk.RIGHT, **options)

        self.add_remove = AddRemove(self)
        self.add_remove.pack(**options)

        #add scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)