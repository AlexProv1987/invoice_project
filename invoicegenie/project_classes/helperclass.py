class postreqhelpers():
    def __init__(self) -> None:
        pass   
    @classmethod
    def parsepost(self,postdict:dict, keys:tuple) -> dict:
        returnDict = {}
        #check type
        if not isinstance(postdict,dict):
            raise TypeError   
        #for each key in keys find value in postdict
        for key in keys:
            try:
                returnDict.update({key:postdict[key]})
            except KeyError:
                continue
        print(returnDict)
        return returnDict

class datehelpers():
    pass

class mathhelpers():
    pass
