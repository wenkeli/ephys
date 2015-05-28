import numpy as np;

class Events(object):
    def __init__(self, timestamps, eventChs, eventIDs):
        self.__data=dict();
        
        chs=np.unique(eventChs);
        
        for i in chs:
            self.__data["ch"+str(i)+"_low"]=timestamps[(eventChs==i) & (eventIDs<=0)];
            self.__data["ch"+str(i)+"_high"]=timestamps[(eventChs==i) & (eventIDs>0)];
            
    def getChs(self):
        return self.__data.keys();
    
    def getChTimes(self, chInd):
        return self.__data[chInd];
    
        