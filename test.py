from tkinter import *

class OperatorNameButtons():
    def __init__(self):
        self.v = StringVar()
        self.v.set('Mike')

        self.OperatorNames = ['Mike', 'Nic', 'Jenn', 'Shannon']

        
        self.OperatorButton = {var:Radiobutton() for var in self.OperatorNames}

        for Name in self.OperatorButton.keys():
            self.OperatorButton[Name] = Radiobutton(root, 
                                            text=Name,
                                            indicatoron=0,
                                            highlightthickness=4,
                                            width = 20,
                                            padx = 20,
                                            pady = 5,
                                            variable=self.v,
                                            borderwidth=0,
                                            bg='#F5F5F5',
                                            activeforeground='#FFFFFF',
                                            command=lambda var=Name: self.SetCol(var),
                                            selectcolor='#13799F',
                                            font=("Open Sans", 24 * -1),
                                            value=Name
                                            )

            self.OperatorButton[Name].pack()
        self.SetCol(self.v.get())

    def SetCol(self, Name):
        for button in self.OperatorButton.values():
            if not button == self.OperatorButton[Name]:
                button.configure(fg='#13799F')
        self.OperatorButton[Name].configure(fg='#FFFFFF')






root = Tk()

LABELS=OperatorNameButtons()

root.mainloop()