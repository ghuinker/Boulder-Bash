from tkinter import *

COLUMNS = 6
ROWS = 35
SCORES = [
#1-3
[100,200,300],[100,200,300],[100,200,300],
#4-6
[100,200,300],[100,200,300],[100,200,300],
#5-9
[100,200,300],[100,200,300],[100,200,300],
#10-12
[100,200,300],[100,200,300],[100,200,300],
#13-15
[100,200,300],[100,200,300],[100,200,300],
#16-18
[100,200,300],[100,200,300],[100,200,300],
#19-21
[100,200,300],[100,200,300],[100,200,300],
#22-24
[100,200,300],[100,200,300],[100,200,300],
#25-27
[100,200,300],[100,200,300],[100,200,300],
#28-30
[100,200,300],[100,200,300],[100,200,300],
#31-33
[800,500,300],[500,500,300],[100,200,300],
]
ROUTESCORELEN = len(SCORES[0])

MIDDLE = 17

class Dash(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.lb = Listbox(self, height= 40)
        self.lb.pack()

        #Debug List
        self.lb.insert(END, "Entry")
        for line in range(100):
            self.lb.insert(END, "This is line number " + str(line))
        #End Debug
        self.lb.bind('<<ListboxSelect>>', self.updatePlayer)

        self.selectbutton = Button(self, text="Select", command=None)
        self.leaderbutton = Button(self, text="Leader", command=None)

        self.numberlabels = []
        for route in range(33):
            label = Label(self, text = str(route + 1))
            self.numberlabels.append(label)

        self.namelab = Label(self, text = "Name")
        self.sexlbl = Label(self, text="Sex")
        self.skilllbl = Label(self, text="Advanced")
        self.scorelbl = Label(self, text=str(22))

        self.scorebuts = []
        for routes in SCORES:
            temp =[]
            for score in routes:
                check = Checkbutton(self, text=str(score), variable = None)
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
        print(self.lb.curselection())

    def train_go(self):
        print("TrainGo")
        if(self.conVar.get()):
            print("Conservative")
        if(self.libVar.get()):
            print("Liberal")


    def test_go(self):
        print("Self Go")

    def setTestResult(self, text):
        self.testResult.config(text=text)

    def setTrainResult(self, text):
        self.trainResult.delete("1.0", END)
        self.trainResult.config("1.0", text)



root = Tk()
root.title("PolAI")
app = Dash(root)
root.mainloop()
