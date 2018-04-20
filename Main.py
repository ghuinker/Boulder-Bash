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
        print(self.excelfiles)
        self.curfile = None


    def create_widgets(self):
        self.excelnamelbl = Label(self, text="Name of xcel file")
        self.excelname = Entry(self, width=30)
        self.create = Button(self,text="Create", command=self.create)
        self.runbtn = Button(self,text="Run File", command=self.runexcel)
        self.openexcelbtn = Button(self, text='Open Excel', command=self.openexcel )
        self.deletebtn = Button(self, text = 'Delete Excel', command=self.deletefile)

        self.lb = Listbox(self)

        for excelfile in self.excelfiles:
            self.lb.insert(END, excelfile)

        self.lb.bind('<<ListboxSelect>>', self.excelclicked)

        self.excelnamelbl.grid(row=0, column = 0)
        self.excelname.grid(row=0, column=1, columnspan=3)
        self.create.grid(row=1, column=0)
        self.openexcelbtn.grid(row=1, column=1)
        self.runbtn.grid(row=1, column=2)
        self.deletebtn.grid(row=1, column=3)


        self.lb.grid(row=2, column=0, columnspan=3)

    def create(self):
        name = self.excelname.get().strip()
        if name in self.excelfiles:
            self.runexcel()
        else:
            print(name)
            if name == '':
                return
            workbook = xlsxwriter.Workbook(name+ '.xlsx')
            setup = workbook.add_worksheet("Setup")
            attempts = workbook.add_worksheet("Attempts")
            scores = workbook.add_worksheet("Scores")
            LeaderBoard = workbook.add_worksheet("LeaderBoard")

            '''Setup Write'''
            setup.write('A1', 'First Name')
            setup.write('B1', 'Last Name')
            setup.write('C1', 'Sex')
            setup.write('D1', 'Level')
            
            setup.write('F1', 'Heats')
            setup.write('G1', 'Route')
            setup.write('H1', 'Scores')

            workbook.close()
            self.openexcel()
            self.updatefileviewer()


    def updatefileviewer(self):
        files = []
        mypath = os.getcwd()
        for (dirpath, dirnames, filenames) in walk(mypath):
            files.extend(filenames)
            break

        self.excelfiles = []
        for id, filename in enumerate(files):
            split = filename.split('.')
            if split[1] == 'xlsx':
                self.excelfiles.append(split[0])

        self.lb.delete(0, END)
        for excelfile in self.excelfiles:
            self.lb.insert(END, excelfile)

    def excelclicked(self, e):
        try:
            self.curfile = self.lb.curselection()[0]
        except:
            None
        self.excelname.delete(0,END)
        self.excelname.insert(0,self.excelfiles[self.curfile])

    def deletefile(self):
        os.remove(self.excelname.get() + '.xlsx')
        self.updatefileviewer()

    def openexcel(self):
        file = self.excelname.get() + '.xlsx'
        os.startfile(file)

    def runexcel(self):
        window = Toplevel(self)
        app = Dash(window, self.excelname.get() + '.xlsx')

    def quit(self):
        self.master.destroy()


root = Tk()
root.title("Boulder Bash")
app = Main(root)
root.mainloop()
