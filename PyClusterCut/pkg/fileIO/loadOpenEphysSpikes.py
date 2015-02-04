import struct;
import numpy as np;

def readSpikes(fh, fsize, fHeaderSize, spikeHeadFStr, 
              spikeGainFStr, spikeThreshFStr, spikeConstTailSize, 
              spikeDataFStr, nChInd, nSampleInd):
    header=fh.read(fHeaderSize);
    
    spikeHeaderSize=struct.calcsize(spikeHeadFStr);
    
    spikeInfo=struct.unpack(spikeHeadFStr, fh.read(struct.calcsize(spikeHeadFStr)));
    
    nChs=spikeInfo[nChInd];
    nSamples=spikeInfo[nSampleInd];
    
    totalSampleSize=nChs*nSamples;
    
    spikeDataSize=struct.calcsize(spikeDataFStr)*totalSampleSize;
    
    spikeGainSize=struct.calcsize(spikeGainFStr)*nChs;
    
    spikeThreshSize=struct.calcsize(spikeThreshFStr)*nChs;
    
    spikeTailSize=spikeConstTailSize;
    
    spikeSize=spikeHeaderSize+spikeDataSize+spikeGainSize+spikeThreshSize+spikeTailSize;
    
    spikeFStr=spikeHeadFStr+str(totalSampleSize)+spikeDataFStr;
    spikeFStr=spikeFStr+str(nChs)+spikeGainFStr;
    spikeFStr=spikeFStr+str(nChs)+spikeThreshFStr+str(spikeTailSize)+"x";
    
    spikeDataInd=len(spikeInfo);
    spikeGainInd=spikeDataInd+totalSampleSize;
    spikeThreshInd=spikeGainInd+nChs;
    
    numSpikes=(fsize-fHeaderSize)/spikeSize;
    
    print(str(spikeSize)+" "+str(struct.calcsize(spikeFStr))+" "+str(numSpikes));
    print(str((fsize-fHeaderSize)%spikeSize)+"\n");
    
    
    retData=dict();
    
    retData["timeStamp"]=np.zeros(numSpikes, dtype="uint64");
    retData["waveForms"]=np.zeros(numSpikes, totalSampleSize, dtype="float32");
    retData["gains"]=np.zeros(numSpikes, nChs, dtype="float32");
    retData["thresholds"]=np.zeros(numSpikes, nChs, dtype="float32");
    
    fh.seek(fHeaderSize);
    
    for i in np.r_[0:numSpikes]:
        spike=struct.unpack(spikeFStr, fh.read(spikeSize));
        retData["timeStamp"][i]=spike[1];
        retData["waveForms"][i, :]=spike[spikeDataInd, spikeDataInd+totalSampleSize];
        retData["gains"][i, :]=spike[spikeGainInd:spikeGainInd+nChs];
        retData["thresholds"][i, :]=spike[spikeThreshInd:spikeThreshInd+nChs];    

        if(i%10000==0):
            print(str(i));
#             print(spike);
    
    retData["gains"]=retData["gains"]/1000.;
    retData["waveForm"]=(32768.-retData["waveForm"]);
    for i in np.r_[0:nChs]:
        wStart=i*nSamples;
        wEnd=wStart+nSamples;
        retData["waveForms"][:, wStart, wEnd]=retData["waveForm"][:, wStart, wEnd]/retData["gains"][:, i];

    return retData;