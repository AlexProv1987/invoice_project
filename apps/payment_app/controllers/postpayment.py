import datetime
from apps.invoice_app.models import invoice
from apps.payment_app.models import payment
from djmoney.money import Money
#i dont like any of this, come back tomorrow when we dont have the sleepies
class postpayment():
    def __init__(self, request) -> None:
        self.req = request
        self.invobj = self._getinvobj()
        self.return_message = ''

    def _getinvobj(self) -> invoice:
        try:
            obj = invoice.objects.get(pk=self.req['invoice_reltn'])
            return obj
        except:
            return None

    def _checkbalance(self) -> bool:
        if self.invobj is not None:
            if self.invobj.curr_amt_due > Money(0.00, 'USD'):
                return True
            else:
                self.return_message = f'INV{self.invobj.pk} Balance is already 0.00'
                return False
        else:
            self.return_message=f"{self.req['invoice_reltn']} Does Not Exist"
            return False

    def _postpayment(self) ->bool:
        if self._checkbalance():
            newbal = self._getnewbalance(self.invobj.curr_amt_due,Money(self.req['payment_amt_0'],'USD'))
            print(newbal)
            if newbal < Money(0.00, 'USD'):
                self.return_message="Cannot apply a payment in excess of total balance"
                return False
            else:
                try:
                    print('hello')
                    self.invobj.curr_amt_due = newbal
                    if newbal == Money('0.00', 'USD'):
                        self.invobj.inv_status = invoice.Paid
                        self.invobj.inv_paid_date = datetime.date.today()
                    self.invobj.save()
                    return True
                except:
                    #we need to have passed in the payment id on the payment table to delete it in this case
                    self.return_message=f"Failed to apply {Money(self.req['payment_amt_0'],'USD')} to INV{self.invobj.pk}"
                    return False
        return False
            

    def _getnewbalance(self, curr_amt, pmt) -> Money:
        newamt = curr_amt - pmt
        return newamt

'''
Get Type of payment request -> 

Debit 
    Check the balance is > 0
    calculate new balance 
    if our new balance is < 0 fail as we cannot go negative
    else
    update object 
Credit (Adjustment):



'''