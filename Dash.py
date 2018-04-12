from tkinter import *
from Leader import Leader
import xlrd, xlwt
import math

COLUMNS = 6
ROWS = 35
SCORES = []


MALE = 'm'
FEMALE = 'f'
BEGINNER = 'Beginner'
INTERMEDIATE = 'Intermediate'
ADVANCED = 'Advanced'
OPEN = 'Open'

'''
CLIMBERS = [["Gabe Huinker", MALE, ADVANCED,0], ["Lydia Heydlauff",FEMALE, OPEN,1]]
'''
CLIMBERS = []


WORKBOOKFILENAME = 'BB18.xlsx'


"""Read and Stuff From Excell"""

bk = xlrd.open_workbook(WORKBOOKFILENAME)
setup = bk.sheet_by_index(0)

#Add Climbers
row = 1
notempty = True
while(notempty):
    firstname, lastname, sex, skilllevel = '', '','',''
    empty = xlrd.empty_cell.value

    firstname = setup.cell(row,0).value
    lastname = setup.cell(row, 1).value
    sex = setup.cell(row, 2).value
    skilllevel = setup.cell(row, 3).value
    climber = [firstname + " " + lastname, sex, skilllevel, 0]
    for entry in climber:
        if entry == empty:
            notempty = False
    if notempty == False:
        break
    else:
        CLIMBERS.append(climber)
        row = row+1

#Add RouteScores
row = 1
notempty = True
while(notempty):
    route = []
    empty = xlrd.empty_cell.value
    try:
        setup.cell(row, 5)
    except:
        break

    col = 6
    while(True):
        if setup.cell(row, col).value != empty:
            route.append(int(setup.cell(row, col).value))
            col = col+1
        else:
            break

    SCORES.append(route)
    row = row+1

ROUTESCORELEN = len(SCORES[0])
MIDDLE = math.ceil(len(SCORES)/2.0)

class Dash(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.lb = Listbox(self, height= 40)
        self.lb.pack()

        for climber in CLIMBERS:
            self.lb.insert(END, climber[0])
        '''Debug List
        self.lb.insert(END, "Entry")
        for line in range(100):
            self.lb.insert(END, "This is line number " + str(line))
        End Debug'''

        self.lb.bind('<<ListboxSelect>>', self.updatePlayer)

        self.selectbutton = Button(self, text="Full Climbers", command=None)
        self.leaderbutton = Button(self, text="LeaderBoard", command=self.leaderboard)

        self.numberlabels = []
        for route in range(33):
            label = Label(self, text = str(route + 1), font='Helvetica 18 bold')
            self.numberlabels.append(label)

        self.namelab = Label(self, text = "Name")
        self.sexlbl = Label(self, text="Sex")
        self.skilllbl = Label(self, text="Advanced")
        self.scorelbl = Label(self, text=str(22))


        self.scorebuts = []
        for routes in SCORES:
            temp =[]
            for score in routes:
                check = Checkbutton(self, text=str(score), variable = None, font='Helvetica 12')
                temp.append(check)
            self.scorebuts.append(temp)




        #Add TO Grid
        self.lb.grid(row=0, column=0, rowspan=32, columnspan=2)
        self.selectbutton.grid(row=33, column=0)
        self.leaderbutton.grid(row=33, column=1)

        col = 3
        nextcol = col + ROUTESCORELEN + 2
        row = 1
        for id, label in enumerate(self.numberlabels):
            if(id>MIDDLE):
                col = nextcol
                row=-MIDDLE
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
                if(rowid>MIDDLE):
                    col = nextcol
                    row=-MIDDLE
                check.grid(row=rowid+row, column=colid+col, pady= (0,0))




    def updatePlayer(self, e):
        self.namelab.config(text=CLIMBERS[self.lb.curselection()[0]][0])
        self.sexlbl.config(text=CLIMBERS[self.lb.curselection()[0]][1])
        self.skilllbl.config(text=CLIMBERS[self.lb.curselection()[0]][2])
        self.scorelbl.config(text=CLIMBERS[self.lb.curselection()[0]][3])

        #TODO Update variables so the rest of the app knows who I am editting

    def leaderboard(self):
        #Display leaderbod
        window = Toplevel(self)
        app = Leader(window)


root = Tk()
root.title("PolAI")
app = Dash(root)
root.mainloop()
