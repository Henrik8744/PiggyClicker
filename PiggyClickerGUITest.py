import tkinter
import customtkinter as ct
from tkinter import *

root_tk = tkinter.Tk()
root_tk.geometry("1920x1000")
root_tk.title("CustomTkinter Test")

def button_function():
    print("button pressed")

pig_btn = PhotoImage(file='ImageFiles\Pig.png')

# Use CTkButton instead of tkinter Button
button = ct.CTkButton(master=root_tk, image=pig_btn, corner_radius=10, command=button_function)
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

root_tk.mainloop()