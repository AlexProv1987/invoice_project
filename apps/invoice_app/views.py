from django.shortcuts import render,redirect
from .modelforms import invoiceform, lineitemformset
from apps.invoice_app.models import invoice,lineitem
from .controllers.invoicegenerator import handleinvoicegen, generatepdf
from django.contrib import messages
from django.http import FileResponse
# Create your views here.

#view method will be split later, just sticking to one for testing
def invoicegen(request):
    if request.method == 'POST':
        newinv = handleinvoicegen(request.POST)
        #generatepdf(newinv.lineitemobj,newinv.invobj)    
        messages.info(request, f'Created INV{newinv.invobj.pk} For {newinv.invobj.bus_reltn.bus_name} To {newinv.invobj.client_reltn.client_name} Succesfully!')
        return redirect('inv-submit',newinv.invobj.bus_reltn.bus_name,newinv.invobj.pk)
    invoice = invoiceform()
    lineitems = lineitemformset()
    context = {'invoice': invoice,'lineitems':lineitems}
    return render(request, 'invoicegen.html', context)

def invoicesview(request,bus,pk):
    invobj = invoice.objects.get(pk=pk)
    invli = lineitem.objects.filter(inv_reltn=pk)
    context = {'invobj': invobj, 'invli':invli}
    return render(request, 'invoiceview.html', context=context)