import numpy as np;

class SamplesClustCount(object):
    def __init__(self, numSamples):
        self.sampleNumClust=np.zeros(numSamples, dtype="int32");
        
    def addClustCount(self, sBA):
        self.sampleNumClust[sBA]=self.sampleNumClust[sBA]+1;
        
    def minusClustCount(self, sBA):
        self.sampleNumClust[sBA]=self.sampleNumClust[sBA]-1;
        self.sampleNumClust[self.sampleNumClust<0]=0;
        
    def getNoClustSamples(self):
        return self.getNClustSamples(0);
    
    def getNClustSamples(self, numClusts):
        return self.sampleNumClust==numClusts;

class SamplesData(object):
    def __init__(self, waveforms, gains, thresholds, timestamps, triggerChs=None):
        self.waveforms=[];
        self.timestamps=[];
        
        self.thresholds=[];
        self.gains=[];
        
        self.triggerCh=[];
        
        self.params=dict();
        self.numChs=0;
        self.numPtsPerCh=0;
        self.numSamples=0;
        
        
        self.numSamples=waveforms.shape[0];
        self.numChs=thresholds.shape[1];
        self.numPtsPerCh=waveforms.shape[1]/self.numChs;
        
        self.waveforms=np.array(np.copy(waveforms), dtype="float32");
        self.waveforms=self.waveforms.reshape((self.numSamples, self.numChs, self.numPtsPerCh));
        self.waveforms=self.waveforms.transpose(1, 0, 2);
        
        self.timestamps=np.zeros(timestamps.shape, dtype="uint64");
        self.timestamps[:]=timestamps;
        
        self.thresholds=np.zeros(thresholds.T.shape, dtype="float32");
        self.thresholds[:]=thresholds.T;
        
        self.gains=np.zeros(gains.T.shape, dtype="float32");
        self.gains[:]=gains.T;
        
        self.calcTriggerChannel(triggerChs);
        self.calcParams();
        
    def calcTriggerChannel(self, triggerCh, triggerEndPoint=9):
        self.triggerCh=np.zeros(self.numSamples, dtype="int32");
        self.triggerCh[:]=-1;
        
        if(triggerCh!=None):
            self.triggerCh[:]=triggerCh;
            return;
        
        appendCol=np.zeros(self.numSamples, dtype="bool")[np.newaxis].T;
        for i in np.r_[0:self.numChs]:
            aboveThresh=self.waveforms[i, :, 0:triggerEndPoint]>=(self.thresholds[i, :][np.newaxis].T);
            belowThresh=self.waveforms[i, :, 0:triggerEndPoint-1]<(self.thresholds[i, :][np.newaxis].T);
            
            belowThresh=np.hstack((appendCol, belowThresh));
            
            isTrigger=np.sum((aboveThresh & belowThresh), 1)>0;
                                         
            self.triggerCh[isTrigger]=i;
            
        validEvents=self.triggerCh>=0;
        
        self.numSamples=np.sum(validEvents);
        
        self.waveforms=self.waveforms[:, validEvents, :];
        self.timestamps=self.timestamps[validEvents];
        self.thresholds=self.thresholds[:, validEvents];
        self.gains=self.gains[:, validEvents];
        
        self.triggerCh=self.triggerCh[validEvents];
    
    
    def calcParams(self):
        self.calcPeak();
        self.calcValley();
        self.calcPVWidth();
        self.calcPeakEnergy();
        self.calcValleyEnergy();
        self.calcPeakAngle();
        
    def calcPeak(self, peakTime=8):
        self.params["peak"]=self.waveforms[:, :, peakTime];
        self.params["peakTime"]=np.zeros((self.numChs, self.numSamples), dtype="uint32");
        self.params["peakTime"][:]=peakTime;
        
    def calcValley(self, valleyStart=10, valleyEnd=30):
        self.params["valley"]=np.min(self.waveforms[:, :, valleyStart:valleyEnd], 2);
        self.params["valleyTime"]=np.argmin(self.waveforms[:, :, valleyStart:valleyEnd], 2)+valleyStart;
        
        valleyTime=self.params["valleyTime"][self.triggerCh, np.r_[0:self.numSamples]];
        for i in np.r_[0:self.numChs]:
            self.params["valleyTime"][i, :]=valleyTime;
        self.params["valleyTime"]=np.uint32(self.params["valleyTime"]);
    
    def calcPVWidth(self):
        self.params["PVWidth"]=self.params["valleyTime"]-self.params["peakTime"];
        
    def calcPeakEnergy(self):
        self.params["peakEnergy"]=np.copy(self.waveforms);
        self.params["peakEnergy"][self.params["peakEnergy"]<0]=0;
        self.params["peakEnergy"]=np.sum(self.params["peakEnergy"], 2);
        
    def calcValleyEnergy(self):
        self.params["valleyEnergy"]=np.copy(self.waveforms);
        self.params["valleyEnergy"][self.params["valleyEnergy"]>0]=0;
        self.params["valleyEnergy"]=np.abs(np.sum(self.params["valleyEnergy"], 2));
        
    def calcPeakAngle(self, stepSize=2):
        self.params["peakAngle"]=np.zeros((self.numChs, self.numSamples), dtype="float32");
        
        chIndRow=np.zeros(self.numSamples, dtype="int32");
        sampleIndRow=np.r_[0:self.numSamples];
        
        for i in np.r_[0:self.numChs]:
            chIndRow[:]=i;
            peakTimeRow=self.params["peakTime"][i, :];
            self.params["peakAngle"][i, :]=(self.waveforms[chIndRow, sampleIndRow, peakTimeRow]-
                                            self.waveforms[chIndRow, sampleIndRow, peakTimeRow-stepSize]);
        
    def getChParamTypes(self):
        return self.params.keys();
    
    def getChParam(self, chN, paramType):
        return self.params[paramType][chN, :];
    
    def getWaveforms(self, chN=None):
        if(chN==None):
            return self.waveforms;
        return self.waveforms[chN, :, :];
    
    def getNumChannels(self):
        return self.numChs;
    
    def getNumSamples(self):
        return self.numSamples;
        
    def getSampleTimes(self):
        return self.timestamps;

    