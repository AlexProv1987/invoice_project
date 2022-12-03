import datetime
from decimal import *
from invoice_app.models import invoice,lineitem,invoicefile
from product_app.models import product
from business_app.models import business,client
from invoicegenie.project_classes.helperclass import postreqhelpers
from django.core.exceptions import FieldError
'''class to handle post request and create invoice object and all related objects'''
class handleinvoicegen():

    def __init__(self, postreq):
        self.invoice = postreqhelpers.parsepost(postdict=postreq,keys=('bus_reltn', 'client_reltn'))
        self.postrequest = postreq
        self.invobj = invoice.objects.none()
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

    def _createinvoicepdf(self):
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