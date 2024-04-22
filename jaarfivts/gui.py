# Python tkinter hello world program

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import fun2
import time
import asyncio

root = tk.Tk()

root.geometry("500x500")
a = ttk.Label(root, text="Hello World")
flip = ttk.Button(
    root, command=lambda: fun2.loop.create_task(fun2.fun.flip(fun2.request_queue))
)
rainbow = ttk.Button(
    root, command=lambda: fun2.loop.create_task(fun2.fun.rainbow(fun2.request_queue))
)
a.pack()
flip.pack()
rainbow.pack()

root.mainloop()
