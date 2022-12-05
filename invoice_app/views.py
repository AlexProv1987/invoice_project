from django.shortcuts import render,redirect
from .modelforms import invoiceform, lineitemformset
from .controllers.invoicegenerator import handleinvoicegen, generatepdf
from fpdf import FPDF
from django.http import FileResponse
# Create your views here.

#view method will be split later, just sticking to one for testing
def invoicegen(request):
    if request.method == 'POST':
        newinv = handleinvoicegen(request.POST)
        invpdf = generatepdf(newinv.lineitemobj,newinv.invobj)
        '''Test Code'''
        return FileResponse(open(invpdf.pdffile, 'rb'), as_attachment=True, content_type='application/pdf')
        '''End Test code'''
    invoice = invoiceform()
    lineitems = lineitemformset()
    context = {'invoice': invoice,'lineitems':lineitems}
    return render(request, 'invoicegen.html', context)