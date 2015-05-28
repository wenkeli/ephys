import re as regexp;
import os;
import struct;
import numpy as np;
from numpy import float64

def readEventFile(fileName):
    fsize=os.stat(fileName);
    fsize=fsize.st_size;
    fHeaderSize=1024;
    
    fh=open(fileName, "rb");
    
    header=fh.read(fHeaderSize);
    header=regexp.sub("header\.", "", header);
    exec(header);

    print("version: "+str(version));
    print("sample rate: "+str(sampleRate));
    
    data=readEvents(fh, fsize, fHeaderSize, "=qh4BH", 0, 1, 5, 4, sampleRate);
    
    fh.close();
    return data;
        

def readEvents(fh, fsize, fHeaderSize, eventFStr, timeStampInd, posInd, chInd, eIDInd, sampleRate):
    
    eventSize=struct.calcsize(eventFStr);
    
    numEvents=(fsize-fHeaderSize)/eventSize;
    
    print(str(eventSize)+" "+str(fsize)+" "+str(numEvents));
    print(str((fsize-fHeaderSize)%eventSize)+"\n");
    
    
    retData=dict();
    
    retData["timestamps"]=np.zeros(numEvents, dtype="float64");
    retData["eventChs"]=np.zeros(numEvents, dtype="int32");
    retData["eventIDs"]=np.zeros(numEvents, dtype="uint8");
     
    fh.seek(fHeaderSize);
    
    for i in np.r_[0:numEvents]:
        event=struct.unpack(eventFStr, fh.read(eventSize));
        retData["timestamps"][i]=(event[timeStampInd]+event[posInd])/np.float64(sampleRate);
        retData["eventChs"][i]=event[chInd];
        retData["eventIDs"][i]=event[eIDInd];
        
        print(event);
        print(str(retData["timestamps"][i]));
        

        if(i%100==0):
            print(str(i));

    return retData;
