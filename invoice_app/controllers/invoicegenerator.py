import datetime
from decimal import *
from invoice_app.models import invoice,lineitem,invoicefile
from product_app.models import product
from business_app.models import business,client
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
        try:
            newinv = invoice.objects.create(
                bus_reltn = biller,
                client_reltn = billedto,
                line_item_cnt = self.postrequest['form-TOTAL_FORMS'],
                product_qty = products_overall_qty,
                total_billed = self._gettotalbilled(),
                inv_status = invoice.Generated,
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

#we have to inherit the base FPDF class to create our own header and footer methods as the default return none
class myFPDF(FPDF):

    def header(self) -> None:
        pass
    def footer(self) -> None:
        pass

class generatepdf():

    def __init__(self, liobj, invobj):
        self.inv = invobj
        self.lineitems = liobj
        self.pdffile = f'{self.inv.pk}.pdf'
        self._pdfgeneration()

    def _pdfgeneration(self):
        pdf = myFPDF('P', 'mm', 'A4')
        pdf.add_page()
        pdf.set_font('courier', 'B', 12)
        pdf.cell(40,10, f'Invoice#{self.inv.pk}'.rjust(40),0,1)
        pdf.cell(200,10, f"{'Pay To:'.ljust(35)} {'Client:'.rjust(20)}",0,1)
        pdf.set_font('courier', '', 12)
        pdf.cell(200,10,f"{str(self.inv.bus_reltn.bus_name).ljust(35)} {str(self.inv.client_reltn.client_name).rjust(24)}",0,1)
        pdf.cell(200,10,f"{str(self.inv.bus_reltn.bus_street).ljust(35)} {str(self.inv.client_reltn.client_street).rjust(24)}",0,1)
        pdf.cell(200,10,f"{str(self.inv.bus_reltn.bus_zip).ljust(35)} {str(self.inv.client_reltn.client_zip).rjust(24)}",0,1)
        pdf.cell(200,10,f"{str(self.inv.bus_reltn.bus_phone).ljust(35)} {str(self.inv.client_reltn.client_phone).rjust(24)}",0,1)
        pdf.cell(200,10,f"{str(self.inv.bus_reltn.bus_email).ljust(35)} {str(self.inv.client_reltn.client_email).rjust(24)}",0,1)
        pdf.ln(10)
        pdf.set_font('courier', '', 12)
        pdf.cell(200, 8, f"{'Item'.ljust(30)} {'Qty'.rjust(20)} {'Total'.rjust(10)}", 0, 1)
        for li in self.lineitems:
            pdf.cell(200, 8, f"{str(li.product.p_name).ljust(30)} {str(li.line_item_qty).rjust(20)} {str(li.line_item_amt).rjust(10)}" , 0, 1)
        pdf.ln(10)
        pdf.cell(200,8,f"{''.ljust(30)} {'Qty Total'.rjust(25)} {'Total Due'.rjust(10)}", 0, 1)
        pdf.cell(200, 8, f"{''.ljust(30)} {str(self.inv.product_qty).rjust(20)} {str(self.inv.total_billed).rjust(15)}" , 0, 1)
        pdf.output(self.pdffile, 'F')

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