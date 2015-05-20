import re as regexp;
import os;
import struct;
import numpy as np;

def readSpikeFile(fh, fileName):
    fsize=os.stat(fileName);
    fsize=fsize.st_size;
    fHeaderSize=1024;
    
    header=fh.read(fHeaderSize);
    header=regexp.sub("header\.", "", header);
    exec(header);
    
    if(version==0.4):
        print("loading version 0.4 file");
        data=readSamples(fh, fsize, fHeaderSize, "=B2q6H3B2f1H", "f", "H", "1H", "H", 4, 5, 8);
    elif(version==0.2):
        print("loading version 0.2 file");
        data=readSamples(fh, fsize, fHeaderSize, "=Bq3H", "H", "H", "1H", "H", 3, 4, None);
        
    data["samplingHz"]=sampleRate;
    
    return data;
        

def readSamples(fh, fsize, fHeaderSize, spikeHeadFStr, 
              spikeGainFStr, spikeThreshFStr, spikeTailFStr, 
              spikeDataFStr, nChInd, nSampleInd, triggerChInd):
    
    fh.seek(fHeaderSize);
    
    spikeHeaderSize=struct.calcsize(spikeHeadFStr);
    
    spikeInfo=struct.unpack(spikeHeadFStr, fh.read(struct.calcsize(spikeHeadFStr)));
    
    nChs=spikeInfo[nChInd];
    nSamples=spikeInfo[nSampleInd];
    
    totalSampleSize=nChs*nSamples;
    
    spikeDataSize=struct.calcsize(spikeDataFStr)*totalSampleSize;
    
    spikeGainSize=struct.calcsize(spikeGainFStr)*nChs;
    
    spikeThreshSize=struct.calcsize(spikeThreshFStr)*nChs;
    
    spikeTailSize=struct.calcsize(spikeTailFStr);
    
    spikeSize=spikeHeaderSize+spikeDataSize+spikeGainSize+spikeThreshSize+spikeTailSize;
    
    spikeFStr=spikeHeadFStr+str(totalSampleSize)+spikeDataFStr;
    spikeFStr=spikeFStr+str(nChs)+spikeGainFStr;
    spikeFStr=spikeFStr+str(nChs)+spikeThreshFStr+spikeTailFStr;
    
    spikeDataInd=len(spikeInfo);
    print(len(spikeInfo));
    spikeGainInd=spikeDataInd+totalSampleSize;
    spikeThreshInd=spikeGainInd+nChs;
    
    numSpikes=(fsize-fHeaderSize)/spikeSize;
    
    print(str(spikeSize)+" "+str(struct.calcsize(spikeFStr))+" "+str(numSpikes));
    print(str((fsize-fHeaderSize)%spikeSize)+"\n");
    
    
    retData=dict();
    
    retData["timestamps"]=np.zeros(numSpikes, dtype="uint64");
    retData["waveforms"]=np.zeros((numSpikes, totalSampleSize), dtype="float32");
    retData["gains"]=np.zeros((numSpikes, nChs), dtype="float32");
    retData["thresholds"]=np.zeros((numSpikes, nChs), dtype="float32");
    retData["triggerChs"]=None;
    if(triggerChInd is not None):
        retData["triggerChs"]=np.zeros(numSpikes, dtype="uint16");
    
    fh.seek(fHeaderSize);
    
    for i in np.r_[0:numSpikes]:
        spike=struct.unpack(spikeFStr, fh.read(spikeSize));
        retData["timestamps"][i]=spike[1];
#         print("spike start");
#         print(int(spike[0]));
#         print(spike[4]);
#         print(spike[5]);
#         print(spike[6]);
#         print(spike[7]);
#         print(spike[8]);
#         print(spike[9]);
#         print(spike[11]);
#         print(spike[12]);
#         print(spike[13]);
#         print(spike[14]);
#         print("\n");
#         print(spike[15]);
#         print(spike[15+40]);
#         print(spike[15+40*2]);
#         print(spike[15+40*3]);
#         print("\n");
#         print(spike[15+4*40]);
#         print(spike[15+4*40+1]);
#         print(spike[15+4*40+2]);
#         print(spike[15+4*40+3]);
#         print("\n");
#         print(spike[15+4*40+4]);
#         print(spike[15+4*40+5]);
#         print(spike[15+4*40+6]);
#         print(spike[15+4*40+7]);
#         print("\n");
#         print(spike[15+4*40+8]);
#         print("\n");
        if(triggerChInd is not None):
            retData["triggerChs"]=spike[triggerChInd];
        retData["waveforms"][i, :]=spike[spikeDataInd:spikeDataInd+totalSampleSize];
        retData["gains"][i, :]=spike[spikeGainInd:spikeGainInd+nChs];
        retData["thresholds"][i, :]=spike[spikeThreshInd:spikeThreshInd+nChs];    

        if(i%10000==0):
            print(str(i));
#             print(spike);
    
    retData["gains"]=retData["gains"]/1000.;
    retData["waveforms"]=(32768.-retData["waveforms"]);
    for i in np.r_[0:nChs]:
        wStart=i*nSamples;
        wEnd=wStart+nSamples;
        retData["waveforms"][:, wStart:wEnd]=retData["waveforms"][:, wStart:wEnd]/retData["gains"][:, i][np.newaxis].T;

    return retData;
