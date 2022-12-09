from django.shortcuts import render,redirect
from .modelforms import invoiceform, lineitemformset
from apps.invoice_app.models import invoice,lineitem, invoicefile
from .controllers.invoicegenerator import handleinvoicegen, generatepdf
from invoicegenie.project_classes.modelobjupdater import updatemodelobj
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.contrib import messages
# Create your views here.

#view method will be split later, just sticking to one for testing
def invoicegen(request):
    if request.method == 'POST':
        newinv = handleinvoicegen(request.POST)
        generatepdf(newinv.lineitemobj,newinv.invobj)  
        return redirect('inv-view',newinv.invobj.bus_reltn.bus_name,newinv.invobj.pk)
    invoice = invoiceform()
    lineitems = lineitemformset()
    context = {'invoice': invoice,'lineitems':lineitems}
    return render(request, 'invoicegen.html', context)

#returns invoice obj view
def invoicesview(request,bus,pk):
    invobj = invoice.objects.get(pk=pk)
    invli = lineitem.objects.filter(inv_reltn=pk)
    context = {'invobj': invobj, 'invli':invli}
    return render(request, 'invoiceview.html', context=context)

#get file_loc and return to client
def downloadpdf(request, bus, pk):
    file = get_object_or_404(invoicefile,inv_reltn=pk)
    return FileResponse(open(file.file_loc, 'rb'), as_attachment=True, content_type='application/pdf')

#updates invoice status on click(ajax call to back end)
def updateinvoice(request,bus,pk):
    inv = get_object_or_404(invoice,pk=pk)
    inv.inv_status = invoice.ReadyToBill
    inv.save()
    messages.success(request,f'INV{pk} For {inv.bus_reltn.bus_name} Set To Ready To Bill.')
    return redirect(request.META.get('HTTP_REFERER'))