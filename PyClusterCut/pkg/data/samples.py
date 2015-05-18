import numpy as np;

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
    def __init__(self, waveforms, gains, thresholds, timestamps, samplingHz=30000, triggerChs=None):
        self.__waveforms=[];
        self.__timestamps=[];
        
        self.__thresholds=[];
        self.__gains=[];
        
        self.__triggerCh=[];
        
        self.__params=dict();
        self.__paramType=dict();
        
        self.__numChs=0;
        self.__numPtsPerCh=0;
        self.__numSamples=0;
        
        self.__samplingHz=samplingHz;
        self.__samplingUSec=1000000.0/self.__samplingHz;
        
        
        self.__numSamples=waveforms.shape[0];
        self.__numChs=thresholds.shape[1];
        self.__numPtsPerCh=waveforms.shape[1]/self.__numChs;
        
        self.__waveforms=np.array(np.copy(waveforms), dtype="float32");
        self.__waveforms=self.__waveforms.reshape((self.__numSamples, self.__numChs, self.__numPtsPerCh));
        self.__waveforms=self.__waveforms.transpose(1, 0, 2);
        
        self.__timestamps=np.zeros(timestamps.shape, dtype="uint64");
        self.__timestamps[:]=timestamps;
        self.__params["time"]=self.__timestamps;
        self.__paramType["time"]=0; #0 is channel independent
        
        self.__thresholds=np.zeros(thresholds.T.shape, dtype="float32");
        self.__thresholds[:]=thresholds.T;
        
        self.__gains=np.zeros(gains.T.shape, dtype="float32");
        self.__gains[:]=gains.T;
        
        self.__calcTriggerChannel(triggerChs);
        self.__calcParams();
        
    def __calcTriggerChannel(self, triggerCh, triggerEndPoint=9):
        self.__triggerCh=np.zeros(self.__numSamples, dtype="int32");
        self.__triggerCh[:]=-1;
        
        if(triggerCh is not None):
            self.__triggerCh[:]=triggerCh;
            return;
        
        appendCol=np.zeros(self.__numSamples, dtype="bool")[np.newaxis].T;
        for i in np.r_[0:self.__numChs]:
            aboveThresh=self.__waveforms[i, :, 0:triggerEndPoint]>=(self.__thresholds[i, :][np.newaxis].T);
            belowThresh=self.__waveforms[i, :, 0:triggerEndPoint-1]<(self.__thresholds[i, :][np.newaxis].T);
            
            belowThresh=np.hstack((appendCol, belowThresh));
            
            isTrigger=np.sum((aboveThresh & belowThresh), 1)>0;
                                         
            self.__triggerCh[isTrigger]=i;
            
        validEvents=self.__triggerCh>=0;
        
        self.__numSamples=np.sum(validEvents);
        
        self.__waveforms=self.__waveforms[:, validEvents, :];
        self.__timestamps=self.__timestamps[validEvents];
        self.__thresholds=self.__thresholds[:, validEvents];
        self.__gains=self.__gains[:, validEvents];
        
        self.__triggerCh=self.__triggerCh[validEvents];
    
    
    def __calcParams(self):
        self.__calcPeak();
        self.__calcValley();
        self.__calcPVWidth();
        self.__calcPeakEnergy();
        self.__calcValleyEnergy();
        self.__calcPeakAngle();
        
    def __calcPeak(self, peakTime=8):
        self.__params["peak"]=self.__waveforms[:, :, peakTime];
        self.__paramType["peak"]=1;
        
        self.__params["peakTime"]=np.zeros(self.__numSamples, dtype="uint32");
        self.__params["peakTime"][:]=peakTime;
        self.__paramType["peakTime"]=0;
        
    def __calcValley(self, valleyStart=10, valleyEnd=30):
#         self.__params["valley"]=np.min(self.__waveforms[:, :, valleyStart:valleyEnd], 2);
        self.__params["valleyTime"]=np.argmin(self.__waveforms[:, :, valleyStart:valleyEnd], 2)+valleyStart;
        self.__params["valleyTime"]=self.__params["valleyTime"][self.__triggerCh, np.r_[0:self.__numSamples]];
        self.__params["valleyTime"]=np.uint32(self.__params["valleyTime"]);
        self.__paramType["valleyTime"]=0;
        
        self.__params["valley"]=self.__waveforms[:, np.r_[0:self.__numSamples], self.__params["valleyTime"]];
        self.__paramType["valley"]=1;
    
    def __calcPVWidth(self):
        self.__params["PVWidth"]=self.__params["valleyTime"]-self.__params["peakTime"];
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
        
    def __calcPeakAngle(self, stepSize=2):
        sampleInd=np.r_[0:self.__numSamples];

        self.__params["peakAngle"]=(self.__waveforms[:, sampleInd, self.__params["peakTime"]]-
                                  self.__waveforms[:, sampleInd, self.__params["peakTime"]-stepSize]);
        self.__params["peakAngle"]=self.__params["peakAngle"]/(self.__samplingUSec*stepSize);
        self.__params["peakAngle"]=np.arctan(self.__params["peakAngle"])/(2*np.pi)*360;                       
        self.__paramType["peakAngle"]=1;

        
    def getParamNames(self):
        return self.__params.keys();
    
    def getParam(self, chN, paramName):
        if(self.__paramType[paramName]==0):
            return self.__params[paramName];
        else:
            return self.__params[paramName][chN, :];
    
    def getWaveforms(self, sBA, chN=None):
        numSel=np.sum(sBA);
        xVals=np.mgrid[0:numSel, 0:self.__numPtsPerCh][1];
        connectArr=np.zeros(xVals.shape, dtype="bool");
        connectArr[:]=True;
        connectArr[:, self.__numPtsPerCh-1]=False;
        if(chN is None):
            return (self.__numPtsPerCh, self.__waveforms[:, sBA, :], xVals, connectArr);
        return (self.__numPtsPerCh, self.__waveforms[chN, sBA, :], xVals, connectArr);
    
    def getNumChannels(self):
        return self.__numChs;
    
    def getNumSamples(self):
        return self.__numSamples;
        
    def getSampleTimes(self):
        return self.__timestamps;

    