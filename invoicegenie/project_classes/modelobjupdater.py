'''class accepts a db model object, and a dictionary of field(key),updatevalue(value) pairs
This is extremely redudant as the base model object class comes with everything this is doing.

from apps.invoice_app.models import invoice,invoicefile,lineitem
from apps.business_app.models import business, client
from apps.product_app.models import product
from django.core.exceptions import ObjectDoesNotExist

class modifymodelobj():
    def __init__(self, modelobj, objinstance, **kwargs) -> None:
        self.obj = modelobj
        self.obj_instance = objinstance
        self.key_val = kwargs

    def updatesingleobj(self):
        self.obj.objects.update(pk=self.obj_instance.pk).update(self.key_val)

    subclass and override this method if you want a specific logic.
    def updatemultobj(self):
        pass


    Declaring this as a static method to be re used elsewhere and makes the most sense in this class
    @staticmethod
    def objexists(model, instance) -> bool:
        try:
            model.objects.get(pk=instance.pk)
            return True
        except ObjectDoesNotExist:
            return False

'''