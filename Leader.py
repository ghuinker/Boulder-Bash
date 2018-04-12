from tkinter import *

class Leader(Frame):

    def __init__(self, master, leaders):
        Frame.__init__(self, master)
        self.grid()
        self.climbers = leaders
        self.leaders = [ [[], [], [], []], [[], [], [], []] ]
        self.initleaders()
        self.create_widgets()

    def create_widgets(self):
        self.male = Label(self, text = "Male")
        self.female = Label(self, text = "Female")
        self.open = Label(self, text = "Open")
        self.advanced = Label(self, text= "Advanced")
        self.int = Label(self, text = "Intermediate")
        self.beg = Label(self, text = "Beginner")


    def initleaders(self):
        sex = 0
        skill = 0
        for climbers in self.climbers:
            if climbers[1].lower() == 'f' or climbers[1] == 'female':
                sex = 1
            if climbers[2].lower() == 'intermediate':
                skill = 1
            if climbers[2].lower() == 'advanced':
                skill = 2
            if climbers[2].lower() == 'open':
                skill = 3

            self.leaders[sex][skill].append([climbers[0], climbers[3]])

        print(self.leaders)

    def sort(self):
        sorted(self.leaders, key=self.getKey)

    def getKey(self, item):
        return item[1]
