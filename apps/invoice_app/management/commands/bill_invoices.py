from apps.invoice_app.models import invoice, invoicefile
from django.core.management.base import BaseCommand
from django.core import mail
'''
Currently we are assuming we wont have a massive query causing issues with the queryset cache.
Using iterator() is something to look at if we run into this. This will fetch only a view rows at a time, but will cause more calls to the DB 
'''
class Command(BaseCommand):
    def handle(self,*args,**kwargs):
        rtb_invoices = self._getinvoices()
        rtb_pdfs = self._getinvpdfs(rtb_invoices)
        message_list = self._createemails(rtb_invoices,rtb_pdfs)
        self._massmail(message_list)

    def _getinvoices(self):
        ready_to_bill = invoice.objects.filter(inv_status=invoice.ReadyToBill)
        return ready_to_bill

    def _getinvpdfs(self, ready_to_bill_inv):
        rtb_invoice_files = invoicefile.objects.filter(inv_reltn__in=ready_to_bill_inv)
        return rtb_invoice_files

    def _createemails(self, rtb_inv, rtb_file):
        mail_list = []
        for inv in rtb_inv:
            for inv_file in rtb_file:
                if inv_file.inv_reltn.pk == inv.pk:
                    pdf = inv_file.file_loc
                    break
            email = mail.EmailMessage (
            f'Invoice From {inv.bus_reltn.bus_name}', 
            f'Hello, {inv.client_reltn.client_name}. You have an invoice with a balance due of: {inv.total_billed}. Please See Attachment.',
            inv.bus_reltn.bus_email,
            [inv.client_reltn.client_email],
            )
            email.attach_file(pdf)
            mail_list.append(email)
        return mail_list

    def _massmail(self, messages):
        connection = mail.get_connection()
        connection.send_messages(messages)
        connection.close()
