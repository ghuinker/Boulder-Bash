from tkinter import *

class FullRoster(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.namelab = Label(self, text = "Name")
        self.namelab.grid(row=0, column=0)
