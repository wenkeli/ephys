import re as regexp;
import os;
import struct;
import numpy as np;

def readEventFile(fileName):
    fsize=os.stat(fileName);
    fsize=fsize.st_size;
    fHeaderSize=1024;
    
    fh=open(fileName, "rb");
    
    header=fh.read(fHeaderSize);
    header=regexp.sub("header\.", "", header);
    exec(header);

    print("version: "+str(version));
    
    data=readEvents(fh, fHeaderSize, fsize, "=qh4BH", 0, 5);
    
    fh.close();
    return data;
        

def readEvents(fh, fsize, fHeaderSize, eventFStr, timeStampInd, chInd):
    
    eventSize=struct.calcsize(eventFStr);
    
    numEvents=(fsize-fHeaderSize)/eventSize;
    
    print(str(eventSize)+" "+str(fsize)+" "+str(numEvents));
    print(str((fsize-fHeaderSize)%eventSize)+"\n");
    
    
    retData=dict();
    
    retData["timestamps"]=np.zeros(numEvents, dtype="uint64");
    retData["eventChs"]=np.zeros(numEvents, dtype="int32");   
    fh.seek(fHeaderSize);
    
    for i in np.r_[0:numEvents]:
        event=struct.unpack(eventFStr, fh.read(eventSize));
        retData["timestamps"][i]=event[timeStampInd];
        retData["eventChs"][i]=event[chInd]; 

        if(i%100==0):
            print(str(i));

    return retData;
