from tkinter import *
from tkinter import ttk
from labelfunctions import *
from PIL import ImageTk, Image
from pathlib import Path
import configparser
import importlib
import tkinter.messagebox as mbox
import io
import sys
import ast


   
class MainDialog:
    def __init__(self, master):
        self.master = master
        self.Path = Path(__file__).parent
        self.Assets = self.Path / Path("./assets")
        self.QuantityVars = {var: IntVar() for var in ['DeliveryNo', 'BoxQty', 'BagQty', 'DryQty']}
        self.DataVars = {var: StringVar() for var in ['Operator', 'StatusMsg', 'QRString', 'DeliveryDate', 'OrderNr', 'Name', 'Street', 'Zip', 'City', 'Phone']}        
        self.config = configparser.ConfigParser()
        self.config.read(self.Path / Path("./config.ini"))  
        self.OperatorNames = ast.literal_eval(self.config.get('Operators', 'OPERATOR_NAMES'))        
        self.PlaceRootCanvas()
        self.ZPLF = ZPLFunctions()  
        self.DataVars['Operator'].set('Mike')
        self.QuantityVars['DeliveryNo'].set(50)
        
        
        
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
                  
        self.OperatorNamesVar = self.DataVars['Operator']
        self.OperatorMenu = ttk.OptionMenu(
            self.master,
            self.OperatorNamesVar,
            self.OperatorNamesVar.get(),
            *self.OperatorNames,
            style='my.TMenubutton'
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
            fill="#000000",
            font=("OpenSans Regular", 36 * -1)
        )

        style = ttk.Style()
        style.configure('my.TMenubutton', font=('OpenSans Regular', 16), background='#FFFFFF')  
        # self.OperatorMenu.config(font=("OpenSans Light", 16), bg='white', relief=FLAT)
        self.OperatorMenu.place(
            x=459.0,
            y=364.0,
            width=200.0,
            height=50.0,
        )
        self.RootCanvas.create_text(
            894.0,
            294.0,
            anchor="nw",
            text="Scan QR code op pakbon",
            fill="#000000",
            font=("OpenSans Regular", 36 * -1)
        )

        # self.ManualEntBtnImg = PhotoImage(
            # file=self.AppAssets("ManualEntBtn.png"))
        # self.ManualEntBtn = Button(
            # image=self.ManualEntBtnImg,
            # borderwidth=0,
            # highlightthickness=0,
            # command=lambda: print("button_1 clicked"),
            # relief="flat"
        # )
        # self.ManualEntBtn.place(
            # x=894.0,
            # y=778.0,
            # width=219.0,
            # height=34.0
        # )
        self.BulletChar = "\u2022" #Specification of bullet character
        self.QREntry = Entry(
            bd=0,
            bg="#FFFFFF",
            show=self.BulletChar,
            highlightthickness=2,
            highlightcolor='#7E1E1D',
            fg='#7E1E1D',
            textvariable=self.DataVars['QRString']
        )
        self.QREntry.place(
            x=904.0,
            y=782.0,
            width=489.0,
            height=23.0
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

#Start of Entry canvas
    def PlaceEntryCanvas(self):        
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
            font=("OpenSans Regular", 36 * -1)
        )

        self.EntryCanvas.create_text(
            458.0,
            284.0,
            anchor="nw",
            text="Klantgegevens",
            fill="#13799F",
            font=("OpenSans Regular", 36 * -1)
        )
        
        self.EntryCanvas.create_text(
            458.0,
            550.0,
            anchor="nw",
            text="Order info",
            fill="#13799F",
            font=("OpenSans Regular", 36 * -1)
)

        self.NameEntry = Entry(
            bd=0,
            bg="#FFFFFF",
            highlightthickness=0,
            font=("OpenSans Light", 21 * -1),
            textvariable=self.DataVars['Name']
        )
        self.NameEntry.place(
            x=458.0,
            y=349.0,
            width=389.0,
            height=33.0
        )

        self.StreetEntry = Entry(
            bd=0,
            bg="#FFFFFF",
            highlightthickness=0,
            font=("OpenSans Light", 21 * -1),
            textvariable=self.DataVars['Street']
        )
        self.StreetEntry.place(
            x=458.0,
            y=397.0,
            width=389.0,
            height=33.0
        )

        self.ZipEntry = Entry(
            bd=0,
            bg="#FFFFFF",
            highlightthickness=0,
            font=("OpenSans Light", 21 * -1),
            textvariable=self.DataVars['Zip']
        )
        self.ZipEntry.place(
            x=458.0,
            y=445.0,
            width=123.0,
            height=33.0
        )

        self.CityEntry = Entry(
            bd=0,
            bg="#FFFFFF",
            highlightthickness=0,
            font=("OpenSans Light", 21 * -1),
            textvariable=self.DataVars['City']
        )
        self.CityEntry.place(
            x=591.0,
            y=445.0,
            width=256.0,
            height=33.0
        )

        self.PhoneEntry = Entry(
            bd=0,
            bg="#FFFFFF",
            highlightthickness=0,
            font=("OpenSans Light", 21 * -1),
            textvariable=self.DataVars['Phone']
        )
        self.PhoneEntry.place(
            x=458.0,
            y=495.0,
            width=389.0,
            height=33.0
        )
        
        self.EntryCanvas.create_text(
            458.0,
            607.0,
            anchor="nw",
            text="Ordernr:",
            fill="#3E3E3E",
            font=("OpenSans Light", 21 * -1)
        )    
            
        self.EntryCanvas.create_text(
            458.0,
            656.0,
            anchor="nw",
            text="Bezorgdatum:",
            fill="#3E3E3E",
            font=("OpenSans Light", 21 * -1)
        )

        self.OrderNrEntry = Entry(
            bd=0,
            bg="#FFFFFF",
            highlightthickness=0,
            font=("OpenSans Light", 21 * -1),
            textvariable=self.DataVars['OrderNr']
        )
        self.OrderNrEntry.place(
            x=624.0,
            y=604.0,
            width=213.0,
            height=33.0
        )

        self.DeliveryDateEntry = Entry(
            bd=0,
            bg="#FFFFFF",
            highlightthickness=0,
            font=("OpenSans Light", 21 * -1),
            textvariable=self.DataVars['DeliveryDate']
        )
        self.DeliveryDateEntry.place(
            x=624.0,
            y=652.0,
            width=213.0,
            height=33.0
        )  
          
        self.EntryCanvas.create_text(
            926.0,
            388.0,
            anchor="nw",
            text="Bestemming:",
            fill="#3E3E3E",
            font=("OpenSans Light", 24 * -1)
        )
        self.EntryCanvas.create_text(
            926.0,
            473.0,
            anchor="nw",
            text="Aantal tassen:",
            fill="#3E3E3E",
            font=("OpenSans Light", 24 * -1)
        )
        self.EntryCanvas.create_text(
            926.0,
            558.0,
            anchor="nw",
            text="Aantal dozen:",
            fill="#3E3E3E",
            font=("OpenSans Light", 24 * -1)
        )
        self.EntryCanvas.create_text(
            926.0,
            643.0,
            anchor="nw",
            text="Aantal droog:",
            fill="#3E3E3E",
            font=("OpenSans Light", 24 * -1)
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
        for i in range(len(self.QuantityVars)):
            if i == 0:
                self.item_var = self.QuantityVars['DeliveryNo']
            elif i == 1:
                self.item_var = self.QuantityVars['BagQty']
            elif i == 2:
                self.item_var = self.QuantityVars['BoxQty']
            else: 
                self.item_var = self.QuantityVars['DryQty']       

            self.PlusBtn = Button(
                image=self.PlusBtnImg,
                bg='#FFFFFF',
                borderwidth=0,
                highlightthickness=0,
                command=lambda var=self.item_var: self.SetQuantity(var, '+'),
                relief="flat"
            )
            self.PlusBtn.place(
                x=1323.0,
                y=371.0 + (i * 85),
                width=55.0,
                height=55.0
            )

            self.MinusBtn = Button(
                image=self.MinusBtnImg,
                bg='#FFFFFF',
                borderwidth=0,
                highlightthickness=0,
                command=lambda var=self.item_var: self.SetQuantity(var, '-'),
                relief="flat"
            )
            self.MinusBtn.place(
                x=1243.0,
                y=371.0 + (i * 85),
                width=55.0,
                height=55.0
            )  
                            
            self.QuantityLabel = Label(
                textvariable=self.item_var,
                fg='#3E3E3E',
                bg='#FFFFFF',
                width='3'
                
            )
            self.QuantityLabel.config(font=("OpenSans Regular", 34 * -1))
            self.QuantityLabel.place(
                x=1135.0,
                y=382.0 + (i * 85),
            )
        for entry in [self.NameEntry, self.StreetEntry, self.ZipEntry, self.CityEntry, self.PhoneEntry, self.OrderNrEntry, self.DeliveryDateEntry]:
            entry.config(fg='#3E3E3E')    
            
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
        self.PrintQuantity.config(font=("OpenSans Regular", 24 * -1))
        self.PrintQuantity.place(
            x=1080.0,
            y=500.0,
        )
        
        
        self.PrinterStatus = Label(
            textvariable=self.DataVars['StatusMsg'],
            fg='#3E3E3E',
            bg='#FFFFFF',       
        )
        self.PrinterStatus.config(font=("OpenSans Regular", 18 * -1))
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
            font=("OpenSans Regular", 36 * -1)
        )


        self.LblPreviewImg = ImageTk.PhotoImage(self.ZPLF.LabelPreview())
        self.PreviewImage = Label(master=self.master, image=self.LblPreviewImg)
        self.PreviewImage.place(
            x=575.0,
            y=436.0,
        )
        
        self.PrintLabel()       

        
    # def ManualEntry(self):
        # self.QRFrame.grid_forget()
        # self.BuildCustomerWidgets()
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
        DeliveryNo = self.QuantityVars['DeliveryNo'].get()
        DeliveryNo -= 1
        self.QuantityVars['DeliveryNo'].set(DeliveryNo)
        
        for var in [self.QuantityVars['BagQty'], self.QuantityVars['BoxQty'], self.QuantityVars['DryQty']]:
            var.set(0)
        
        self.DataVars['StatusMsg'].set('  ')
        self.PrintCanvas.delete('all')
        self.EntryCanvas.delete('all')
        self.PlaceRootCanvas()
        
        
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
                qr_lst = QRString.strip('><=').split(',')
                v_nme, v_str, v_zip, v_cty, v_tel, v_ddt, v_onr, validate = qr_lst
                break
            except ValueError:
                self.DataVars['StatusMsg'].set('Gescande code is niet geldig!')
                self.StatusMessage.config(fg='red')
                self.QREntry.delete(0, 'end')
                self.QREntry.focus()
                return False
                
        self.RootCanvas.delete('all')
        
        self.DataVars['Name'].set(v_nme)
        self.DataVars['Street'].set(v_str)        
        self.DataVars['Zip'].set(v_zip)
        self.DataVars['City'].set(v_cty)
        self.DataVars['Phone'].set(v_tel)
        self.DataVars['DeliveryDate'].set(v_ddt)
        self.DataVars['OrderNr'].set(v_onr)
        self.QREntry.delete(0, 'end')
        self.PlaceEntryCanvas()
        
        return True
        
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
        self.Quantities = self.QuantityVars['BagQty'].get() + self.QuantityVars['BoxQty'].get() + self.QuantityVars['DryQty'].get()
        
        if self.Quantities == 0:
            mbox.showerror(title='Foutmelding', message='Er zijn geen aantallen ingevuld!')
        else:             
            self.SetLabelVars()

    def SetLabelVars(self):
        LabelVars = []
        for var in [self.QuantityVars['DeliveryNo'], self.QuantityVars['BagQty'], self.QuantityVars['BoxQty'], self.QuantityVars['DryQty'], self.DataVars['Name'], self.DataVars['Street'], self.DataVars['Zip'], self.DataVars['City'], self.DataVars['Phone'],self.DataVars['Operator'], self.DataVars['DeliveryDate'], self.DataVars['OrderNr']]:
            LabelVar = var.get()
            LabelVars.append(LabelVar)
        self.ZPLF.BuildLabel(LabelVars, self.Quantities)
        self.PlacePrintCanvas()

      
def main(): 
    root = Tk()
    root.title('NOVA QR2Label v0.2')
    root.configure(cursor='none')
    
    
    # root.wm_overrideredirect(True)
    #root.wm_attributes('-type', 'splash')
    root.wm_attributes('-fullscreen', True)
    app = MainDialog(root)
    root.update()
    root.mainloop()


if __name__ == '__main__':
    main()