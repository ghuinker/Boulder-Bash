from tkinter import *
import xlsxwriter
from Dash import Dash
import xlrd
from os import walk
import os



class Main(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.initfileviewer()
        self.create_widgets()

    def initfileviewer(self):
        files = []
        mypath = os.getcwd()
        for (dirpath, dirnames, filenames) in walk(mypath):
            files.extend(filenames)
            break

        self.excelfiles = []
        for filename in files:
            split = filename.split('.')
            if split[1] == 'xlsx':
                self.excelfiles.append(split[0])

        self.curfile = None


    def create_widgets(self):
        self.excelnamelbl = Label(self, text="Name of xcel file")
        self.excelname = Entry(self, width=30)
        self.create = Button(self,text="Create", command=self.create)
        self.runbtn = Button(self,text="Run File", command=self.runexcel)
        self.openexcelbtn = Button(self, text='Open Excel', command=self.openexcel )

        self.lb = Listbox(self)

        for excelfile in self.excelfiles:
            self.lb.insert(END, excelfile)

        self.lb.bind('<<ListboxSelect>>', self.excelclicked)

        self.excelnamelbl.grid(row=0, column = 0)
        self.excelname.grid(row=0, column=1, columnspan=2)
        self.create.grid(row=1, column=0)
        self.openexcelbtn.grid(row=1, column=1)
        self.runbtn.grid(row=1, column=2)


        self.lb.grid(row=2, column=0, columnspan=2)

    def create(self):
        try:
            xlrd.open_workbook(self.excelname.get("1.0", 'end-1c') + '.xlsx')

        except:
            print("creating New File")
            workbook = xlsxwriter.Workbook(self.excelname.get("1.0", 'end-1c') + '.xlsx')
            setup = workbook.add_worksheet("Setup")
            attempts = workbook.add_worksheet("Attempts")
            scores = workbook.add_worksheet("Scores")
            LeaderBoard = workbook.add_worksheet("LeaderBoard")

            '''Setup Write'''
            setup.write('A1', 'First Name')
            setup.write('B1', 'Last Name')
            setup.write('C1', 'Sex')
            setup.write('D1', 'Level')

            setup.write('G1', 'Route')
            setup.write('H1', 'Scores')



            print("saved")
            workbook.close()
            self.updatesetup()
            self.quit()


    def updateexcel(self):
        None

    def excelclicked(self, e):
        try:
            self.curfile = self.lb.curselection()[0]
        except:
            None
        self.excelname.delete(0,END)
        self.excelname.insert(0,self.excelfiles[self.curfile])

    def openexcel(self):
        file = self.excelname.get() + '.xlsx'
        os.startfile(file)

    def runexcel(self):
        window = Toplevel(self)
        app = Dash(window, self.excelname.get() + '.xlsx')

    def updatesetup(self):
        window = Toplevel(self)
        frame = Frame(window, width=100, height=50)
        frame.place(x=700, y=0)
        label = Label(frame, text="Go Update Setup").pack()

    def quit(self):
        self.master.destroy()


root = Tk()
root.title("Boulder Bash")
app = Main(root)
root.mainloop()
