import tkinter as tk
from tkinter import ttk
from Frames.search import Search
from Frames.list import ListFrame
from Frames.accounts import Accounts
from tkinter import messagebox


class MainNotebook(ttk.Notebook):
    def __init__(self, container):
        super().__init__(container)

        self.account = 0

        options = {'padx': 5, 'pady': 5}
        
        self.add(Accounts(self), text="Accounts")
        self.add(Search(self), text="Search")
        self.add(ListFrame(self), text="List")
        self.pack(**options)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        #_configure_the_root_window
        self.title('Anime Watchlist')
        self.geometry('400x280')

if __name__ == "__main__":
    app = App()

    notebook = MainNotebook(app)
    app.mainloop()
    # style = ttk.Style(app)
    # style.theme_use("aqua")

#the rating to hide: "Rx - Hentai"

#animelist.json is a json file with the following format:
#ID
#Status
#Progress
#Score