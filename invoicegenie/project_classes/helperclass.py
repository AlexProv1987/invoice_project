'''re usable class that holds static methods to parse a post request that can be called without constructing an instance of the class'''
class postreqhelpers():
    def __init__(self) -> None:
        pass
    @staticmethod
    def parsepost(postdict:dict, keys:tuple) -> dict:
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

'''unused'''
class datehelpers():
    pass

'''unused'''
class mathhelpers():
    pass

'''class containing static methods to be called to assist in validating data sent to the server'''
class postreqvalidator():
    def __init__(self) -> None:
        pass
    @staticmethod
    def checktype():
        pass
    @staticmethod
    def checkkeys():
        pass