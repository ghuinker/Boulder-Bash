from tkinter import *
from operator import itemgetter

MALE = 0
FEMALE = 1

BEGINNER = 0
INTERMEDIATE = 1
ADVANCED = 2
OPEN = 3

class Leader(Frame):

    def __init__(self, master, leaders):
        Frame.__init__(self, master)
        self.grid()
        self.climbers = leaders
        self.leaders = [ [[], [], [], []], [[], [], [], []] ]
        self.label = [ [[], [], [], []], [[], [], [], []] ]
        self.initleaders()
        self.create_widgets()

    def create_widgets(self):
        self.male = Label(self, text = "Male")
        self.female = Label(self, text = "Female")

        self.open = Label(self, text = "Open")
        self.advanced = Label(self, text= "Advanced")
        self.int = Label(self, text = "Intermediate")
        self.beg = Label(self, text = "Beginner")

        self.open1 = Label(self, text = "Open")
        self.advanced1 = Label(self, text= "Advanced")
        self.int1 = Label(self, text = "Intermediate")
        self.beg1 = Label(self, text = "Beginner")

        self.male.grid(row=0, column=0)
        self.female.grid(row=0, column=4)


        '''Male'''
        self.open.grid(row=1, column=0)
        try:
            for i in range(5):
                Label(self, text = self.leaders[MALE][OPEN][i]).grid(row=2+i, column=0)
        except:
            print("Not Enough Male Open")

        self.advanced.grid(row=7, column=0)
        try:
            for i in range(5):
                Label(self, text = self.leaders[MALE][ADVANCED][i]).grid(row=8+i, column=0)
        except:
            print("Not Enough Male ADVANCED")

        self.int.grid(row=1, column=3)
        try:
            for i in range(5):
                Label(self, text = self.leaders[MALE][INTERMEDIATE][i]).grid(row=2+i, column=3)
        except:
            print("Not Enough Male INTERMEDIATE")

        self.beg.grid(row=7, column=3)
        try:
            for i in range(5):
                Label(self, text = self.leaders[MALE][BEGINNER][i]).grid(row=8+i, column=3)
        except:
            print("Not Enough Male BEGINNER")




        '''Female'''
        self.open1.grid(row=1, column=4)
        try:
            for i in range(5):
                Label(self, text = self.leaders[FEMALE][OPEN][i]).grid(row=2+i, column=4)
        except:
            print("Not Enough Female OPEN")

        self.advanced1.grid(row=7, column=4)
        try:
            for i in range(5):
                Label(self, text = self.leaders[FEMALE][ADVANCED][i]).grid(row=8+i, column=4)
        except:
            print("Not Enough Female ADVANCED")

        self.int1.grid(row=1, column=7)
        try:
            for i in range(5):
                Label(self, text = self.leaders[FEMALE][INTERMEDIATE][i]).grid(row=2+i, column=7)
        except:
            print("Not Enough Female INTERMEDIATE")

        self.beg1.grid(row=7, column=7)
        try:
            for i in range(5):
                Label(self, text = self.leaders[FEMALE][BEGINNER][i]).grid(row=8+i, column=7)
        except:
            print("Not Enough Female BEGINNER")






    def debug(self):


        self.leaders[MALE][BEGINNER].append(["MALE", "BEGINNER"])
        self.leaders[MALE][INTERMEDIATE].append(["MALE", "INTERMEDIATE"])
        self.leaders[MALE][ADVANCED].append(["MALE", "ADVANCED"])
        self.leaders[MALE][OPEN].append(["MALE", "OPEN"])
        self.leaders[MALE][OPEN].append(["MALE", "SECONDOPEN"])

        self.leaders[FEMALE][BEGINNER].append(["FEMALE", "BEGINNER"])
        self.leaders[FEMALE][INTERMEDIATE].append(["FEMALE", "INTERMEDIATE"])
        self.leaders[FEMALE][ADVANCED].append(["FEMALE", "ADVANCED"])
        self.leaders[FEMALE][OPEN].append(["FEMALE", "OPEN"])



    def initleaders(self):

        MALE = 0
        FEMALE = 1

        BEGINNER = 0
        INTERMEDIATE = 1
        ADVANCED = 2
        OPEN = 3

        for climber in self.climbers:
            sex = MALE
            skill = BEGINNER

            if climber[1].lower() == 'f':
                sex = FEMALE
            if climber[2].lower() == 'intermediate':
                skill = INTERMEDIATE
            elif climber[2].lower() == 'advanced':
                skill = ADVANCED
            elif climber[2].lower() == 'open':
                skill = OPEN
            self.leaders[sex][skill].append([climber[0], climber[3]])

        for sex in self.leaders:
            for skill in sex:
                if not not skill:
                    skill = skill.sort(key = lambda x: x[1], reverse=True)
