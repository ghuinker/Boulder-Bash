from tkinter import *
import xlsxwriter
from Dash import Dash
import xlrd

class Main(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.excelnamelbl = Label(self, text="Name of xcel file")
        self.excelname = Text(self, width=30, height=1)
        self.create = Button(self,text="Create", command=self.create)
        self.open = Button(self,text="Open", command=self.open)

        self.excelnamelbl.grid(row=0, column = 0)
        self.excelname.grid(row=0, column=1, columnspan=2)
        self.create.grid(row=1, column=0)
        self.open.grid(row=1, column=2)

    def create(self):
        try:
            xlrd.open_workbook(self.excelname.get("1.0", 'end-1c') + '.xlsx')
            self.dash()
        except:
            print("creating New File")
            workbook = xlsxwriter.Workbook(self.excelname.get("1.0", 'end-1c') + '.xlsx')
            setup = workbook.add_worksheet("Setup")
            setup.write('A1', 'First Name')
            setup.write('B1', 'Last Name')
            setup.write('C1', 'Sex')
            setup.write('D1', 'Level')

            setup.write('G1', 'Route')
            setup.write('H1', 'Scores')

            print("saved")
            workbook.close()
            self.updateexcel()
            self.updatesetup()



    def updateexcel():
        None
    def dash(self):
        window= Toplevel(self)
        app = Dash(window, self.excelname.get("1.0", 'end-1c') + '.xlsx')
    def open(self):
        window = Toplevel(self)
        app = Dash(window, self.excelname.get("1.0", 'end-1c') + '.xlsx')

    def updatesetup(self):
        window = Toplevel(self):
        label = Label(window, text= "Excel Created \nUpdate The Setup Excel Sheet")
        label.pack()


root = Tk()
root.title("Boulder Bash")
app = Main(root)
root.mainloop()
