from tkinter import *
from Leader import Leader
import xlrd
import xlsxwriter
import math

SETUP_SCORES = []
SETUP_CLIMBERS = []

TICKS = []
SCORES = []
LEADERBOARD = []


MALE = 'm'
FEMALE = 'f'
BEGINNER = 'Beginner'
INTERMEDIATE = 'Intermediate'
ADVANCED = 'Advanced'
OPEN = 'Open'




class Dash(Frame):

    def __init__(self, master, url):
        Frame.__init__(self, master)
        self.filename = url
        self.bk = xlrd.open_workbook(self.filename)
        self.setup = self.bk.sheet_by_index(0)
        self.ticks = self.bk.sheet_by_index(1)
        self.scores = self.bk.sheet_by_index(2)

        self.initSETUP_CLIMBERS()
        self.initSETUP_SCORES()
        self.initTICKS()
        self.initSCORES()

        self.grid()
        self.create_widgets()


    def initbuttonstates(self):
        None


    def initTICKS(self):
        #Add Ticks
        row = 1
        notempty = True
        global TICKS
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
                        route.append(int(self.ticks.cell(row, col).value))
                        col = col+1
                    except:
                        break
            TICKS.append(route)
            row = row+1
        TICKS = TICKS[:-1]
        self.initbuttonstates()

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
        print(SCORES)


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

    def initSETUP_SCORES(self):
        #Add RouteSETUP_SCORES
        row = 1
        notempty = True
        while(notempty):
            route = []
            empty = xlrd.empty_cell.value
            try:
                self.setup.cell(row, 5)
            except:
                break
            col = 6
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
        for id, routes in enumerate(SETUP_SCORES):
            temp =[]
            for score in routes:
                check = Checkbutton(self, text=str(score),
                variable = None, font='Helvetica 12',
                command=self.updateSETUP_SCORES)
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




    def updatePlayer(self, e):
        self.namelab.config(text=SETUP_CLIMBERS[self.lb.curselection()[0]][0])
        self.sexlbl.config(text=SETUP_CLIMBERS[self.lb.curselection()[0]][1])
        self.skilllbl.config(text=SETUP_CLIMBERS[self.lb.curselection()[0]][2])
        self.scorelbl.config(text=SETUP_CLIMBERS[self.lb.curselection()[0]][3])

        #TODO Update variables so the rest of the app knows who I am editting
    def updateSETUP_SCORES(self):
        try:
            self.ticks = self.bk.sheet_by_index(1)
        except:
            self.createTicks()


    def leaderboard(self):
        #Display leaderbod
        window = Toplevel(self)
        app = Leader(window)

''' DEBUG '''
root = Tk()
root.title("PolAI")
app = Dash(root, "BB18.xlsx")
root.mainloop()
