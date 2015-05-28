import numpy as np;

class Events(object):
    def __init__(self, timestamps, eventChs):
        self.__data=dict();
        
        chs=np.unique(eventChs);
        
        for i in chs:
            self.__data["ch"+str(i)]=timestamps[eventChs==i];
            
    def getChs(self):
        return self.__data.keys();
    
    def getChTimes(self, chInd):
        return self.__data[chInd];
    
        