import re;
import os;
import struct;
import numpy as np;

def readEventFile(fileName):
    hVarRE=re.compile("header\.(.+) = \'?(.+?)\'?;");
    
    fsize=os.stat(fileName);
    fsize=fsize.st_size;
    
    fh=open(fileName, "rb");
    readPos=0;
    header=dict();
    
    while(readPos<fsize):
        try:
            line=fh.readline().decode("utf-8");
            match=hVarRE.match(line);
        except:
            break;
        if(match is None):
            break;
        header[match.groups()[0]]=match.groups()[1];
        readPos=fh.tell();
    
    fHeaderSize=int(header["header_bytes"]);
    version=header["version"];
    sampleRate=float(header["sampleRate"]);

    print("version: "+str(version));
    print("sample rate: "+str(sampleRate));
    
    data=readEvents(fh, fsize, fHeaderSize, "=qh4BH", 0, 1, 5, 4, sampleRate);
    
    fh.close();
    return data;
        

def readEvents(fh, fsize, fHeaderSize, eventFStr, timeStampInd, posInd, chInd, eIDInd, sampleRate):
    
    eventSize=struct.calcsize(eventFStr);
    
    numEvents=(fsize-fHeaderSize)//eventSize;
    
    print(str(eventSize)+" "+str(fsize)+" "+str(numEvents));
    print(str((fsize-fHeaderSize)%eventSize)+"\n");
    
    
    retData=dict();
    
    retData["timestamps"]=np.zeros(numEvents, dtype="float64");
    retData["eventChs"]=np.zeros(numEvents, dtype="int32");
    retData["eventIDs"]=np.zeros(numEvents, dtype="uint8");
     
    fh.seek(fHeaderSize);
    
    for i in range(numEvents):
        event=struct.unpack(eventFStr, fh.read(eventSize));
        retData["timestamps"][i]=event[timeStampInd]/sampleRate;
        retData["eventChs"][i]=event[chInd];
        retData["eventIDs"][i]=event[eIDInd];
        
#         print(event);
#         print(str(retData["timestamps"][i]));
        

        if(i%100==0):
            print(str(i));

    return retData;
