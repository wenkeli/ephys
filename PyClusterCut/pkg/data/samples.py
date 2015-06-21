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
    def __init__(self, waveforms, thresholds, timestamps, samplingHz, triggerChs):
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
        
        self.__timestamps=np.zeros(timestamps.shape, dtype="float64");
        self.__timestamps[:]=timestamps;

        if(thresholds is not None):        
            self.__calcTriggerChannel(triggerChs, thresholds.T);
        else:
            self.__calcTriggerChannel(triggerChs, None);
            
        self.__calcParams();
        
    def __calcTriggerChannel(self, triggerCh, thresholds, triggerEndPoint=9):
        self.__triggerCh=np.zeros(self.__numSamples, dtype="int32");
        self.__triggerCh[:]=-10;
        
        if(triggerCh is not None):
            self.__triggerCh[:]=triggerCh;
            return;
        
        appendCol=np.zeros(self.__numSamples, dtype="bool")[np.newaxis].T;
        for i in np.r_[0:self.__numChs]:
            aboveThresh=self.__waveforms[i, :, 0:triggerEndPoint]>=(thresholds[i, :][np.newaxis].T);
            belowThresh=self.__waveforms[i, :, 0:triggerEndPoint-1]<(thresholds[i, :][np.newaxis].T);
            
            belowThresh=np.hstack((appendCol, belowThresh));
            
            isTrigger=np.sum((aboveThresh & belowThresh), 1)>0;
                                         
            self.__triggerCh[isTrigger]=i;
            
        validEvents=self.__triggerCh>=0;
        
        self.__numSamples=np.sum(validEvents);
        
        self.__waveforms=self.__waveforms[:, validEvents, :];
        self.__timestamps=self.__timestamps[validEvents];
        
        self.__triggerCh=self.__triggerCh[validEvents];
    
    
    def __calcParams(self):
        self.__params["timestamp"]=self.__timestamps;
        self.__paramType["timestamp"]=0; #0 is channel independent
        self.__calcPeak();
        self.__calcValley();
        self.__calcPVWidth();
        self.__calcPeakEnergy();
        self.__calcValleyEnergy();
        self.__calcPeakAngle();
        self.__calcTime();
        
    def __calcPeak(self, peakTime=8):
        peakLocalInds=np.argmax(self.__waveforms[:, :, (peakTime-1):(peakTime+2)], 2);
        peakLocalInds=peakLocalInds[self.__triggerCh, np.r_[0:self.__numSamples]];
        self.__params["peakTime"]=peakLocalInds+peakTime-1;
        self.__paramType["peakTime"]=0;

        self.__params["peak"]=self.__waveforms[:, np.r_[0:self.__numSamples], self.__params["peakTime"]];
#         self.__params["peak"]=self.__waveforms[:, :, peakTime];
        self.__paramType["peak"]=1;
        
        
    def __calcValley(self, valleyStartOffset=0, valleyLen=27):
        inds=np.mgrid[0:self.__numSamples, 0:valleyLen];
        sampleInd=inds[0];
        valleyInd=inds[1];
        startInd=self.__params["peakTime"]+valleyStartOffset;
        valleyInd=valleyInd+np.reshape(startInd, (self.__numSamples,1));
#         self.__params["valleyTime"]=np.argmin(self.__waveforms[:, :, valleyStart:valleyEnd], 2)+valleyStart;
        self.__params["valleyTime"]=np.argmin(self.__waveforms[:, sampleInd, valleyInd], 2)+startInd;
        sampleInd=np.r_[0:self.__numSamples];
        self.__params["valleyTime"]=self.__params["valleyTime"][self.__triggerCh, sampleInd];
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
    
    
    def getWaveforms(self, sBA, chN=None, triggerChOnly=False):
        if(chN==None):
            chN=np.r_[0:self.__numChs];
        
        xVals=[];
        connectArrs=[];
        waveforms=[];      
        for i in chN:
            select=sBA;
            if(triggerChOnly):
                select=select & (self.__triggerCh==i);
                
            numSel=np.sum(select);
            
            xVal=np.mgrid[0:numSel, 0:self.__numPtsPerCh][1];
            xVals.append(xVal);
            
            connectArr=np.zeros(xVal.shape, dtype="bool");
            connectArr[:]=True;
            connectArr[:, -1]=False;
            connectArrs.append(connectArr);
            
            waveforms.append(self.__waveforms[i, select, :]);    
                 
        return (self.__numPtsPerCh, waveforms, xVals, connectArrs);
        
    
    def getNumChannels(self):
        return self.__numChs;
    
    def getNumSamples(self):
        return self.__numSamples;

    