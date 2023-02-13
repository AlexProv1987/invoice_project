import datetime
from decimal import *
from apps.invoice_app.models import invoice,lineitem
from apps.product_app.models import product
from apps.business_app.models import business,client
from invoicegenie.project_classes.helperclass import postreqhelpers
from django.core.exceptions import FieldError
from fpdf import FPDF
'''class to handle post request and create invoice object and all related objects'''
class handleinvoicegen():

    def __init__(self, postreq):
        self.invoice = postreqhelpers.parsepost(postdict=postreq,keys=('bus_reltn', 'client_reltn'))
        self.postrequest = postreq
        self.invobj = invoice.objects.none()
        self.lineitemobj = []
        self.issuccess = False
        if self._createinvoiceobj():
            if self._createlineitems():
                self.issuccess = True

    def _createinvoiceobj(self) -> bool:
        biller = business.objects.get(id=self.invoice['bus_reltn'])
        billedto = client.objects.get(id=self.invoice['client_reltn'])
        products_overall_qty = self._gettotalproducts()
        total_billed = self._gettotalbilled()
        try:
            newinv = invoice.objects.create(
                bus_reltn = biller,
                client_reltn = billedto,
                line_item_cnt = self.postrequest['form-TOTAL_FORMS'],
                product_qty = products_overall_qty,
                total_billed = total_billed,
                inv_status = invoice.Generated,
                inv_generated_date = datetime.date.today(),
                curr_amt_due = total_billed
            )
        except FieldError:
            return False

        if(newinv.pk != 0):
            self.invobj = newinv
            return True
        else:
            return False

    def _createlineitems(self) -> bool:
        lineitem_objects = []
        for value in range(int(self.postrequest['form-TOTAL_FORMS'])):
            product_billed = product.objects.get(id=int(self.postrequest[f'form-{value}-product']))
            lineitem_objects.append(
                lineitem(
                    inv_reltn = self.invobj,
                    product = product_billed,
                    line_item_qty = int(self.postrequest[f'form-{value}-line_item_qty']),
                    line_item_amt = product_billed.p_price * Decimal(self.postrequest[f'form-{value}-line_item_qty'])
                )
            )
        
        if(len(lineitem_objects) != 0):
            lineitem.objects.bulk_create(lineitem_objects)
            self.lineitemobj = lineitem_objects
            return True

    def _gettotalproducts(self) -> int:
        sum = 0
        for value in range(int(self.postrequest['form-TOTAL_FORMS'])):
            sum+= int(self.postrequest[f'form-{value}-line_item_qty'])
        return sum

    def _gettotalbilled(self) -> Decimal:
        totalBilled = 0.00
        for value in range(int(self.postrequest['form-TOTAL_FORMS'])):
            curr_product = product.objects.get(id=int(self.postrequest[f'form-{value}-product']))
            product_total = curr_product.p_price * Decimal(self.postrequest[f'form-{value}-line_item_qty'])
            totalBilled+=product_total
        return totalBilled

'''
we have to inherit the base FPDF class to create our own header and footer methods as the default return none
we need to super the constructor so we can pass our instance of the invoice object to the class without re querying
'''
class custFPDF(FPDF):
    def __init__(self, orientation, unit,format, invobj):
        super(custFPDF,self).__init__()
        self.cur_orientation = orientation
        self.unit = unit
        self.format = format
        self.invoice = invobj

    def header(self) -> None:
        today = datetime.date.today()
        #first line 
        self.set_font('Times', 'B', 15)
        self.cell(100,0,f"{str(self.invoice.bus_reltn.bus_name)}",ln=0)
        #removing image until one is attained
        #self.image('./busimgs/testlogo2.PNG', 95, 8, 33)
        self.set_font('Times', 'B', 10)
        self.cell(100,0,'INVOICE'.rjust(90), ln=1)
        self.ln(6)
        #second line
        self.set_font('Times', '', 12)
        self.cell(100,0,f"{self.invoice.bus_reltn.bus_street}",ln=0)
        self.set_font('Times','', 8)
        self.cell(100,0,f'INV{str(self.invoice.pk)}'.rjust(119), ln=1)
        self.ln(6)
        #third line
        self.set_font('Times', '', 12)
        self.cell(100,0,f"{self.invoice.bus_reltn.bus_city},{self.invoice.bus_reltn.bus_state}",ln=0)
        self.set_font('Times', 'B', 10)
        self.cell(100,0,f'DATE'.rjust(93), ln=1)
        self.ln(6)
        #fourth line
        self.set_font('Times', '', 12)
        self.cell(100,0,f"{self.invoice.bus_reltn.bus_phone}",ln=0)
        self.set_font('Times', '', 8)
        self.cell(100,0,f'{today.strftime("%b %d %Y")}'.rjust(110), ln=1)
        self.ln(6)
        #fifth line
        self.set_font('Times', '', 12)
        self.cell(100,0,f"{self.invoice.bus_reltn.bus_email}",ln=0)
        self.set_font('Times', 'B', 10)
        self.cell(100,0,'DUE'.rjust(94), ln=1)
        self.ln(6)
        #sixth line
        self.set_font('Times', '', 8)
        self.cell(100,0,'On Receipt'.rjust(190), ln=0)
        self.ln(6)
        #seventh line
        self.set_font('Times', 'B', 10)
        self.cell(100,0,'BALANACE DUE'.rjust(194), ln=0)
        self.ln(6)
        #eigth line
        self.set_font('Times', '', 8)
        self.cell(100,0,f"USD {str(self.invoice.total_billed)}".rjust(190),ln=0)
        self.ln(6)
        # Set up a logo
        #self.image('./busimgs/testlogo2.png', 10, 8, 33)
        # Line break
        self.ln(20)
    
    def footer(self) -> None:
        self.set_y(-10)
        
        self.set_font('Arial', 'I', 8)
        
        # Add a page number
        page = 'Page ' + str(self.page_no()) + '/{nb}'
        self.cell(0, 10, page, 0, 0, 'C')

'''class to handle generating the PDF with db data, utilizes custFPDF'''
class generatepdf():

    def __init__(self, liobj, invobj):
        self.inv = invobj
        self.lineitems = liobj
        #self.invfile = invoicefile.objects.none()
        #self.pdf_file_nm = f'{self.inv.pk}_{self.inv.bus_reltn.bus_name}.pdf'
        self.pdf = self._pdfgeneration()
    def _pdfgeneration(self):
        pdf = custFPDF(orientation='P', unit= 'mm', format='A4', invobj=self.inv)
        #add page calls add header/footer
        pdf.add_page()
        pdf.line(10, 60, 200, 60)
        pdf.set_font('Times', 'B', 15)
        pdf.cell(0,5, 'BILL TO',ln=1)
        pdf.ln(3)
        pdf.set_font('Times', 'B', 14)
        pdf.cell(0,5, f'{self.inv.client_reltn.client_name}', ln=1)
        pdf.set_font('Times', '', 12)
        pdf.cell(0,5, f'{self.inv.client_reltn.client_street}', ln=1)
        pdf.cell(0,5, f'{self.inv.client_reltn.client_city}, {self.inv.client_reltn.client_state}', ln=1)
        pdf.cell(0,5, f'{self.inv.client_reltn.client_phone}', ln=1)
        pdf.cell(0,5, f'{self.inv.client_reltn.client_email}', ln=1)
        pdf.ln(10)
        pdf.set_font('Times', 'B', 12)
        pdf.line(10, 60, 200, 60)
        pdf.line(10, 120, 200, 120)
        pdf.cell(200, 8, f"{'DESCRIPTION'.ljust(40)} {'RATE'.rjust(30)}  {'QTY'.rjust(30)} {'AMOUNT'.rjust(30)}", ln=1)
        pdf.line(10, 128, 200, 128)
        #loop over line items to create pseduo table
        for li in self.lineitems:
            pdf.set_font('Times', '', 12)
            pdf.cell(50,5, f"{li.product.p_name}", ln=0)
            pdf.cell(50,5, f"{str(li.product.p_price).rjust(43)}", ln=0)
            pdf.cell(50,5, f"{str(li.line_item_qty).rjust(34)}", ln=0)
            pdf.cell(50,5, f"{str(li.line_item_amt).rjust(28)}", ln=1)
            pdf.set_font('Times', '', 10)
            pdf.cell(200,8, f"{li.product.p_description}", ln=1)
        #get y axis where our line items ended, since we never know where we end up any additional line draws need
        #to get the curreny Y axis again
        new_y = pdf.get_y()
        #draw a line to end line items with the current y axis position
        pdf.line(10,new_y,200,new_y)
        pdf.ln(5)
        pdf.set_font('Times', 'B', 12)
        pdf.cell(100,0,f"{'TOTAL'.rjust(87)}", ln=0)
        pdf.cell(100,0,f"{str(self.inv.total_billed).rjust(75)}", ln=1)
        new_y = pdf.get_y()
        new_y+=4
        pdf.line(97, new_y, 200, new_y)
        pdf.ln(10)
        pdf.cell(50,0,f"{'BALANCE DUE'.rjust(93)}", ln=0)
        pdf.cell(50,0,f"USD: {str(self.inv.total_billed)}".rjust(118), ln=1)
        new_y = pdf.get_y()
        new_y+=4
        pdf.line(97, new_y, 200, new_y)
        new_y+=2
        pdf.line(97, new_y, 200, new_y)
        pdf.cell(100,0, "Please pay to Robertson's Enterprises.", ln=1)
        pdf.ln(5)
        pdf.cell(100,0, "Thank you for your business.", ln=1)
        return pdf

'''
EX postreq
<QueryDict: 
{
'csrfmiddlewaretoken': ['bNGg0ML2BFdu4LPTseNzWS8MRKi0Mndwyea7OJC6sR11cilMHS4AOiq7IU5gwoVe'], 
'bus_reltn': ['1'], 'client_reltn': ['1'], 
'form-TOTAL_FORMS': ['6'], 
'form-INITIAL_FORMS': ['0'], 
'form-MIN_NUM_FORMS': ['0'], 
'form-MAX_NUM_FORMS': ['1000'], 
'form-0-product': ['1'], 'form-0-line_item_qty': ['1'], 'form-0-id': [''], 
'form-1-product': ['1'], 'form-1-line_item_qty': ['1'], 'form-1-id': [''], 
'form-2-product': ['1'], 'form-2-line_item_qty': ['1'], 'form-2-id': [''], 
'form-3-product': ['1'], 'form-3-line_item_qty': ['1'], 'form-3-id': [''], 
'form-4-product': ['1'], 'form-4-line_item_qty': ['1'], 'form-4-id': [''], 
'form-5-product': ['1'], 'form-5-line_item_qty': ['1'], 'form-5-id': ['']
}
'''