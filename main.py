import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Anime Watchlist 2")
root.geometry("300x300")

hello = ttk.Label(text="Hello world!")
hello.pack()
button = ttk.Button(text="Click me!")
button.pack()

tk.mainloop()