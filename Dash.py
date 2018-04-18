from tkinter import *
from Leader import Leader
import xlrd
import xlsxwriter
import math

MALE = 'm'
FEMALE = 'f'
BEGINNER = 'Beginner'
INTERMEDIATE = 'Intermediate'
ADVANCED = 'Advanced'
OPEN = 'Open'




class Dash(Frame):

    def __init__(self, master, url):
        Frame.__init__(self, master)

        self.master = master

        self.curclimber = 0
        self.score = 0

        self.filename = url
        self.bk = xlrd.open_workbook(self.filename)
        self.setupsheet = self.bk.sheet_by_index(0)
        self.sendssheet = self.bk.sheet_by_index(1)
        self.scoressheet = self.bk.sheet_by_index(2)
        self.attemptssheet = self.bk.sheet_by_index(3)

        self.initclimbers()
        self.initroutescores()
        self.initsends()
        self.initattempts()

        self.grid()
        self.create_widgets()

    '''Setup climbing roster sets self.climbers'''
    def initclimbers(self):

        empty = xlrd.empty_cell.value
        set = self.setupsheet
        self.climbers = []
        row = 1

        while(True):
            try:
                if set.cell(row,0).value ==empty:
                    break
            except:
                break
            else:
                self.climbers.append(
                [set.cell(row,0).value + " " + set.cell(row,1).value,
                 set.cell(row,2).value, set.cell(row,3).value, 0]  )
                row = row +1

    '''Sets up what the user added in setup excel for route section sets self.routescores'''
    def initroutescores(self):
        self.routescores = []
        row = 1
        notempty = True
        while(notempty):
            route = []
            empty = xlrd.empty_cell.value
            try:
                self.setupsheet.cell(row, 6)
            except:
                break
            col = 7
            while(True):
                    try:
                        route.append(int(self.setupsheet.cell(row, col).value))
                        col = col+1
                    except:
                        break
            if not not route:
                self.routescores.append(route)
            row = row+1

    '''Init self.sends'''
    def initsends(self):
        self.sends = self.readexcelattemptsandsends(self.sendssheet)
        self.initsendstates()

    '''Init checkboxes states array with a mutable boolean var sets self.sendstates'''
    def initsendstates(self):
        self.sendstates = []
        for row, routes in enumerate(self.routescores):
            temp = []
            for scores in range(len(routes)):
                temp.append(BooleanVar())
            self.sendstates.append(temp)

    '''Init self.attempts'''
    def initattempts(self):
        self.attempts = self.readexcelattemptsandsends(self.attemptssheet)
        self.initattemptsstates()

    '''Init states for drop down menu attempts'''
    def initattemptsstates(self):
        self.attemptsstates = []

    '''Read excel for attempts and sends and return resulting array'''
    def readexcelattemptsandsends(self, sheet):
        arr = []
        row = 1
        notempty = True
        for row in range(len(self.climbers)):
            route = []

            for col in range(len(self.routescores)):
                try:
                    route.append(int(sheet.cell(row+1, col+1).value))
                except:
                    route.append(0)
            arr.append(route)
        return arr

    '''Creates widgets within tkinter screen'''
    def create_widgets(self):

        self.lb = Listbox(self)

        for climber in self.climbers:
            self.lb.insert(END, climber[0])

        self.lb.bind('<<ListboxSelect>>', self.updateClimber)

        self.selectbutton = Button(self, text="LeaderBoard", command=self.leaderboard)
        self.leaderbutton = Button(self, text="Full Roster", command=None)

        self.numberlabels = []
        for route in range(len(self.routescores)):
            label = Label(self, text = str(route + 1), font='Helvetica 18 bold')
            self.numberlabels.append(label)

        self.namelab = Label(self, text = "Name")
        self.sexlbl = Label(self, text="Sex")
        self.skilllbl = Label(self, text="Advanced")
        self.scorelbl = Label(self, text=self.score)

        self.attemptmenus = []
        self.scorebuts = []

        for row, routes in enumerate(self.routescores):

            temp =[]
            runs = []

            for col, score in enumerate(routes):
                check = Checkbutton(self, text=str(score),
                variable = self.sendstates[row][col],
                font='Helvetica 12',
                command=self.update)
                temp.append(check)
            self.scorebuts.append(temp)

        #Add TO Grid
        self.lb.grid(row=0, column=0, rowspan=32, columnspan=2)
        self.selectbutton.grid(row=33, column=0)
        self.leaderbutton.grid(row=33, column=1)

        routescorelen = len(self.routescores[0])
        middle = math.ceil(len(self.routescores)/2.0)

        first = math.ceil(len(self.routescores)/3.0)
        second = first + first

        col = 3
        nextcol = col + routescorelen + 2
        thirdcol = nextcol + routescorelen + 2
        row = 1
        for id, label in enumerate(self.numberlabels):

            if(id>first):
                col = nextcol
                row =-first
            if(id>second):
                col = thirdcol+1
                row = -second
            label.grid(row=id+row, column = col)


        self.namelab.grid(row=0, column=4)
        self.sexlbl.grid(row=0, column=5)
        self.skilllbl.grid(row=0, column=6)
        self.scorelbl.grid(row=0, column=7)

        col = 4
        nextcol = nextcol + 1
        thirdcol = thirdcol + 1
        row=1
        for rowid, route in enumerate(self.scorebuts):
            for colid, check in enumerate(route):

                if(rowid>first):
                    col = nextcol +1
                    row =-first

                if(rowid>second):
                    col = thirdcol +1
                    row = -second
                check.grid(row=rowid+row, column=colid+col, pady= (0,0))


    '''TODO'''
    def update(self):
        self.updatesend()
        self.updatescore()
        self.save()

    '''Updates the score for the person showed -- sets label at top bar for score'''
    def updatescore(self):
        self.score = 0
        if self.curclimber is not None:
            climber = self.sends[self.curclimber]

        for route, attempt in enumerate(climber):
            add = 0
            if attempt != 0:
                try:
                    add = self.routescores[route][attempt-1]
                except:
                    add = self.routescores[route][len(self.routescores[0])-1]
            self.score = self.score + add
        self.scorelbl.config(text=str(self.score))

    '''Updates the sends of climber when checkbox is clicked'''
    def updatesend(self):
        if self.curclimber is not None:
            climber = self.sends[self.curclimber]
            for row, routes in enumerate(self.sendstates):
                falseroutes = 0

                for col, state in enumerate(routes):
                    if routes[col].get() == True:
                        climber[row] = col +1
                    else:
                        falseroutes = falseroutes +1
                if(falseroutes == col+1):
                    climber[row] = 0


    '''TODO'''
    def updateextraruns(self, e):
        self.updatesend()
        self.updateClimber(e)

        self.save()

    '''When a clibmer is selected in left menu --- set curclimber and bar at top to that climber'''
    def updateClimber(self, e):
        lboxfont = 17
        lboxheight = self.master.winfo_height() -20
        lboxheight = int(lboxheight/lboxfont)


        self.lb.config(height=lboxheight)
        self.namelab.config(text=self.climbers[self.lb.curselection()[0]][0])
        self.sexlbl.config(text=self.climbers[self.lb.curselection()[0]][1])
        self.skilllbl.config(text=self.climbers[self.lb.curselection()[0]][2])
        self.scorelbl.config(text=self.climbers[self.lb.curselection()[0]][3])

        self.curclimber = self.lb.curselection()[0]

        for rows in self.sendstates:
            for cols in rows:
                cols.set(0)

        ticks = self.sends[self.curclimber]
        for id,  route in enumerate(ticks):
            if route == 0:
                continue
            route = route -1
            self.sendstates[self.curclimber][id].set(0)
            try:
                self.sendstates[id][route].set(1)
            except:
                #Setup the states if the attempts are past the checkboxes
                self.sendstates[id][len(self.sendstates[id])-1].set(1)
        self.updatescore()


    '''Save the data to excel'''
    def save(self):

        debugsave = "testfile.xlsx"

        newbk = xlsxwriter.Workbook(self.filename)

        setup = newbk.add_worksheet("Setup")
        sends = newbk.add_worksheet("Send Attempt")
        scores = newbk.add_worksheet("Scores")
        LeaderBoard = newbk.add_worksheet("LeaderBoard")

        '''Setup Write'''
        setup.write('A1', 'First Name')
        setup.write('B1', 'Last Name')
        setup.write('C1', 'Sex')
        setup.write('D1', 'Level')

        setup.write('G1', 'Route')
        setup.write('H1', 'Scores')

        for rows, climber in enumerate(self.climbers):
            for cols, el in enumerate(climber):
                if cols ==0:
                    names = el.split(" ")
                    for namecol, name in enumerate(names):
                        setup.write(rows +1, cols+namecol, name)
                else:
                    setup.write(rows +1, cols+1, el)

        for rows, routes in enumerate(self.routescores):
            rows = rows + 1
            setup.write(rows, 6, rows)
            for cols, score in enumerate(routes):
                setup.write(rows, cols + 7, score)

        '''Sends Write'''
        sends.write('A1', 'Climber')

        for cols in range(len(self.routescores)):
            sends.write(0, cols +1, cols+1)

        for rows, climber in enumerate(self.climbers):
            sends.write(rows+1, 0, climber[0])

        for rows, climber in enumerate(self.sends):
            for cols, el in enumerate(climber):
                sends.write(rows+1, cols+1, el)
                
        '''Scores Write'''
        scores.write('A1', 'Climber')
        scores.write('B1', 'Score')

        for cols in range(len(self.routescores)):
            scores.write(0, cols +2, cols+1)

        for rows, climber in enumerate(self.climbers):
            scores.write(rows+1, 0, climber[0])

        for id, climber in enumerate(self.sends):
            score = 0
            for route, attempt in enumerate(climber):
                add = 0
                if attempt != 0:
                    try:
                        add = self.routescores[route][attempt-1]
                    except:
                        add = self.routescores[route][len(self.routescores[0])-1]
                    scores.write(id+1, route + 2, add)
                score = score + add
            scores.write(id+1, 1, score)




        '''LeaderBoard Write'''

        newbk.close()

    '''Sets and creates leaderboard LeaderBoard'''
    def leaderboard(self):
        leaders = []

        for climber in self.climbers:
            leaders.append([climber[0], climber[1], climber[2]])

        for id, climber in enumerate(self.sends):
            score = 0
            for route, attempt in enumerate(climber):
                add = 0
                if attempt != 0:
                    try:
                        add = self.routescores[route][attempt-1]
                    except:
                        add = self.routescores[route][len(self.routescores[0])-1]
                score = score + add
            leaders[id].append(score)

        window = Toplevel(self)
        app = Leader(window, leaders)


''' DEBUG'''
root = Tk()
root.title("Debugging")
app = Dash(root, "bbtest.xlsx")
root.mainloop()
