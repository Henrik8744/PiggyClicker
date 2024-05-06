import tkinter
import customtkinter as ct
from tkinter import *
from PIL import Image

ct.set_appearance_mode("dark")
ct.set_default_color_theme("dark-blue")

length_to_width = 1000/1920

root_tk = tkinter.Tk()
root_tk.geometry("1920x1000")
root_tk.title("Piggy Clicker")

def button_function():
    print("button pressed")

my_image = ct.CTkImage(dark_image=Image.open("ImageFiles\Pig.png"), size=(500,500)) #Width by height
 
# Use CTkButton instead of tkinter Button
button = ct.CTkButton(master=root_tk, text="",image=my_image, corner_radius=5, command=button_function, fg_color="transparent", hover_color="green")
button.place(relx=.01 * length_to_width, rely=.01, anchor="nw")

root_tk.mainloop()