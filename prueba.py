#!/usr/bin/env python
import tkinter as tk
from tkinter import ttk

def create_tab(tab_control, title):
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text=title)
    tab_control.pack(expand=1, fill="both")

root = tk.Tk()
root.title("Sistema de Pestañas")

tab_control = ttk.Notebook(root)

tab_titles = ["Pestaña 1", "Pestaña 2", "Pestaña 3"]

for title in tab_titles:
    create_tab(tab_control, title)

root.mainloop()