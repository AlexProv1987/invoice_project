import datetime
from django.shortcuts import render,redirect
from .modelforms import invoiceform, lineitemformset
from apps.invoice_app.models import invoice,lineitem, invoicefile
from .controllers.invoicegenerator import handleinvoicegen, generatepdf
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
    invobj = get_object_or_404(invoice,pk=pk)
    invli = lineitem.objects.filter(inv_reltn=pk)
    context = {'invobj': invobj, 'invli':invli}
    return render(request, 'invoiceview.html', context=context)

#get file_loc and return to client
def downloadpdf(request, bus, pk):
    file = get_object_or_404(invoicefile,inv_reltn=pk)
    return FileResponse(open(file.file_loc, 'rb'), as_attachment=True, content_type='application/pdf')

#updates invoice status
def updateinvoicestatus(request,bus,pk):
    inv = get_object_or_404(invoice,pk=pk)
    if inv.inv_status == invoice.Generated:
        inv.inv_status = invoice.ReadyToBill
        inv.save()
        messages.success(request,f'INV{pk} For {inv.bus_reltn.bus_name} Set To {inv.get_inv_status_display()}.')
    elif inv.inv_status == invoice.ReadyToBill:
        inv.inv_status = invoice.Billed
        inv.inv_billed_date = datetime.date.today()
        inv.save()
        messages.success(request,f'INV{pk} For {inv.bus_reltn.bus_name} Set To {inv.get_inv_status_display()}.')
    elif inv.inv_status == invoice.Billed:
        inv.inv_status = invoice.Paid
        inv.inv_paid_date = datetime.date.today()
        inv.save()
        messages.success(request,f'INV{pk} For {inv.bus_reltn.bus_name} Set To {inv.get_inv_status_display()}.')
    return redirect(request.META.get('HTTP_REFERER'))

#set invoice to cancelled
def cancelinvoice(request, bus, pk):
    inv = get_object_or_404(invoice,pk=pk)
    inv.inv_status = invoice.Cancelled
    inv.save()
    messages.success(request,f'INV{pk} For {inv.bus_reltn.bus_name} Set To {inv.get_inv_status_display()}.')
    return redirect(request.META.get('HTTP_REFERER'))