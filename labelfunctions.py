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
        DeliveryNumber, BagQty, BoxQty, DryQty, CustName, CustStreet, CustZip, CustCity, CustPhone, Operator, DeliveryDate, OrderNr = listvar
        self.zpl = ZPLDocument()

        #Borders
        self.zpl.add_zpl_raw('^FO0,0^GFA,46592,46592,00104,:Z64:eJzs0jERwzAUBcGfUaHSEAzF0CxogmIIKVNZZvHGM9kjsM1V6dW1FWhU7QnnV3UmnLsqwaxVn4wz2p2Y7Zjtm3C22a+E068+E06LOVvKGRwOh8PhcDgcDofD4XA4HA6Hw+FwOBwOh8PhcDgcDofD4XA4HA6Hw+FwOBwOh8PhcDgcDofD4XA4HA6Hw+FwOBwOh8PhcDgcDofD4XA4HA6Hw+FwOBwOh8PhcDgcDofD4XA4HA6Hw+FwOP/pPAAAAP//7dIxDYBAFAXBT66gRAJSQdpJOQmUVICLRyCzBqZZDofD4XA4HA6Hw+FwOBwOh8PhcDgcDofD4XA4HA6Hw+FwOBwOh8P5qjOnnP4zZyScebQj4Sy93ZH6lHH2yjhVW4K5qtaEcyZmk6RXegD3HFrD:A509^FO6,238^GB489,0,5^FS^FO165,238^GB167,198,5^FS^FO328,7^GB0,231,5^FS^FO491,216^GB0,216,5^FS^FO496,357^GB329,0,5^FS^FO330,213^GB495,0,5^FS^FO496,285^GB329,0,5^FS')
        
        #Phone Icon
        
        self.zpl.add_zpl_raw('^FO320,140^GFA,00512,00512,00008,:Z64:eJxjYBjxgANK1+OiG7Dz7dFoOwZUWgZKy0FpHijNB6XZoTQzVD/jAQEI4wHUhoL/ENoeSstDaXYozQilGfY3MJALAJCpExs=:2D73')
        
        
        # Route order value
        # X, Y
        self.zpl.add_field_origin(33, 40)
        self.zpl.add_field_block(300,1,0,'C')
        self.zpl.add_zpl_raw('^A0N,180,177')
        self.zpl.add_field_data(DeliveryNumber) #INSERT ADDRESS ORDER VALUE

        self.zpl.add_field_origin(17, 280)
        self.zpl.add_field_block(180,1,0,'C')
        self.zpl.add_zpl_raw('^A0N,114,140')
        self.zpl.add_field_data(BagQty) #INSERT BAG

        self.zpl.add_field_origin(180, 280)
        self.zpl.add_field_block(180,1,0,'C')
        self.zpl.add_zpl_raw('^A0N,114,140')
        self.zpl.add_field_data(BoxQty) #INSERT BOX

        self.zpl.add_field_origin(342, 280)
        self.zpl.add_field_block(180,1,0,'C')
        self.zpl.add_zpl_raw('^A0N,114,140')
        self.zpl.add_field_data(DryQty) #INSERT DRY
        
        self.zpl.add_field_origin(567, 223)
        self.zpl.add_field_block(200,1,0,'C')
        self.zpl.add_zpl_raw('^A0N,30,40')
        self.zpl.add_field_data(Operator) #INSERT OPERATOR
        
        
        self.zpl.add_field_origin(567, 295)
        self.zpl.add_field_block(200,1,0,'C')
        self.zpl.add_zpl_raw('^A0N,30,40')
        self.zpl.add_field_data(OrderNr) #INSERT ORDER NUMBER
        
        self.zpl.add_field_origin(567, 368)
        self.zpl.add_field_block(200,1,0,'C')
        self.zpl.add_zpl_raw('^A0N,30,40')
        self.zpl.add_field_data(DeliveryDate) #INSERT DELIVERY DATE     
        
        # Labels
        self.zpl.add_zpl_raw('^FT31,228^A0N,24,36^FB269,1,0,C^FH\^FDBESTEMMING NR.^FS^FT26,421^A0N,24,36^FB125,1,0,C^FH\^FDTASSEN^FS^FT358,421^A0N,24,36^FB108,1,0,C^FH\^FDDROOG^FS^FT198,421^A0N,24,36^FB101,1,0,C^FH\^FDDOZEN^FS^FT544,421^A0N,24,36^FB231,1,0,C^FH\^FDBEZORGDATUM^FS^FT536,275^A0N,24,36^FB247,1,0,C^FH\^FDINGEPAKT DOOR^FS^FT537,347^A0N,24,36^FB245,1,0,C^FH\^FDORDERNUMMER^FS')

        # Label Backgrounds

        self.zpl.add_zpl_raw('^LRY^FO13,204^GB310,0,29^FS^LRN ^LRY^FO13,397^GB148,0,29^FS^LRN ^LRY^FO338,397^GB148,0,29^FS^LRN ^LRY^FO175,397^GB148,0,29^FS^LRN ^LRY^FO500,397^GB318,0,29^FS^LRN ^LRY^FO500,251^GB318,0,29^FS^LRN ^LRY^FO500,323^GB318,0,29^FS^LRN')

        # Customer data
        self.zpl.add_zpl_raw('^FT347,58^A0N,28,28^FH\^FD' + str(CustName) + '^FS ^FT347,95^A0N,28,28^FH\^FD' + str(CustStreet) + '^FS ^FT347,135^A0N,28,28^FH\^FD' + str(CustZip) + '^FS ^FT452,135^A0N,28,28^FH\^FD' + str(CustCity) + '^FS ^FT374,195^A0N,28,28^FH\^FD' + str(CustPhone) + '^FS')

        self.zpl.add_print_quantity(qty, 0, 0, 'N', 'Y')
        # Get PNG byte array
        
    def LabelPreview(self):
        png = self.zpl.render_png(label_width=4.1, label_height=2.2)
        GenerateImg = io.BytesIO(png)
        PreviewImg = Image.open(GenerateImg)
        PreviewImg = PreviewImg.resize((350, 188), Image.ANTIALIAS)
        return PreviewImg

        
    # def LabelPrint(self):
        # self.printer = TCPPrinter('192.168.1.242')  # CHANGE TO YOUR PRINTER IP
        # self.printer.send_job(self.zpl)
        
    def Printer(self):
        self.Path = Path(__file__).parent
        self.config = configparser.ConfigParser()
        self.config.read(self.Path / Path("./config.ini"))
        self.PrinterIP = self.config.get('Network', 'PRINTER_IP_ADDRESS')
        printer = NetworkPrinter(str(self.PrinterIP))
        printer.print_zpl(self.zpl)    
    

    
    
    
    



