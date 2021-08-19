from tkinter import *
from PIL import ImageTk, Image
import sys
import importlib
from pathlib import Path
import tkinter.messagebox as mbox
import io
from labelfunctions import *

   
class MainDialog:
    def __init__(self, master):
        self.master = master
        self.Path = Path(__file__).parent
        self.Assets = self.Path / Path("./assets")
        self.QuantityVars = {var: IntVar() for var in ['DeliveryNo', 'BoxQty', 'BagQty', 'DryQty']}
        self.DataVars = {var: StringVar() for var in ['QRString','StatusMsg', 'Name', 'Street', 'Zip', 'City', 'Phone']}         
        self.PlaceRootCanvas()
        self.ZPLF = ZPLFunctions()     
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

        self.RootCanvas.create_rectangle(
            651.0,
            288.0,
            801.0,
            438.0,
            fill="#EBEBEB",
            outline="")

        self.RootCanvas.create_rectangle(
            463.0,
            287.0,
            613.0,
            437.0,
            fill="#000000",
            outline="")

        self.RootCanvas.create_rectangle(
            651.0,
            475.0,
            801.0,
            625.0,
            fill="#EBEBEB",
            outline="")

        self.RootCanvas.create_rectangle(
            463.0,
            475.0,
            613.0,
            625.0,
            fill="#EBEBEB",
            outline="")

        self.RootCanvas.create_rectangle(
            651.0,
            662.0,
            801.0,
            812.0,
            fill="#EBEBEB",
            outline="")

        self.RootCanvas.create_rectangle(
            463.0,
            662.0,
            613.0,
            812.0,
            fill="#EBEBEB",
            outline="")

        self.RootCanvas.create_text(
            486.0,
            341.0,
            anchor="nw",
            text="MIKE",
            fill="#FFFFFF",
            font=("Raleway Regular", 36 * -1)
        )

        self.RootCanvas.create_text(
            492.0,
            716.0,
            anchor="nw",
            text="LIZE",
            fill="#000000",
            font=("Raleway Regular", 36 * -1)
        )

        self.RootCanvas.create_text(
            675.0,
            716.0,
            anchor="nw",
            text="NICK",
            fill="#000000",
            font=("Raleway Regular", 36 * -1)
        )

        self.RootCanvas.create_text(
            476.0,
            533.0,
            anchor="nw",
            text="SJAAN",
            fill="#000000",
            font=("Raleway Regular", 32 * -1)
        )

        self.RootCanvas.create_text(
            660.0,
            533.0,
            anchor="nw",
            text="IWONA",
            fill="#000000",
            font=("Raleway Regular", 32 * -1)
        )

        self.RootCanvas.create_text(
            669.0,
            340.0,
            anchor="nw",
            text="JENN",
            fill="#000000",
            font=("Raleway Regular", 36 * -1)
)

        self.QREntryImg = PhotoImage(
            file=self.AppAssets("QREntry.png"))
        self.QREntryBg = self.RootCanvas.create_image(
            1148.5,
            749.5,
            image=self.QREntryImg
        )
        self.BulletChar = "\u2022" #Specification of bullet character
        self.QREntry = Entry(
            bd=0,
            bg="#CEDBFF",
            show=self.BulletChar,
            highlightthickness=0,
            textvariable=self.DataVars['QRString']
        )
        self.QREntry.place(
            x=904.0,
            y=732.0,
            width=489.0,
            height=33.0
        )
        self.StatusMessage = Label(
            textvariable=self.DataVars['StatusMsg'],
            fg='#3E3E3E',
            bg='#FFFFFF'
        )
        self.StatusMessage.config(font=("OpenSans Light", 16))
        self.StatusMessage.place(
            x=904.0,
            y=683.0,
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

        self.EntryCanvas.place(x = 0, y = 0)
        self.EntryCanvas.create_rectangle(
            420.0,
            236.0,
            1500.0,
            844.0,
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

        self.NameEntry = Entry(
            bd=0,
            bg="#FFFFFF",
            highlightthickness=0,
            font=("Raleway Regular", 21 * -1),
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
            font=("Raleway Regular", 21 * -1),
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
            font=("Raleway Regular", 21 * -1),
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
            font=("Raleway Regular", 21 * -1),
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
            font=("Raleway Regular", 21 * -1),
            textvariable=self.DataVars['Phone']
        )
        self.PhoneEntry.place(
            x=458.0,
            y=495.0,
            width=389.0,
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
            y=765.0,
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
            y=765.0,
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
#Print Splash Window            
    def PlacePrintCanvas(self):
        self.PrintBtn.config(state=DISABLED)
        self.PrintQty = IntVar()
        self.PrintQty.set(self.Quantities)
        # self.StatusLabel = Label(self.PrintFrame, textvariable=self.StatusVariable, font=("Calibri", 18), bg='white')
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
                qr_lst = QRString.strip('/><=').split(',')
                v_nme, v_str, v_zip, v_cty, v_tel, validate = qr_lst
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
        for var in [self.QuantityVars['DeliveryNo'], self.QuantityVars['BagQty'], self.QuantityVars['BoxQty'], self.QuantityVars['DryQty'], self.DataVars['Name'], self.DataVars['Street'], self.DataVars['Zip'], self.DataVars['City'], self.DataVars['Phone']]:
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