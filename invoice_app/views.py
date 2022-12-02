from django.shortcuts import render
from .modelforms import invoiceform, lineitemformset
# Create your views here.

def invoicegen(request):
    if request.method == 'POST':
        print(request.POST)
    invoice = invoiceform()
    lineitems = lineitemformset()
    context = {'invoice': invoice,'lineitems':lineitems}
    return render(request, 'invoicegen.html', context)