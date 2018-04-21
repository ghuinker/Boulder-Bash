from tkinter import *
from operator import itemgetter

MALE = 0
FEMALE = 1

SEXS = [MALE, FEMALE]

BEGINNER = 0
INTERMEDIATE = 1
ADVANCED = 2
OPEN = 3

SKILLS = [OPEN, ADVANCED, INTERMEDIATE, BEGINNER]

class FullRoster(Frame):

    def __init__(self, master, leaders):
        Frame.__init__(self, master)
        self.grid()
        self.climbers = leaders
        self.leaders = [ [[], [], [], []], [[], [], [], []] ]
        self.label = [ [[], [], [], []], [[], [], [], []] ]
        self.initleaders()
        self.create_widgets()

    def create_widgets(self):
        self.male = Label(self, text = "Male", font='Helvetica 18 bold')
        self.female = Label(self, text = "Female", font='Helvetica 18 bold')
        '''
        self.lb = Listbox(self)

        for climber in self.climbers:
            self.lb.insert(END, climber[0])

        self.lb.bind('<<ListboxSelect>>', self.updateClimber)
        '''
        '''INIT Widgets'''
        self.open = Label(self, text = "Open", font='Helvetica 18 bold')
        self.advanced = Label(self, text= "Advanced", font='Helvetica 18 bold')
        self.int = Label(self, text = "Intermediate", font='Helvetica 18 bold')
        self.beg = Label(self, text = "Beginner", font='Helvetica 18 bold')

        self.lbs = []
        for i in range(8):
            self.lbs.append(Listbox(self, height=10))

        self.open1 = Label(self, text = "Open", font='Helvetica 18 bold')
        self.advanced1 = Label(self, text= "Advanced", font='Helvetica 18 bold')
        self.int1 = Label(self, text = "Intermediate", font='Helvetica 18 bold')
        self.beg1 = Label(self, text = "Beginner", font='Helvetica 18 bold')

        self.lbopen1 = Listbox(self)
        self.lbadvanced1 = Listbox(self)
        self.lbint1 = Listbox(self)
        self.lbbeg1 = Listbox(self)

        self.male.grid(row=0, column=0)
        self.female.grid(row=0, column=2)

        '''Place Labels'''
        self.open.grid(row=1, column=0)
        self.advanced.grid(row=3, column=0)
        self.int.grid(row=1, column=1)
        self.beg.grid(row=3, column=1)

        self.open1.grid(row=1, column=2)
        self.advanced1.grid(row=3, column=2)
        self.int1.grid(row=1, column=3)
        self.beg1.grid(row=3, column=3)

        count = 0
        for sex in SEXS:
            col = sex
            for skill in SKILLS:
                for climber in self.leaders[sex][skill]:
                    self.lbs[count].insert(END, str(climber[0]) +" "+ str(climber[1]))
                    col = 2*sex
                    row = 4
                    if skill == BEGINNER or skill == INTERMEDIATE:
                        col = 1 + 2*sex
                    if skill == OPEN or skill == INTERMEDIATE:
                        row = 2
                    self.lbs[count].grid(row=row, column=col)
                count = count +1

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
