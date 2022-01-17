import io
from simple_zpl2 import ZPLDocument
from PIL import Image
import configparser
import socket
from pathlib import Path

class NetworkPrinter(object):
    def __init__(self, ip_address, port=9100):
        self.ip = ip_address
        self.port = port

    def print_zpl(self, zpl_document, timeout=10):
        """
        Send ZPL2 formatted text to a network label printer
        :param zpl_document: Document object, fully build for label.
        :param timeout: Socket timeout for printer connection, default 10.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)
            s.settimeout(timeout)
            s.connect((self.ip, self.port))
            s.send(zpl_document.zpl_bytes)
            print(zpl_document.zpl_bytes)
    
class ZPLFunctions:
    def BuildLabel(self, listvar, qty):
        OrderType, DeliveryNumber, BoxQty, DryQty, CustName, CustStreet, CustZip, CustCity, CustPhone, Operator, Date, OrderNr = listvar
        self.zpl = ZPLDocument()

        #Alignment settings and shared label borders
        self.zpl.add_zpl_raw('^MMT^PW831^LL0440^LS0'
                             '^FO0,20^GFA,46592,46592,00104,:Z64:eJzszTERgDAUBbDPMTAiASmVBtKQggRGBq7FxRu4xEBqHgFXVUs8vSrRjHFMmedcMs+9Zp4n9WyZ5009LfP09lbA1tudeJbYs18ej8fj8Xg8Ho/H4/F4PB6Px+PxeDwej8fj8Xg8Ho/H4/F4PB6Px+PxeDwej8fj8Xg8Ho/H4/F4PB6Px+PxeDwej8fj8Xg8Ho/H4/F4PB6Px+PxeDwej8fj8Xg8Ho/H4/F4PB6Px+PxeDyePzwfAAAA///t1LENgCAARUGsLBnBUVjN0RiJ0sKgW/wQcm+B6x6Hw+FwOBwOh8PhcDgcDofD4XA4HA6Hw+FwOBwOh8PhcDgcDofD4XDWcNrYzPkixZwr47wpp2acJ+WcGWccGaeXjHOXlmBmYjrStv2w2OoE:11E9'
                             '^FO496,377^GB329,0,5^FS^FO6,233^GB818,0,5^FS^FO496,305^GB329,0,5^FS^FO247,236^GB0,216,5^FS^FO491,236^GB0,216,5^FS')

        #Order quantity data fields
        self.zpl.add_field_origin(62, 290)
        self.zpl.add_field_block(180,1,0,'C')
        self.zpl.add_zpl_raw('^A0N,114,140')
        self.zpl.add_field_data(BoxQty) 

        self.zpl.add_field_origin(304, 290)
        self.zpl.add_field_block(180,1,0,'C')
        self.zpl.add_zpl_raw('^A0N,114,140')
        self.zpl.add_field_data(DryQty) 
        
        self.zpl.add_field_origin(567, 243)
        self.zpl.add_field_block(200,1,0,'C')
        self.zpl.add_zpl_raw('^A0N,30,40')
        self.zpl.add_field_data(Operator) 
        
        self.zpl.add_field_origin(567, 315)
        self.zpl.add_field_block(200,1,0,'C')
        self.zpl.add_zpl_raw('^A0N,30,40')
        self.zpl.add_field_data(OrderNr) 
        
        self.zpl.add_field_origin(547, 388)
        self.zpl.add_field_block(230,1,0,'C')
        self.zpl.add_zpl_raw('^A0N,30,40')
        self.zpl.add_field_data(Date)        
        
        if OrderType == 'D':        
            #Row separators, labeltext
            self.zpl.add_zpl_raw('^FO328,27^GB0,208,5^FS'                                 
                                 '^FT544,441^A0N,24,36^FB231,1,0,C^FH^FDBEZORGDATUM^FS'
                                 '^FT31,223^A0N,24,36^FB269,1,0,C^FH^FDBESTEMMING NR.^FS'
                                 '^LRY^FO16,199^GB307,0,29^FS^LRN'
                                 )               
            #Phone Icon 
            self.zpl.add_zpl_raw('^FO320,158^GFA,00512,00512,00008,:Z64:eJxjYBjxgANK1+OiG7Dz7dFoOwZUWgZKy0FpHijNB6XZoTQzVD/jAQEI4wHUhoL/ENoeSstDaXYozQilGfY3MJALAJCpExs=:2D73')     
            
            #Destination number
            self.zpl.add_field_origin(37, 45)
            self.zpl.add_field_block(300,1,0,'C')
            self.zpl.add_zpl_raw('^A0N,180,177')
            self.zpl.add_field_data(DeliveryNumber) 

            # Customer data
            self.zpl.add_zpl_raw('^FT347,72^A0N,35,35^FH\^FD' + str(CustName) + '^FS'
                                 '^FT347,112^A0N,35,35^FH\^FD' + str(CustStreet) + '^FS'
                                 '^FT347,155^A0N,35,35^FH\^FD' + str(CustZip) + '^FS'
                                 '^FT475,155^A0N,35,35^FH\^FD' + str(CustCity) + '^FS'
                                 '^FT374,215^A0N,35,35^FH\^FD' + str(CustPhone) + '^FS')
        elif OrderType == 'C':
            #Row separators, labeltext'^FO328,236^GB0,218,5^FS'
            self.zpl.add_zpl_raw(
                                 '^FO6,193^GB818,0,5^FS'
                                 '^FT544,441^A0N,24,36^FB231,1,0,C^FH^FDAFHAALDATUM^FS')  
            self.zpl.add_field_origin(55, 45)
            self.zpl.add_field_block(720,2,0,'C')
            self.zpl.add_zpl_raw('^A0N,75,75')
            self.zpl.add_field_data(CustName)
            self.zpl.add_field_origin(55, 205)
            self.zpl.add_field_block(720,1,0,'C')
            self.zpl.add_zpl_raw('^A0N,27,37')
            self.zpl.add_field_data('AFHAALLOCATIE: RIJSWIJK')
            # self.zpl.add_field_data('AFHAALLOCATIE: ' + str(CollectLocation))

        
        #Bottom Layer shared label data
        self.zpl.add_zpl_raw('^FT80,441^A0N,24,36^FB101,1,0,C^FH^FDDOZEN^FS'
                             '^FT321,441^A0N,24,36^FB108,1,0,C^FH^FDDROOG^FS'
                             '^FT536,295^A0N,24,36^FB247,1,0,C^FH^FDINGEPAKT DOOR^FS'
                             '^FT537,367^A0N,24,36^FB245,1,0,C^FH^FDORDERNUMMER^FS'
                             '^LRY^FO16,417^GB225,0,29^FS^LRN'

                             '^LRY^FO258,417^GB228,0,29^FS^LRN'
                             '^LRY^FO500,417^GB318,0,29^FS^LRN'
                             '^LRY^FO500,271^GB318,0,29^FS^LRN'
                             '^LRY^FO500,343^GB318,0,29^FS^LRN')
        #Limit printing speed
        self.zpl.add_zpl_raw('^PR2,4,2')
        self.zpl.add_print_quantity(qty, 0, 0, 'N', 'Y')
        
    def LabelPreview(self):
        png = self.zpl.render_png(label_width=4.1, label_height=2.2)
        GenerateImg = io.BytesIO(png)
        PreviewImg = Image.open(GenerateImg)
        PreviewImg = PreviewImg.resize((350, 188), Image.ANTIALIAS)
        return PreviewImg

    def Printer(self):
        self.Path = Path(__file__).parent
        self.config = configparser.ConfigParser()
        self.config.read(self.Path / Path("./config.ini"))
        self.PrinterIP = self.config.get('Network', 'PRINTER_IP_ADDRESS')
        printer = NetworkPrinter(str(self.PrinterIP))
        printer.print_zpl(self.zpl)    
    

    
    
    
    



