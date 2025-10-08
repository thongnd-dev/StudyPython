from tkinter import *
from tkinter.ttk import *
from time import strftime

root= Tk()
root.title("Digital Clok")

def clock():
    string = strftime('%I:%M:%S')
    label.config(text=string)
    label.after(1000,clock)

label = Label(root,font=("Tahoma",100), background="black",foreground="red")
label.pack(anchor='center')
clock()
root.mainloop()