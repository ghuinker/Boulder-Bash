from tkinter import *
from Leader import Leader
import xlrd
import xlsxwriter
import math

SETUP_SCORES = []
SETUP_CLIMBERS = []

ATTEMPTS = []
SCORES = []


MALE = 'm'
FEMALE = 'f'
BEGINNER = 'Beginner'
INTERMEDIATE = 'Intermediate'
ADVANCED = 'Advanced'
OPEN = 'Open'




class Dash(Frame):

    def __init__(self, master, url):
        Frame.__init__(self, master)

        self.leaderboard = []
        self.routestates = []
        self.curclimber = 0

        self.filename = url
        self.bk = xlrd.open_workbook(self.filename)
        self.setup = self.bk.sheet_by_index(0)
        self.attempts = self.bk.sheet_by_index(1)
        self.scores = self.bk.sheet_by_index(2)

        self.initSETUP_CLIMBERS()
        self.initSETUP_SCORES()
        self.initATTEMPTS()
        self.initSCORES()

        self.grid()
        self.create_widgets()

    def initroutestates(self):
        self.states = []
        for row, routes in enumerate(SETUP_SCORES):
            temp = []
            for scores in range(len(routes)):
                temp.append(BooleanVar())
            self.states.append(temp)


    def initATTEMPTS(self):
        #Add Ticks
        row = 1
        notempty = True
        global ATTEMPTS
        while(notempty):
            route = []
            empty = xlrd.empty_cell.value
            try:
                self.setup.cell(row, 0)
            except:
                break
            col = 1
            while(True):
                    try:
                        route.append(int(self.attempts.cell(row, col).value))
                        col = col+1
                    except:
                        break
            ATTEMPTS.append(route)
            row = row+1
        ATTEMPTS = ATTEMPTS[:-1]
        self.attempts = ATTEMPTS
        self.initroutestates()

    def initSCORES(self):
        #Add Scores
        row = 1
        notempty = True
        global SCORES
        while(notempty):
            route = []
            empty = xlrd.empty_cell.value
            try:
                self.scores.cell(row, 0)
            except:
                break
            col = 1
            while(True):
                    try:
                        route.append(int(self.scores.cell(row, col).value))
                        col = col+1
                    except:
                        break
            SCORES.append(route)
            row = row+1
        self.scores = SCORES


    def initSETUP_CLIMBERS(self):
        #Add SETUP_CLIMBERS
        row = 1
        notempty = True
        while(notempty):
            firstname, lastname, sex, skilllevel = '', '','',''
            empty = xlrd.empty_cell.value

            firstname = self.setup.cell(row,0).value
            lastname = self.setup.cell(row, 1).value
            sex = self.setup.cell(row, 2).value
            skilllevel = self.setup.cell(row, 3).value
            climber = [firstname + " " + lastname, sex, skilllevel, 0]
            for entry in climber:
                if entry == empty:
                    notempty = False
            if notempty == False:
                break
            else:
                SETUP_CLIMBERS.append(climber)
                row = row+1
        self.setupclimbers=SETUP_CLIMBERS

    def initSETUP_SCORES(self):
        #Add RouteSETUP_SCORES
        row = 1
        notempty = True
        while(notempty):
            route = []
            empty = xlrd.empty_cell.value
            try:
                self.setup.cell(row, 6)
            except:
                break
            col = 7
            while(True):
                    try:
                        route.append(int(self.setup.cell(row, col).value))
                        col = col+1
                    except:
                        break
            SETUP_SCORES.append(route)
            row = row+1

        self.routescorelen = len(SETUP_SCORES[0])
        self.middle = math.ceil(len(SETUP_SCORES)/2.0)
        self.setupscores=SETUP_SCORES

    def create_widgets(self):
        self.lb = Listbox(self, height= 40)
        self.lb.pack()

        for climber in SETUP_CLIMBERS:
            self.lb.insert(END, climber[0])

        self.lb.bind('<<ListboxSelect>>', self.updatePlayer)

        self.selectbutton = Button(self, text="Full Climbers", command=None)
        self.leaderbutton = Button(self, text="LeaderBoard", command=self.leaderboard)

        self.numberlabels = []
        for route in range(len(SETUP_SCORES)):
            label = Label(self, text = str(route + 1), font='Helvetica 18 bold')
            self.numberlabels.append(label)

        self.namelab = Label(self, text = "Name")
        self.sexlbl = Label(self, text="Sex")
        self.skilllbl = Label(self, text="Advanced")
        self.scorelbl = Label(self, text=str(22))


        self.scorebuts = []
        for row, routes in enumerate(SETUP_SCORES):
            temp =[]
            for col, score in enumerate(routes):
                check = Checkbutton(self, text=str(score),
                variable = self.states[row][col],
                font='Helvetica 12',
                command=self.updateATTEMPTS)
                temp.append(check)
            self.scorebuts.append(temp)




        #Add TO Grid
        self.lb.grid(row=0, column=0, rowspan=32, columnspan=2)
        self.selectbutton.grid(row=33, column=0)
        self.leaderbutton.grid(row=33, column=1)

        col = 3
        nextcol = col + self.routescorelen + 2
        row = 1
        for id, label in enumerate(self.numberlabels):
            if(id>self.middle):
                col = nextcol
                row=-self.middle
            label.grid(row=id+row, column = col)


        self.namelab.grid(row=0, column=4)
        self.sexlbl.grid(row=0, column=5)
        self.skilllbl.grid(row=0, column=6)
        self.scorelbl.grid(row=0, column=7)

        col = 4
        nextcol = nextcol + 1
        row=1
        for rowid, route in enumerate(self.scorebuts):
            for colid, check in enumerate(route):
                if(rowid>self.middle):
                    col = nextcol
                    row=-self.middle
                check.grid(row=rowid+row, column=colid+col, pady= (0,0))




    def updateATTEMPTS(self):
        None
    def updatePlayer(self, e):
        self.namelab.config(text=SETUP_CLIMBERS[self.lb.curselection()[0]][0])
        self.sexlbl.config(text=SETUP_CLIMBERS[self.lb.curselection()[0]][1])
        self.skilllbl.config(text=SETUP_CLIMBERS[self.lb.curselection()[0]][2])
        self.scorelbl.config(text=SETUP_CLIMBERS[self.lb.curselection()[0]][3])

        self.curclimber = self.lb.curselection()[0]

        ticks = ATTEMPTS[self.curclimber]
        for id,  route in enumerate(ticks):
            self.states[id][route].set(1)


    def leaderboard(self):
        #Display leaderbod
        window = Toplevel(self)
        app = Leader(window)

''' DEBUG '''
root = Tk()
root.title("PolAI")
app = Dash(root, "BB18.xlsx")
root.mainloop()
