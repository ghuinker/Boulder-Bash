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

        for i in range(0,2):
            try:
                self.filename = url
                self.bk = xlrd.open_workbook(self.filename)

                self.setupsheet = self.bk.sheet_by_index(0)
                self.initsetup()

                self.sendssheet = self.bk.sheet_by_index(2)
            except:
                self.save()

        self.initsends()

        self.attemptssheets = []
        try:
            for i in range(self.heats):
                self.attemptssheets.append(self.bk.sheet_by_index(3+i))
        except:
            self.resetattempts()

        self.initattempts()

        self.grid()
        self.create_widgets()

    def initsetup(self):
        self.initclimbers()
        self.initroutescores()
        self.initheats()

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

    def initheats(self):
        try:
            self.heats = int(self.setupsheet.cell(1,5).value)
        except:
            self.heats = 2
        self.curheat = IntVar()
        self.curheat.set(1)

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
        self.attempts = []
        for sheet in self.attemptssheets:
            self.attempts.append(self.readexcelattemptsandsends(sheet))
        self.initattemptsstates()

    '''If the correct amount of attempt sheets are not on excel then fix that'''
    def resetattempts(self):
        self.attempts=[]
        for heat in range(self.heats):
            heattemp = []
            for rows, climber in enumerate(self.climbers):
                climbertemp=[]
                for cols, el in enumerate(self.routescores):
                    climbertemp.append(0)
                heattemp.append(climbertemp)
            self.attempts.append(heattemp)
        self.save()

    '''Init states for Entry attempts'''
    def initattemptsstates(self):
        self.attemptsstates = []
        for row, routes in enumerate(self.routescores):
            var = IntVar()
            self.attemptsstates.append(var)

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

        self.leaderboardbtn = Button(self, text="LeaderBoard", command=self.leaderboard)
        self.fullroster = Button(self, text="Full Roster", command=None)

        self.routestoscore = IntVar()
        self.routestoscore.set(5)
        self.routetoscoreentry = Entry(self, textvariable=self.routestoscore, width=3)

        heatsoptions = []
        for i in range(self.heats):
            heatsoptions.append(i + 1)
        self.heatselect = OptionMenu(self, self.curheat, command=self.updateheat, *heatsoptions)

        self.updateattemptsbtn = Button(self, text="Save Attempts", command=self.updateattempts)

        self.numberlabels = []
        for route in range(len(self.routescores)):
            label = Label(self, text = str(route + 1), font='Helvetica 18 bold')
            self.numberlabels.append(label)

        self.namelab = Label(self, text = "Name")
        self.sexlbl = Label(self, text="Sex")
        self.skilllbl = Label(self, text="Advanced")
        self.scorelbl = Label(self, text=self.score)

        self.attemptentrys = []
        self.scorebuts = []

        for row, routes in enumerate(self.routescores):
            temp =[]
            self.attemptentrys.append(Entry(self,
             textvariable=self.attemptsstates[row],
              width=3))
            for col, score in enumerate(routes):
                check = Checkbutton(self, text=str(score),
                variable = self.sendstates[row][col],
                font='Helvetica 12',
                command=self.update)
                temp.append(check)
            self.scorebuts.append(temp)

        #Add TO Grid
        self.lb.grid(row=0, column=0, rowspan=32, columnspan=2)
        self.leaderboardbtn.grid(row=33, column=0)
        self.fullroster.grid(row=33, column=1)
        self.routetoscoreentry.grid(row=33, column=3)
        self.heatselect.grid(row=33, column=4)
        self.updateattemptsbtn.grid(row=33, column=5)

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
                self.attemptentrys[rowid].grid(row=rowid+row, column=colid+col+1, pady= (0,0))


    '''TODO'''
    def update(self):
        self.updatesend()
        self.updateattemptstates()
        self.updatescore()
        self.save()

    '''Accessed when heatselect is updated'''
    def updateheat(self, e):
        self.updateattemptstates()

    def updateattemptstates(self):
        for rows in self.attemptsstates:
            rows.set(0)
        climber = self.attempts[self.curheat.get()-1][self.curclimber]
        for id, route in enumerate(self.attemptsstates):
            route.set(climber[id])

    def updateattempts(self):
        if self.curclimber is not None:
            climber = self.attempts[self.curheat.get()-1][self.curclimber]
            for id, state in enumerate(self.attemptsstates):
                try:
                    climber[id] = state.get()
                    self.save()
                except:
                    None


    '''Updates the score for the person showed -- sets label at top bar for score'''
    def updatescore(self):
        self.score = 0
        if self.curclimber is not None:
            climber = self.sends[self.curclimber]

        count = 0
        for route, send in enumerate(reversed(climber)):
            add = 0
            if send != 0:
                try:
                    add = self.routescores[len(climber)-1-route][send-1]
                except:
                    add = self.routescores[len(climber)-1-route][len(self.routescores[0])-1]
                if add > 0:
                    count = count +1
            if count>self.routestoscore.get():
                break
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
        self.updateattempts()
        self.updateClimber(e)
        self.save()

    '''When a clibmer is selected in left menu --- set curclimber and bar at top to that climber'''
    def updateClimber(self, e):
        lboxfont = 17
        lboxheight = self.master.winfo_height() -20
        lboxheight = int(lboxheight/lboxfont)

        self.lb.config(height=lboxheight)
        try:
            self.namelab.config(text=self.climbers[self.lb.curselection()[0]][0])
            self.sexlbl.config(text=self.climbers[self.lb.curselection()[0]][1])
            self.skilllbl.config(text=self.climbers[self.lb.curselection()[0]][2])
            self.scorelbl.config(text=self.climbers[self.lb.curselection()[0]][3])


            self.curclimber = self.lb.curselection()[0]
        except:
            None

        for rows in self.sendstates:
            for cols in rows:
                cols.set(0)

        ticks = self.sends[self.curclimber]
        for id,  route in enumerate(ticks):
            if route == 0:
                continue
            route = route -1
            try:
                self.sendstates[id][route].set(1)
            except:
                #Setup the states if the attempts are past the checkboxes
                self.sendstates[id][len(self.sendstates[id])-1].set(1)
        self.updatescore()
        self.updateattemptstates()



    '''Save the data to excel'''
    def save(self):
        newbk = xlsxwriter.Workbook(self.filename)

        setup = newbk.add_worksheet("Setup")
        scores = newbk.add_worksheet("Scores")
        sends = newbk.add_worksheet("Sends")
        attemptheats= []
        for i in range(self.heats):
            attemptheats.append(newbk.add_worksheet("Attempts Heat " + str(i+1)))

        '''Setup Write'''
        setup.write('A1', 'First Name')
        setup.write('B1', 'Last Name')
        setup.write('C1', 'Sex')
        setup.write('D1', 'Level')

        setup.write('F1', 'Heats')
        setup.write('F2', self.heats)

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



        '''Scores Write'''
        scores.write('A1', 'Climber')
        scores.write('B1', 'Score')

        for cols in range(len(self.routescores)):
            scores.write(0, cols +2, cols+1)

        for rows, climber in enumerate(self.climbers):
            scores.write(rows+1, 0, climber[0])

        if not hasattr(self, 'sends'):
            self.sends =[]
        for id, climber in enumerate(self.sends):
            score = 0
            for route, send in enumerate(climber):
                add = 0
                if send != 0:
                    try:
                        add = self.routescores[route][send-1]
                    except:
                        add = self.routescores[route][len(self.routescores[0])-1]
                    scores.write(id+1, route + 2, add)
                score = score + add
            scores.write(id+1, 1, score)

        '''Sends Write'''
        for cols in range(len(self.routescores)):
            sends.write(0, cols +1, cols+1)

        for rows, climber in enumerate(self.climbers):
            sends.write(rows+1, 0, climber[0])

        for rows, climber in enumerate(self.sends):
            for cols, el in enumerate(climber):
                sends.write(rows+1, cols+1, el)

        '''Attempts Write'''
        for heat in range(self.heats):
            for cols in range(len(self.routescores)):
                attemptheats[heat].write(0, cols +1, cols+1)
            for rows, climber in enumerate(self.climbers):
                attemptheats[heat].write(rows+1, 0, climber[0])

        if not hasattr(self, 'attempts'):
            self.attempts =[]
        for heatid, heat in enumerate(self.attempts):
            for rows, climber in enumerate(heat):
                for cols, el in enumerate(climber):
                    attemptheats[heatid].write(rows+1, cols+1, el)



        newbk.close()

    '''Sets and creates leaderboard LeaderBoard'''
    def leaderboard(self):
        leaders = []

        for climber in self.climbers:
            leaders.append([climber[0], climber[1], climber[2]])

        for id, climber in enumerate(self.sends):
            score = 0
            count = 0
            for route, send in enumerate(reversed(climber)):
                add = 0
                if send != 0:
                    try:
                        add = self.routescores[len(climber)-1-route][send-1]
                    except:
                        add = self.routescores[len(climber)-1-route][len(self.routescores[0])-1]
                    if add > 0:
                        count = count +1
                if count>self.routestoscore.get():
                    break
                score = score + add
            leaders[id].append(score)
        window = Toplevel(self)
        app = Leader(window, leaders)




''' DEBUG'''
root = Tk()
root.title("Debugging")
app = Dash(root, "C:\\Users\\ghuin\\Personal Projects\\Excel Files\\test.xlsx")
root.mainloop()
