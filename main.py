import tkinter as tk
from tkinter import ttk
from Frames.search import Search

#Gloabl Variables
full_anime_list = ["Demon Slayer", "My Hero Academia", "Steins;Gate", "One Piece"]

#TODO: Text label to filter anime list

class MainNotebook(ttk.Notebook):
    def __init__(self, container):
        super().__init__(container)

        options = {'padx': 5, 'pady': 5}
        
        self.add(Search(self), text="Search")
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