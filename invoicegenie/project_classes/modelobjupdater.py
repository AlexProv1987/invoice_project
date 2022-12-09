'''class accepts a db model object, and a dictionary of field(key),updatevalue(value) pairs
'''

class updatemodelobj():
    def __init__(self, modelobj, **kwargs) -> None:
        self.obj = modelobj
        self.keyval = kwargs

    def _updateobj(self):
        pass