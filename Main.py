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
        self.initexcelfolder()
        self.initfileviewer()
        self.create_widgets()





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
            if name == '':
                return
            name = self.mypath + "\\\\" + name
            workbook = xlsxwriter.Workbook(name+ '.xlsx')
            setup = newbk.add_worksheet("Setup")
            scores = newbk.add_worksheet("Scores")
            sends = newbk.add_worksheet("Sends")

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

    def initfileviewer(self):
        files = []

        for (dirpath, dirnames, filenames) in walk(self.mypath):
            files.extend(filenames)
            break

        self.excelfiles = []
        for filename in files:
            split = filename.split('.')
            if split[1] == 'xlsx':
                self.excelfiles.append(split[0])
        self.curfile = None

    def updatefileviewer(self):
        files = []
        for (dirpath, dirnames, filenames) in walk(self.mypath):
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

    def initexcelfolder(self):
        self.mypath = os.getcwd()
        splitpath = self.mypath.split('\\')
        splitpath = splitpath[:-1]
        up = ""
        for str in splitpath:
            up = up + str + '\\\\'


        up = up + "Excel Files"
        if not os.path.exists(up):
            os.makedirs(up)
        self.mypath = up

    def excelclicked(self, e):
        try:
            self.curfile = self.lb.curselection()[0]
        except:
            None
        self.excelname.delete(0,END)
        self.excelname.insert(0,self.excelfiles[self.curfile])

    def deletefile(self):
        name = self.excelname.get()
        name = self.mypath + "\\\\" + name
        os.remove(name + '.xlsx')
        self.updatefileviewer()

    def openexcel(self):
        name = self.excelname.get()
        name = self.mypath + "\\\\" + name
        os.startfile(name + '.xlsx')

    def runexcel(self):
        window = Toplevel(self)
        name = self.excelname.get()
        name = self.mypath + "\\\\" + name
        name = name.replace("\\\\", "\\")
        app = Dash(window, name + '.xlsx')

    def quit(self):
        self.master.destroy()


root = Tk()
root.title("Boulder Bash")
app = Main(root)
root.mainloop()
