from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from labelfunctions import *
from PIL import ImageTk, Image
from pathlib import Path
import configparser
import tkinter.messagebox as mbox
import ast

  
class MainDialog:
    def __init__(self, master):
        self.master = master
        self.Path = Path(__file__).parent
        self.Assets = self.Path / Path("./assets")
        self.config = configparser.ConfigParser()
        self.config.read(self.Path / Path("./config.ini"))  
        self.OperatorNames = ast.literal_eval(self.config.get('Operators', 'OPERATOR_NAMES'))  
        self.IntVars = {var: IntVar() for var in ['DryQty', 'BagQty', 'BoxQty', 'DeliveryNo']}
        self.DataVars = {var: StringVar() for var in ['Operator', 'StatusMsg', 'QRString', 'OrderType', 'DateCaption', 'Date', 'OrderNr', 'Name', 'Street', 'Zip', 'City', 'Phone']}        
        self.OperatorButton = {var:Radiobutton() for var in self.OperatorNames}
        self.ZPLF = ZPLFunctions()  
        self.DataVars['Operator'].set('Mike')
        self.DataVars['OrderType'].set('D')
        self.IntVars['DeliveryNo'].set(50)
        self.CustomerData = [self.DataVars['Name'], self.DataVars['Street'], self.DataVars['Zip'], self.DataVars['City'], self.DataVars['Phone'], self.DataVars['OrderNr']]   
        self.PlaceRootCanvas()

        print('Init')
        
        for var in self.CustomerData:
            print(var)


    def AppAssets(self, path: str) -> Path:
        return self.Assets / Path(path)
    
    def PlaceRootCanvas(self): 
        self.RootCanvas = Canvas(
            self.master,
            bg = "#3E3E3E",
            height = 1080,
            width = 1920,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )          
        self.BackgroundImage = PhotoImage(file=self.AppAssets("RootBg.png"))
        self.RootCanvas.create_image(0, 0, image=self.BackgroundImage, anchor=NW)          
        
        for Name in self.OperatorNames:
                    self.OperatorButton[Name] = Radiobutton(self.master, 
                                                            text=Name,
                                                            indicatoron=0,
                                                            width = 20,
                                                            padx = 20,
                                                            pady = 10,
                                                            borderwidth=0,
                                                            bg='#F5F5F5',
                                                            activeforeground='#FFFFFF',
                                                            selectcolor='#13799F',
                                                            font=("Open Sans", 24 * -1),
                                                            value=Name,
                                                            variable=self.DataVars['Operator'],
                                                            command=lambda var=Name: self.SetCol(var),
                                                            )

        self.RootCanvas.place(x = 0, y = 0)
        self.RootCanvas.create_rectangle(
            420.0,
            246.0,
            1500.0,
            854.0,
            fill="#FFFFFF",
            outline="")

        self.RootCanvas.create_rectangle(
            861.0,
            275.0,
            862.0,
            825.0,
            fill="#777777",
            outline="")
            
        self.QRImage = PhotoImage(file=self.AppAssets("QRImg.png"))
        self.RootCanvas.create_image(930, 380, image=self.QRImage, anchor=NW) 

        self.RootCanvas.create_text(
            459.0,
            294.0,
            anchor="nw",
            text="Selecteer operator",
            fill="#13799F",
            font=("Open Sans", 32 * -1)
        )

        c = -20
        for var in self.OperatorNames:
            c +=70
            self.OperatorButton[var].place(
                x=480.0,
                y=314.0 + c
            )

        self.SetCol(self.DataVars['Operator'].get())

        self.RootCanvas.create_text(
            894.0,
            294.0,
            anchor="nw",
            text="Scan QR code op pakbon",
            fill="#13799F",
            font=("Open Sans", 32 * -1)
        )
        self.QREntry = Entry(
            bd=0,
            bg="#FFFFFF",
            highlightthickness=2,
            highlightcolor='#FFFFFF',
            fg='#FFFFFF',
            textvariable=self.DataVars['QRString']
        )
        self.QREntry.place(
            x=1300.0,
            y=782.0,
            width=50.0,
            height=23.0
        )
        
        self.ManualEntBtnImg = PhotoImage(
            file=self.AppAssets("ManualEntBtn.png"))
        self.ManualEntBtn = Button(
            image=self.ManualEntBtnImg,
            borderwidth=0,
            highlightthickness=0,
            command=lambda var=self.RootCanvas: self.ManualEntry(var),
            relief="flat"
        )
        self.ManualEntBtn.place(
            x=1256.0,
            y=775.0,
            width=219.0,
            height=54.0
        )

        self.StatusMessage = Label(
            textvariable=self.DataVars['StatusMsg'],
            fg='#3E3E3E',
            bg='#FFFFFF'
        )
        self.StatusMessage.config(font=("OpenSans Light", 16))
        self.StatusMessage.place(
            x=904.0,
            y=733.0,
        )
        self.QREntry.bind(('<Return>'),lambda event:self.QRDecode())
        self.QREntry.focus()



#Start of Manual Entry canvas
    def PlaceManEntCanvas(self):
        self.EntryCaptions = ['Voorletter en achternaam', 'Straat en huisnummer', 'Postcode en plaats', 'Telefoonnummer', 'Ordernummer', 'Datum', 'Type order']
        self.Entries = ['Name', 'Street', 'Zip', 'City', 'Phone', 'OrderNr']
        self.Entry = {var:None for var in self.Entries} 
        self.OrderTypeButton = {var:None for var in ['D', 'C']}
        self.DataVars['StatusMsg'].set('')
        self.ManEntCanvas = Canvas(
            self.master,
            bg = "#3E3E3E",
            height = 1080,
            width = 1920,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        style = ttk.Style()
        style.configure('my.DateEntry', fieldbackground='#F5F5F5', background='#13799F', borderwidth=0, arrowcolor='#FFFFFF', arrowsize=33)

        for Type in self.OrderTypeButton.keys():
            self.OrderTypeButton[Type] = Radiobutton(self.master, 
                                                    indicatoron=0,
                                                    width = 15,
                                                    padx = 1,
                                                    pady = 1,
                                                    borderwidth=0,
                                                    bg='#F5F5F5',
                                                    activeforeground='#FFFFFF',
                                                    selectcolor='#13799F',
                                                    font=("OpenSans Light", 21 * -1),
                                                    variable=self.DataVars['OrderType'],
                                                    command=lambda var=Type: self.SetCol(var),
                                                    )

        for l in range(len(self.EntryCaptions)):
            self.EntryCaptions[l] = Label(
                bg='#FFFFFF',
                font=("OpenSans Light", 21 * -1),
                text=self.EntryCaptions[l]
                )

        self.BackgroundImage = PhotoImage(file=self.AppAssets("RootBg.png"))
        self.ManEntCanvas.create_image(0, 0, image=self.BackgroundImage, anchor=NW)  
     
        self.ManEntCanvas.place(x = 0, y = 0)
        self.ManEntCanvas.create_rectangle(
            420.0,
            246.0,
            1500.0,
            854.0,
            fill="#FFFFFF",
            outline="") 

        self.ManEntCanvas.create_text(
            459.0,
            294.0,
            anchor="nw",
            text="Gegevens wijzigen",
            fill="#13799F",
            font=("Open Sans", 32 * -1)
        )            

        self.ManEntCanvas.create_text(
            459.0,
            580.0,
            anchor="nw",
            text="Orderinformatie",
            fill="#7E1E1D",
            font=("OpenSans Light", 24 * -1)
        )

        self.ManEntCanvas.create_text(
            459.0,
            335.0,
            anchor="nw",
            text="Klantgegevens",
            fill="#7E1E1D",
            font=("OpenSans Light", 24 * -1)
        )

       
        for var in self.Entries:
            self.Entry[var] = Entry(
                bg='#F5F5F5',
                bd=0,
                highlightthickness=0,
                font=("OpenSans Light", 21 * -1),
                textvariable=self.DataVars[var]
                )
   
        self.Entry['Name'].place(
            x=777.0,
            y=380.0,
            width=389.0,
            height=33.0
        )

        self.Entry['Street'].place(
            x=777.0,
            y=430.0,
            width=389.0,
            height=33.0
        )

        self.Entry['Zip'].place(
            x=777.0,
            y=480.0,
            width=123.0,
            height=33.0
        )

        self.Entry['City'].place(
            x=910.0,
            y=480.0,
            width=256.0,
            height=33.0 
        )

        self.Entry['Phone'].place(
            x=777.0,
            y=530.0,
            width=389.0,
            height=33.0
        )

        self.Entry['OrderNr'].place(
            x=777.0,
            y=625.0,
            width=389.0,
            height=33.0
        )


        for l in range(len(self.EntryCaptions)):
            y=380.0
            if l > 3:
                y=425.0
            
            self.EntryCaptions[l].place(
                x=467.0,
                y=y + (l * 50)   
            )

        self.EntryCaptions[5].configure(textvariable=self.DataVars['DateCaption'])
        
        self.DateEntry = DateEntry(
            style='my.DateEntry',
            background='#13799F',
            locale='nl_NL',
            date_pattern='dd/mm/yyyy',
            bd=0,
            highlightthickness=0,
            font=("OpenSans Light", 21 * -1),
            textvariable=self.DataVars['Date'],
            foreground='#FFFFFF')

        self.DateEntry.place(
            x=777.0,
            y=675.0,
            width=389.0,
            height=33.0   
            )

        self.OrderTypeButton['C'].configure(value='C', text='Afhalen')
        self.OrderTypeButton['C'].place(
            x=777.0,
            y=725.0
        )

        self.OrderTypeButton['D'].configure(value='D', text='Bezorgen')
        self.OrderTypeButton['D'].place(
            x=982.0,
            y=725.0
        )

        self.SetCol(self.DataVars['OrderType'].get())

        self.ManEntExitImg = PhotoImage(
            file=self.AppAssets("ManEntExitBtn.png"))
        self.ManEntExitBtn = Button(
            image=self.ManEntExitImg,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.ExitManEnt(),
            relief="flat"
        )
        self.ManEntExitBtn.place(
            x=1010.0,
            y=775.0,
            width=219.0,
            height=54.0
)

        self.ManEntOKImg = PhotoImage(
            file=self.AppAssets("ManEntOKBtn.png"))
        self.ManEntOKBtn = Button(
            image=self.ManEntOKImg,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.ManEntValidate(),
            relief="flat"
        )
        self.ManEntOKBtn.place(
            x=1256.0,
            y=775.0,
            width=219.0,
            height=54.0
        )


#Start of Entry canvas
    def PlaceEntryCanvas(self):        
        self.DataVars['StatusMsg'].set('')
        self.EntryCanvas = Canvas(
            self.master,
            bg = "#3E3E3E",
            height = 1080,
            width = 1920,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.BackgroundImage = PhotoImage(file=self.AppAssets("RootBg.png"))
        self.EntryCanvas.create_image(0, 0, image=self.BackgroundImage, anchor=NW)  
        
        self.EntryCanvas.place(x = 0, y = 0)
        self.EntryCanvas.create_rectangle(
            420.0,
            236.0,
            1500.0,
            854.0,
            fill="#FFFFFF",
            outline="")
        self.EntryCanvas.create_rectangle(
            861.0,
            265.0,
            862.0,
            815.0,
            fill="#777777",
            outline="")

        self.EntryCanvas.create_text(
            894.0,
            284.0,
            anchor="nw",
            text="Levering",
            fill="#13799F",
            font=("Open Sans", 32 * -1)
        )

        self.EntryCanvas.create_text(
            458.0,
            284.0,
            anchor="nw",
            text="Klantgegevens",
            fill="#13799F",
            font=("Open Sans", 32 * -1)
        )
        
        self.EntryCanvas.create_text(
            458.0,
            600.0,
            anchor="nw",
            text="Order info",
            fill="#13799F",
            font=("Open Sans", 32 * -1)
)
        #Tkinter label loop
        self.Labels = ['DateCaption', 'Date', 'OrderNrCaption', 'OrderNr', 'Name', 'Street', 'Zip', 'City', 'Phone']
        self.Label = {var:None for var in self.Labels}
             
        for var in self.Labels:
            self.Label[var] = Label(
                bg='#FFFFFF',
                font=("OpenSans Light", 21 * -1),
                )
            if var in self.DataVars.keys():
                self.Label[var].config(textvariable=self.DataVars[var])
            
        self.Label['Name'].place(
            x=458.0,
            y=349.0,
        )       
        self.Label['Street'].place(
            x=458.0,
            y=385.0,
        )
        self.Label['Zip'].place(
            x=458.0,
            y=421.0,
        ) 
        self.Label['City'].place(
            x=591.0,
            y=421.0,
        )
        self.Label['Phone'].place(
            x=458.0,
            y=457.0,
        )  
        self.Label['OrderNrCaption'].config(text='Ordernummer:')
        self.Label['OrderNrCaption'].place(
            x=463.0,
            y=654.0,
        )  
        self.Label['OrderNr'].place(
            x=629.0,
            y=654.0,
        )         
        self.Label['DateCaption'].place(
            x=463.0,
            y=690.0,
        )       
        self.Label['Date'].place(
            x=629.0,
            y=690.0,
        ) 
        self.ChangeDataImg = PhotoImage(
            file=self.AppAssets("ChangeDataBtn.png"))
        self.ChangeDataBtn = Button(
            image=self.ChangeDataImg,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.ManualEntry(self.EntryCanvas),
            relief="flat"
        )
        self.ChangeDataBtn.place(
            x=463.0,
            y=775.0,
            width=219.0,
            height=54.0
        ) 
          
        self.ReturnBtnImg = PhotoImage(
            file=self.AppAssets("ReturnBtn.png"))
        self.ReturnBtn = Button(
            image=self.ReturnBtnImg,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.ReturnToQR(),
            relief="flat"
        )
        self.ReturnBtn.place(
            x=1010.0,
            y=775.0,
            width=219.0,
            height=54.0
        )

        self.PrintBtnImg = PhotoImage(
            file=self.AppAssets("PrintBtn.png"))
        self.PrintBtn = Button(
            image=self.PrintBtnImg,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.PrintValidation(),
            relief="flat"
        )
        self.PrintBtn.place(
            x=1256.0,
            y=775.0,
            width=219.0,
            height=54.0
        )
        
        self.PlusBtnImg = PhotoImage(
            file=self.AppAssets("PlusBtn.png"))
        self.MinusBtnImg = PhotoImage(
            file=self.AppAssets("MinusBtn.png"))

        #Create fields loop

        self.IntVar = [self.IntVars['DryQty'], self.IntVars['BoxQty'], self.IntVars['BagQty'], self.IntVars['DeliveryNo']]
        self.Captions = ['Aantal droog:','Aantal dozen:','Aantal tassen:','Bestemming:']
        if self.DataVars['OrderType'].get() == 'C':
            self.DataVars['DateCaption'].set('Afhaaldatum:') 
            s = 35                       
            if self.IntVars['DeliveryNo'] in self.IntVar:
                # self.DeliveryN = self.IntVars['DeliveryNo'].get()
                del self.IntVar[3]
                print(self.IntVar)  
        elif self.DataVars['OrderType'].get() == 'D':
            self.DataVars['DateCaption'].set('Bezorgdatum:') 
            s = 0
            if not self.IntVars['DeliveryNo'] in self.IntVar:
                self.IntVar.append(self.IntVars['DeliveryNo'])
                print(self.IntVar)
        
        for i in range(len(self.IntVar)):

            self.EntryCanvas.create_text(
                926.0,
                643.0 - s - (i * 85),
                anchor="nw",
                text=str(self.Captions[i]),
                fill="#3E3E3E",
                font=("OpenSans Light", 24 * -1)
            )

            self.PlusBtn = Button(
                image=self.PlusBtnImg,
                bg='#FFFFFF',
                borderwidth=0,
                highlightthickness=0,
                command=lambda var=self.IntVar[i]: self.SetQuantity(var, '+'),
                relief="flat"
            )
            self.PlusBtn.place(
                x=1323.0,
                y=626.0 - s - (i * 85),
                width=55.0,
                height=55.0
            )

            self.MinusBtn = Button(
                image=self.MinusBtnImg,
                bg='#FFFFFF',
                borderwidth=0,
                highlightthickness=0,
                command=lambda var=self.IntVar[i]: self.SetQuantity(var, '-'),
                relief="flat"
            )
            self.MinusBtn.place(
                x=1243.0,
                y=626.0 - s - (i * 85),
                width=55.0,
                height=55.0
            )  
                            
            self.QuantityLabel = Label(
                textvariable=self.IntVar[i],
                fg='#3E3E3E',
                bg='#FFFFFF',
                width='3'
                
            )
            self.QuantityLabel.config(font=("Open Sans", 34 * -1))
            self.QuantityLabel.place(
                x=1135.0,
                y=637.0 - s - (i * 85),
            )
         
            
#Start of Printing canvas      
    def PlacePrintCanvas(self):
        self.PrintBtn.config(state=DISABLED)
        self.PrintQty = IntVar()
        self.PrintQty.set(self.Quantities)
        self.PrintCanvas = Canvas(
            self.master,
            bg = "#FFFFFF",
            height = 262,
            width = 1920,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.PrintCanvas.place(x = 0, y = 400)
        self.PrintCanvas.create_rectangle(
            0.0,
            0.0,
            1920.0,
            262.0,
            fill="#FFFFFF",
            outline="")

        self.PrintCanvas.create_rectangle(
            0.0,
            0.0,
            1920.0,
            4.0,
            fill="#7E1E1D",
            outline="")

        self.PrintCanvas.create_rectangle(
            0.0,
            258.0,
            1920.0,
            262.0,
            fill="#7E1E1D",
            outline="")

        self.PrintCanvas.create_text(
            991.0,
            102.0,
            anchor="nw",
            text="Aantal:",
            fill="#3E3E3E",
            font=("OpenSans Light", 24 * -1)
        )
        
        self.PrintQuantity = Label(
            textvariable=self.PrintQty,
            fg='#3E3E3E',
            bg='#FFFFFF',       
        )
        self.PrintQuantity.config(font=("Open Sans", 24 * -1))
        self.PrintQuantity.place(
            x=1080.0,
            y=500.0,
        )
        
        
        self.PrinterStatus = Label(
            textvariable=self.DataVars['StatusMsg'],
            fg='#3E3E3E',
            bg='#FFFFFF',       
        )
        self.PrinterStatus.config(font=("Open Sans", 18 * -1))
        self.PrinterStatus.place(
            x=988.0,
            y=535.0,
        )

        self.PrintCanvas.create_rectangle(
            958.0,
            31.0,
            959.0,
            231.0,
            fill="#777777",
            outline="")

        self.PrintCanvas.create_text(
            991.0,
            36.0,
            anchor="nw",
            text="Labels worden geprint....",
            fill="#13799F",
            font=("Open Sans", 36 * -1)
        )

        self.LblPreviewImg = ImageTk.PhotoImage(self.ZPLF.LabelPreview())
        self.PreviewImage = Label(master=self.master, image=self.LblPreviewImg)
        self.PreviewImage.place(
            x=575.0,
            y=436.0,
        )
        
        self.PrintLabel()       

    def PrintLabel(self):
        try:
            self.ZPLF.Printer()
            self.DataVars['StatusMsg'].set('Opdracht verzenden naar printer...')
        except Exception:
            # self.DataVars['StatusMsg'].set('Kan niet verbinden met printer!')
            # self.PrinterStatus.config(fg='red')    
            raise
        else: 
            self.DataVars['StatusMsg'].set('Opdracht succesvol verzonden!')
            self.master.after(3500, self.ReturnToRoot)
            
    def ReturnToRoot(self):
        DeliveryNo = self.IntVars['DeliveryNo'].get()
        DeliveryNo -= 1
        self.IntVars['DeliveryNo'].set(DeliveryNo)
        
        for var in [self.IntVars['BagQty'], self.IntVars['BoxQty'], self.IntVars['DryQty']]:
            var.set(0)

        for var in self.CustomerData:
            var.set('')

        self.DataVars['StatusMsg'].set('  ')
        self.PrintCanvas.delete('all')
        self.EntryCanvas.delete('all')
        self.PlaceRootCanvas()
        
    def ManualEntry(self, ref):
        self.ref = ref
        ref.delete('all')
        self.PlaceManEntCanvas()

    def ExitManEnt(self):
        self.ManEntCanvas.delete('all')
        if self.ref == self.RootCanvas:
            self.PlaceRootCanvas()
            for var in self.CustomerData:
                var.set('')
        else:
            self.PlaceEntryCanvas()

    def ManEntValidate(self):
        valid = True
        if self.DataVars['OrderType'].get() == 'C':
            for var in [self.DataVars['Name'], self.DataVars['OrderNr']]:
                var = var.get()
                if not var:
                    valid = False
            if valid == False:
                mbox.showerror(title='Foutmelding', message='Naam of Ordernummer niet ingevuld!')
        else:
            for var in self.CustomerData:
                var = var.get()
                if var == '':
                    valid = False 
            if valid == False:
                mbox.showerror(title='Foutmelding', message='Alle velden dienen ingevuld te worden!')

        if valid == True:
            self.ManEntCanvas.delete('all')
            self.PlaceEntryCanvas() 

    def ReturnToQR(self):
        self.EntryCanvas.delete('all')
        self.PlaceRootCanvas()

    def QRDecode(self):
        QRString = self.DataVars['QRString'].get()     
        if not QRString:
            self.DataVars['StatusMsg'].set('Geen QR code gescand!')
            self.StatusMessage.config(fg='red')
            return False

        if not(QRString.endswith('pass')):
            self.DataVars['StatusMsg'].set('Fout tijdens scannen of ongeldige QR code!')
            self.StatusMessage.config(fg='red')
            self.QREntry.delete(0, 'end')
            self.QREntry.focus()
            return False

        while True:
            try:
                QRLst = QRString.strip('><=').split(',')
                OrderType, Name, Sname, Street, Zip, City, Phone, Date, OrderNr, QRVal = QRLst
                break
            except ValueError:
                self.DataVars['StatusMsg'].set('Gescande code is niet geldig!')
                self.StatusMessage.config(fg='red')
                self.QREntry.delete(0, 'end')
                self.QREntry.focus()
                return False
                
        self.RootCanvas.delete('all')
        
        FormattedName = str(Name[0])+'. '+str(Sname)
        self.DataVars['OrderType'].set(OrderType)
        self.DataVars['Name'].set(FormattedName)
        self.DataVars['Street'].set(Street)        
        self.DataVars['Zip'].set(Zip)
        self.DataVars['City'].set(City)
        self.DataVars['Phone'].set(Phone)
        self.DataVars['Date'].set(Date)
        self.DataVars['OrderNr'].set(OrderNr)
        self.QREntry.delete(0, 'end')
        self.PlaceEntryCanvas()
        
        return True
        
    def SetCol(self, Name):
        if not Name in self.OperatorNames:
            for button in self.OrderTypeButton.values():
                if not button == self.OrderTypeButton[Name]:
                    button.configure(fg='#13799F')
            if self.DataVars['OrderType'].get() == 'D':
                self.DataVars['DateCaption'].set('Bezorgdatum')
            else:
                self.DataVars['DateCaption'].set('Afhaaldatum')
            self.OrderTypeButton[Name].configure(fg='#FFFFFF')
        else:
            for button in self.OperatorButton.values():
                if not button == self.OperatorButton[Name]:
                    button.configure(fg='#13799F')
            self.OperatorButton[Name].configure(fg='#FFFFFF')

    def SetQuantity(self, variable:IntVar, method:str) -> None:
        item = variable.get()
        if method == '+':
            item += 1
        elif method == '-':
            item -= 1
        else:
            print('Error: Invalid method given')
        variable.set(item)   
        
    def PrintValidation(self):
        self.Quantities = self.IntVars['BagQty'].get() + self.IntVars['BoxQty'].get() + self.IntVars['DryQty'].get()
        
        if self.Quantities == 0:
            mbox.showerror(title='Foutmelding', message='Er zijn geen aantallen ingevuld!')
        else:             
            self.SetLabelVars()

    def SetLabelVars(self):
        LabelVars = [self.DataVars['OrderType'].get()]
        for var in [self.IntVars['DeliveryNo'], self.IntVars['BagQty'], self.IntVars['BoxQty'], self.IntVars['DryQty'], self.DataVars['Name'], self.DataVars['Street'], self.DataVars['Zip'], self.DataVars['City'], self.DataVars['Phone'],self.DataVars['Operator'], self.DataVars['Date'], self.DataVars['OrderNr']]:
            LabelVar = var.get()
            LabelVars.append(LabelVar)
        self.ZPLF.BuildLabel(LabelVars, self.Quantities)
        self.PlacePrintCanvas()

      
def main(): 
    root = Tk()
    root.title('NOVA QR2Label v1.5')
    # root.configure(cursor='none')
    
    
    # root.wm_overrideredirect(True)
    #root.wm_attributes('-type', 'splash')
    root.wm_attributes('-fullscreen', True)
    app = MainDialog(root)
    root.update()
    root.mainloop()


if __name__ == '__main__':
    main()