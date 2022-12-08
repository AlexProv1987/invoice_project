from django.shortcuts import render,redirect
from .modelforms import invoiceform, lineitemformset
from .controllers.invoicegenerator import handleinvoicegen, generatepdf
from django.contrib import messages
from django.http import FileResponse
# Create your views here.

#view method will be split later, just sticking to one for testing
def invoicegen(request):
    if request.method == 'POST':
        newinv = handleinvoicegen(request.POST)
        invpdf = generatepdf(newinv.lineitemobj,newinv.invobj)    
        '''Test Code'''
        #FileResponse(open(invpdf.invfile.file_loc, 'rb'), as_attachment=True, content_type='application/pdf')
        messages.info(request, f'Created INV{newinv.invobj.pk} For {newinv.invobj.bus_reltn.bus_name} To {newinv.invobj.client_reltn.client_name} Succesfully!')
        return redirect('invoice-gen')
        '''End Test code'''
    '''Test Code'''
    '''End Test Code'''
    invoice = invoiceform()
    lineitems = lineitemformset()
    context = {'invoice': invoice,'lineitems':lineitems}
    return render(request, 'invoicegen.html', context)

def invoicesubmission(request, pk):
    pass