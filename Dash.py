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

        self.curclimber = 0
        self.score = 0

        self.filename = url
        self.bk = xlrd.open_workbook(self.filename)
        self.setupsheet = self.bk.sheet_by_index(0)
        self.sendssheet = self.bk.sheet_by_index(1)
        self.scoressheet = self.bk.sheet_by_index(2)

        self.initclimbers()
        self.routescores()
        self.initsend()
        self.initSCORES()

        self.grid()
        self.create_widgets()


    '''Init checkboxes states array with a mutable boolean var sets self.sendstates'''
    def initsendstates(self):
        self.sendstates = []
        for row, routes in enumerate(self.routescores):
            temp = []
            for scores in range(len(routes)):
                temp.append(BooleanVar())
            self.sendstates.append(temp)

    '''Read Excel sheet to get send climb of climbers Sets self.sends'''
    def initsends(self):
        #Add Ticks
        row = 1
        notempty = True

        self.attempts = []

        for row in range(len(self.climbers)):
            route = []
            runs = []

            for col in range(len(self.routescores)):
                try:
                    route.append(int(self.sends.cell(row+1, col+1).value))
                except:
                    route.append(0)
                var = IntVar()
                var.set(0)
                runs.append(var)

            self.sends.append(route)
            self.attempts.append(runs)
        self.initsendstates()

    '''Setup climbing roster sets self.climbers'''
    def initinitclimbers(self):

        empty = xlrd.empty_cell.value
        set = self.setupsheet

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

    '''Creates widgets within tkinter screen'''
    def create_widgets(self):
        self.lb = Listbox(self, height= 40)
        self.lb.pack()

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


        for id, climber in enumerate(self.attempts):
            for row, route in enumerate(climber):
                min = len(self.routescores[0])

                attemptmenu = OptionMenu(self, self.attempts[id][row],0,
                 min+1, min+2, min+3, min+4, min+5, min+7, min+8, min+9, min+10,
                 min+11, min+12, min+13, min+14, min+15, min+17, min+18, min+19, min+20,
                 command=self.updateextraruns)
                runs.append(attemptmenu)
            self.attemptmenus.append(runs)


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
                self.attemptmenus[0][0].grid(row=rowid+row-1, column=colid+col+1, pady= (0,0))


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

                    if(self.attempts[self.curclimber][row].get() != 0):
                        climber[row] = self.attempts[self.curclimber][row].get()

                if(falseroutes == col+1):
                    climber[row] = 0

    '''TODO'''
    def updateextraruns(self, e):
        self.updatesend()
        self.updateClimber(e)

        self.save()

    '''When a clibmer is selected in left menu --- set curclimber and bar at top to that climber'''
    def updateClimber(self, e):
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
            self.attempts[self.curclimber][id].set(0)
            try:
                self.sendstates[id][route].set(1)
            except:
                #Setup the states if the attempts are past the checkboxes
                min = len(self.routescores[0])
                self.attempts[self.curclimber][id].set(route+1)
                self.sendstates[id][len(self.sendstates[id])-1].set(1)
        self.updatescore()


    '''Save the data to excel'''
    def save(self):

        debugsave = "testfile.xlsx"

        newbk = xlsxwriter.Workbook(self.filename)

        setup = newbk.add_worksheet("Setup")
        attempts = newbk.add_worksheet("Attempts")
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

        '''Attempts Write'''
        attempts.write('A1', 'Climber')

        for cols in range(len(self.routescores)):
            attempts.write(0, cols +1, cols+1)

        for rows, climber in enumerate(self.climbers):
            attempts.write(rows+1, 0, climber[0])

        for rows, climber in enumerate(self.sends):
            for cols, el in enumerate(climber):
                attempts.write(rows+1, cols+1, el)

                if self.attempts[rows][cols].get() != 0:
                    attempts.write(rows+1, cols+1, self.attempts[rows][cols].get())

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
app = Dash(root, "test.xlsx")
root.mainloop()
