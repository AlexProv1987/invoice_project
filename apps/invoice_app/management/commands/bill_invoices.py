import datetime
from apps.invoice_app.models import invoice
from django.core.management.base import BaseCommand
from django.core import mail
from apps.invoice_app.models import lineitem,invoice
import os,tempfile
from apps.invoice_app.controllers.invoicegenerator import generatepdf
from smtplib import SMTPException
'''
Currently we are assuming we wont have a massive query causing issues with the queryset cache.
Using iterator() is something to look at if we run into this. This will fetch only a few rows at a time, but will cause more calls to the DB 
We need to capture any emails that fail to send 

We need more robust email validation deliverability is important here : https://www.abstractapi.com/api/email-verification-validation-api
'''
class Command(BaseCommand):

    def handle(self,*args,**kwargs):
        rtb_invoices = self._get_rtb_invoices()
        self._send_emails(rtb_invoices)

    def _get_rtb_invoices(self):
        ready_to_bill = invoice.objects.filter(inv_status=invoice.ReadyToBill)
        return ready_to_bill
    
    def _get_line_items(self,inv_pk):
        line_items = lineitem.objects.filter(inv_reltn=inv_pk)
        return line_items

    def _send_emails(self, rtb_inv):
        sucess_invoice = []
        failed_invoice = []
        for_cnt = 0
        company_mail = ''
        for inv in rtb_inv:
            if for_cnt == 0:
                company_mail = inv.bus_reltn.bus_email
                for_cnt+=1
            email = mail.EmailMessage (
            f'Invoice From {inv.bus_reltn.bus_name}', 
            f'Hello, {inv.client_reltn.client_name}. You have an invoice with a balance due of: {inv.total_billed}. Please See Attachment.',
            inv.bus_reltn.bus_email,
            [inv.client_reltn.client_email],
            )
            invli=self._get_line_items(inv.pk)
            #generate PDF object
            pdf = generatepdf(invli,inv)
            #get temp file
            temp_pdf = self._get_temp_file(pdf.pdf, f'{inv.pk}', '.pdf')
            #attach file
            email.attach_file(temp_pdf.name)
            #attemp to send email - fail_silently is false by default, setting is for clarity.
            try:
                email.send(fail_silently=False)
                #add to success dict to be updated
                sucess_invoice.append(inv)
            #we are going to have issues here on invalid email since this simply just sends and queues it up as long as the address is formatted correct, looking at abstract api
            except SMTPException:
                #django uses smtp for mailing we need to make this more robust so its not just generic exception
                failed_invoice.append(f'{inv.pk} Failed To Send Message - Base SMTPException')
            #cleanup/remove file
            self._destry_temp_file(temp_pdf)
        #update success invoice
        self._update_invoice_status(sucess_invoice)
        #email log admin, if no errors, send success email
        self._send_log(failed_invoice, company_mail, len(sucess_invoice))
        return

    def _get_temp_file(self, object, prefix, suffix):
        #create temp file
        temp_file = tempfile.NamedTemporaryFile(delete=False, prefix=prefix, suffix=suffix)
        #output (save) the pdf object to the temp file
        object.output(temp_file)
        #reset file pos to start
        temp_file.seek(0)
        return temp_file

    #destroy file in file system
    def _destry_temp_file(self,fname):
        fname.close()
        os.unlink(fname.name)

    #update all succesfull invoices
    def _update_invoice_status(self, obj_list):
        for obj in obj_list:
            obj.inv_status = invoice.Billed
            obj.inv_billed_date = datetime.date.today()
        invoice.objects.bulk_update(obj_list, fields=['inv_status', 'inv_billed_date'], batch_size=200)
    
    #send a log very archaic atm
    def _send_log(self, error_log, company_email, success_count):
        email = mail.EmailMessage (
            f'Email Log for Invoice Billing Job on {datetime.date.today()}', 
            f'Success Count: {success_count} \n Failed Count: {len(error_log)} \n Failure Messages: {error_log}',
            company_email,
            [company_email],
            )
        email.send()