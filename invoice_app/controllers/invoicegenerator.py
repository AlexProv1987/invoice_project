import datetime
from decimal import *
from invoice_app.models import invoice,lineitem,invoicefile
from product_app.models import product
from business_app.models import business,client
from invoicegenie.project_classes.helperclass import postreqhelpers
'''class to handle post request and create invoice object and all related objects'''
class handleinvoicegen():
    def __init__(self, postreq):
        self.invoice = postreqhelpers.parsepost(postdict=postreq,keys=('bus_reltn', 'client_reltn'))
        self.postrequest = postreq
        self.inv_id = 0
        self._createinvoice()

    def _createinvoice(self):
        biller = business.objects.get(id=self.invoice['bus_reltn'])
        billedto = client.objects.get(id=self.invoice['client_reltn'])
        products_overall_qty = self._gettotalproducts()
        newinv = invoice.objects.create(
            bus_reltn = biller,
            client_reltn = billedto,
            line_item_cnt = self.postrequest['form-TOTAL_FORMS'],
            product_qty = products_overall_qty,
            inv_status = 1,
            inv_billed_date = datetime.datetime.today()
        )
        print(newinv.id)
        print(products_overall_qty)
        print(biller.bus_name, billedto.client_name)
        
        return None

    def _gettotalproducts(self) -> int:
        sum = 0
        for value in range(int(self.postrequest['form-TOTAL_FORMS'])):
            sum+= int(self.postrequest[f'form-{value}-line_item_qty'])
        return sum

    def _gettotalbilled(self) -> Decimal:
        pass

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
>

'''