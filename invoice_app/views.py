from django.shortcuts import render
from .modelforms import invoiceform, lineitemformset
from .controllers.invoicegenerator import handleinvoicegen
# Create your views here.

def invoicegen(request):
    if request.method == 'POST':
        handleinvoicegen(request.POST)
        '''Test Code'''
        '''End Test code'''
    invoice = invoiceform()
    lineitems = lineitemformset()
    context = {'invoice': invoice,'lineitems':lineitems}
    return render(request, 'invoicegen.html', context)