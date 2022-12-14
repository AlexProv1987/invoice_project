import datetime
from django.shortcuts import render,redirect
from .modelforms import invoiceform, lineitemformset
from apps.invoice_app.models import invoice,lineitem, invoicefile
from .controllers.invoicegenerator import handleinvoicegen, generatepdf
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.

#view method will be split later, just sticking to one for testing
@login_required
@permission_required('invoice_app.add_invoice', raise_exception=True)
def invoicegen(request):
    if request.method == 'POST':
        invoice = invoiceform(request.POST)
        lineitems = lineitemformset(request.POST)
        if(invoice.is_valid() and lineitems.is_valid()):
            newinv = handleinvoicegen(request.POST)
            if newinv.issuccess:
                generatepdf(newinv.lineitemobj,newinv.invobj)
                return redirect('inv-view',newinv.invobj.bus_reltn.bus_name,newinv.invobj.pk)
            else:
                invoice = invoiceform()
                lineitems = lineitemformset()
                context = {'invoice': invoice,'lineitems':lineitems}
                messages.error(request,'Failed to Save Invoice. Please Contact your System Administrator')
                return render(request, 'invoicegen.html', context)
        else:
            invoice = invoiceform()
            lineitems = lineitemformset()
            context = {'invoice': invoice,'lineitems':lineitems}
            messages.error(request,'Failed to validate Product or Units.')
            return render(request, 'invoicegen.html', context)
    invoice = invoiceform()
    lineitems = lineitemformset()
    context = {'invoice': invoice,'lineitems':lineitems}
    return render(request, 'invoicegen.html', context)

#returns invoice obj view
@login_required
@permission_required('invoice_app.view_invoice',raise_exception=True)
def invoicesview(request,bus,pk):
    invobj = get_object_or_404(invoice,pk=pk)
    invli = lineitem.objects.filter(inv_reltn=pk)
    context = {'invobj': invobj, 'invli':invli}
    return render(request, 'invoiceview.html', context=context)

#get file_loc and return to client
@login_required
@permission_required('invoice_app.view_invoicefile',raise_exception=True)
def downloadpdf(request, bus, pk):
    file = get_object_or_404(invoicefile,inv_reltn=pk)
    return FileResponse(open(file.file_loc, 'rb'), as_attachment=True, content_type='application/pdf')

'''this needs to be one method, use form send something in post req dictating what to do'''
#updates invoice status
@login_required
@permission_required('invoice_app.change_invoice',raise_exception=True)
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
@login_required
@permission_required('invoice_app.change_invoice',raise_exception=True)
def cancelinvoice(request, bus, pk):
    inv = get_object_or_404(invoice,pk=pk)
    inv.inv_status = invoice.Cancelled
    inv.save()
    messages.success(request,f'INV{pk} For {inv.bus_reltn.bus_name} Set To {inv.get_inv_status_display()}.')
    return redirect(request.META.get('HTTP_REFERER'))