import numpy as np;
from scipy.signal import waveforms

class SamplesClustCount(object):
    def __init__(self, numSamples):
        self.__sampleNumClust=np.zeros(numSamples, dtype="int32");
        
    def addClustCount(self, sBA):
        self.__sampleNumClust[sBA]=self.__sampleNumClust[sBA]+1;
        
    def minusClustCount(self, sBA):
        self.__sampleNumClust[sBA]=self.__sampleNumClust[sBA]-1;
        self.__sampleNumClust[self.__sampleNumClust<0]=0;
        
    def getNoClustSamples(self):
        return self.getNClustSamples(0);
    
    def getNClustSamples(self, numClusts):
        return self.__sampleNumClust==numClusts;
    
    def getMinClustSamples(self, numClusts):
        return self.__sampleNumClust>=numClusts;

class SamplesData(object):
    def __init__(self, waveforms, timestamps, numChs, samplingHz):
        self.__waveforms=[];
        self.__timestamps=[];
        
        self.__thresholds=[];
        self.__gains=[];
        
        self.__refWaveCh=[];
        
        self.__params=dict();
        self.__paramType=dict();
        
        self.__numChs=0;
        self.__numPtsPerCh=0;
        self.__numSamples=0;
        
        self.__samplingHz=samplingHz;
        self.__samplingUSec=1000000.0/self.__samplingHz;
        
        
        self.__numSamples=waveforms.shape[0];
        self.__numChs=numChs;
        self.__numPtsPerCh=waveforms.shape[1]/self.__numChs;
        
        self.__waveforms=np.array(np.copy(waveforms), dtype="float32");
        self.__waveforms=self.__waveforms.reshape((self.__numSamples, self.__numChs, self.__numPtsPerCh));
        self.__waveforms=self.__waveforms.transpose(1, 0, 2);
        
        self.__timestamps=np.zeros(timestamps.shape, dtype="float64");
        self.__timestamps[:]=timestamps;

        self.__calcRefWaveCh();
        self.__calcParams();
        
        
    def __calcRefWaveCh(self, peakStart=7, peakEnd=10):
        wavesMax=np.max(self.__waveforms[:, :, peakStart:peakEnd], 2);
#         print(wavesMax.shape);
        self.__refWaveCh=np.argmax(wavesMax, 0);
#         print(self.__refWaveCh.shape);
        
        
    def __calcPeak(self, peakStart=7, peakEnd=10):
        sampleInds=np.r_[0:self.__numSamples];
        wavesMaxP=np.argmax(self.__waveforms[:, :, peakStart:peakEnd], 2)+peakStart;
        self.__params["peakTime"]=wavesMaxP[self.__refWaveCh, sampleInds];
        self.__paramType["peakTime"]=0;
        
        self.__params["peak"]=self.__waveforms[:, sampleInds, self.__params["peakTime"]];
        self.__paramType["peak"]=1;
    
    
    def __calcParams(self):
        self.__params["timestamp"]=self.__timestamps;
        self.__paramType["timestamp"]=0; #0 is channel independent
        self.__calcPeak();
        self.__calcValley();
        self.__calcPVWidth();
        self.__calcPeakEnergy();
        self.__calcValleyEnergy();
        self.__calcPeakAngle();
        self.calcPeakFallAngle();
        self.__calcTime();
        
#     def __calcPeak(self, peakTime=8):
#         peakLocalInds=np.argmax(self.__waveforms[:, :, (peakTime-1):(peakTime+2)], 2);
#         peakLocalInds=peakLocalInds[self.__refWaveCh, np.r_[0:self.__numSamples]];
#         self.__params["peakTime"]=peakLocalInds+peakTime-1;
#         self.__paramType["peakTime"]=0;
# 
#         self.__params["peak"]=self.__waveforms[:, np.r_[0:self.__numSamples], self.__params["peakTime"]];
# #         self.__params["peak"]=self.__waveforms[:, :, peakTime];
#         self.__paramType["peak"]=1;
        
        
    def __calcValley(self, valleyStartOffset=0, valleyLen=27):
        inds=np.mgrid[0:self.__numSamples, 0:valleyLen];
        sampleInd=inds[0];
        valleyInd=inds[1];
        startInd=self.__params["peakTime"]+valleyStartOffset;
        valleyInd=valleyInd+np.reshape(startInd, (self.__numSamples,1));
#         self.__params["valleyTime"]=np.argmin(self.__waveforms[:, :, valleyStart:valleyEnd], 2)+valleyStart;
        self.__params["valleyTime"]=np.argmin(self.__waveforms[:, sampleInd, valleyInd], 2)+startInd;
        sampleInd=np.r_[0:self.__numSamples];
        self.__params["valleyTime"]=self.__params["valleyTime"][self.__refWaveCh, sampleInd];
        self.__params["valleyTime"]=np.uint32(self.__params["valleyTime"]);
        self.__paramType["valleyTime"]=0;
        
        self.__params["valley"]=self.__waveforms[:, sampleInd, self.__params["valleyTime"]];
        self.__paramType["valley"]=1;
    
    def __calcPVWidth(self):
        self.__params["PVWidth"]=(self.__params["valleyTime"]-self.__params["peakTime"])*self.__samplingUSec;
        self.__paramType["PVWidth"]=0;
        
    def __calcPeakEnergy(self):
        self.__params["peakEnergy"]=np.copy(self.__waveforms);
        self.__params["peakEnergy"][self.__params["peakEnergy"]<0]=0;
        self.__params["peakEnergy"]=np.sum(self.__params["peakEnergy"], 2);
        self.__paramType["peakEnergy"]=1;
        
    def __calcValleyEnergy(self):
        self.__params["valleyEnergy"]=np.copy(self.__waveforms);
        self.__params["valleyEnergy"][self.__params["valleyEnergy"]>0]=0;
        self.__params["valleyEnergy"]=np.abs(np.sum(self.__params["valleyEnergy"], 2));
        self.__paramType["valleyEnergy"]=1;
        
    def __calcPeakAngle(self, startOffset=-1, stepSize=3):
        sampleInd=np.r_[0:self.__numSamples];

        self.__params["peakAngle"]=(self.__waveforms[:, sampleInd, self.__params["peakTime"]+startOffset]-
                                  self.__waveforms[:, sampleInd, self.__params["peakTime"]+startOffset-stepSize]);
        self.__params["peakAngle"]=self.__params["peakAngle"]/(self.__samplingUSec*stepSize);
        self.__params["peakAngle"]=np.arctan(self.__params["peakAngle"])/(2*np.pi)*360;                       
        self.__paramType["peakAngle"]=1;
        
    def calcPeakFallAngle(self, startOffset=1, stepSize=3):
        sampleInd=np.r_[0:self.__numSamples];
        self.__params["peakFallAngle"]=(self.__waveforms[:, sampleInd, self.__params["peakTime"]+startOffset+stepSize]-
                                       self.__waveforms[:, sampleInd, self.__params["peakTime"]+startOffset]);
        self.__params["peakFallAngle"]=self.__params["peakFallAngle"]/(self.__samplingUSec*stepSize);
        self.__params["peakFallAngle"]=np.arctan(self.__params["peakFallAngle"])/(2*np.pi)*360;
        self.__paramType["peakFallAngle"]=1;
        
    def __calcTime(self):
        self.__params["time"]=np.float64(self.__timestamps)/self.__samplingHz;
        self.__paramType["time"]=0;

        
    def getParamNames(self):
        return self.__params.keys();
    
    def getParam(self, chN, paramName):
        if(self.__paramType[paramName]==0):
            return self.__params[paramName];
        else:
            return self.__params[paramName][chN, :];
        
#     def getParamRange(self, chN, paramName):
#         if(self.__paramType[paramName]==0):
#     
        
    def getParamAllChs(self, paramName):
        return self.__params[paramName];
    
    
    def getWaveforms(self, sBA, chN=None, refWaveChOnly=False):
        if(chN==None):
            chN=np.r_[0:self.__numChs];
        
        xVals=[None]*self.__numChs;
        connectArrs=[None]*self.__numChs;
        waveforms=[None]*self.__numChs;      
        for i in chN:
            select=sBA;
            try:
                if(refWaveChOnly):
                    select=select & (self.__refWaveCh==i);
            except AttributeError:
                self.__calcRefWaveCh();
                select=select & (self.__refWaveCh==i);
            else:                
                numSel=np.sum(select);
                
                xVal=np.mgrid[0:numSel, 0:self.__numPtsPerCh][1];
                xVals[i]=xVal;
                
                connectArr=np.zeros(xVal.shape, dtype="bool");
                connectArr[:]=True;
                connectArr[:, -1]=False;
                connectArrs[i]=connectArr;
                
                waveforms[i]=self.__waveforms[i, select, :];    
                 
        return (self.__numPtsPerCh, waveforms, xVals, connectArrs);
        
    
    def getNumChannels(self):
        return self.__numChs;
    
    def getNumSamples(self):
        return self.__numSamples;

    