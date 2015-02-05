import numpy as np

# class ChannelData:
#     self.waveforms=[];
#     self.gains=[];
#     self.params=dict();
#     
#     def __init(self, waveforms, gains):
#         self.waveforms=np.zeros(waveforms.shape, dtype="float32");
#         self.waveforms[:]=waveforms;
#         
#         self.gains=np.zeros(gains.shape, dtype="float32");
#         self.gains[:]=gains;
#         
#         calcParams();
#  
#         
#     def calcParams(self):
#         calcPeak();
#         calcPeakTime();
#         calcValley();
#         calcValleyTime();
#         calcPVWidth();
#         
#         calcPeakEnergy();
#         calcValleyEnergy();
#         
#         calcPeakAngle();
#         
#     def calcPeak(self, peakStart=7, peakEnd=10):
#         self.params["peak"]=np.max(self.waveforms[:, peakStart:peakEnd], 1);
#     
#     def calcPeakTime(self, peakStart=7, peakEnd=10):
#         self.params["peakTime"]=np.argmax(self.waveforms[:, peakStart:peakEnd], 1)+peakStart;
#     
#     def calcValley(self, valleyStart=10, valleyEnd=30):
#         self.params["valley"]=np.min(self.waveforms[:, valleyStart:valleyEnd], 1);
#         
#     def calcValley(self, valleyStart=10, valleyEnd=30):
#         self.params["valleyTime"]=np.argmin(self.waveforms[:, valleyStart:valley], 1)+valleyStart;
#         
#     def calcPVWidth(self):
#         self.params["PVWidth"]=self.params["valleyTime"]-self.params["peakTime"];
#         
#     def calcPeakEnergy(self):
#         self.params["peakEnergy"]=0;
#         
#     def calcValleyEnergy(self): 
#         return;
#     
#     def getParamTypes(self):
#         return self.params.keys();
#     
#     def getParam(self, paramType):
#         return self.params[paramType];

class SpikesData:    
    def __init__(self, waveforms, gains, thresholds, timestamps, triggerChs=None):
        self.waveforms=[];
        self.timestamps=[];
        
        self.thresholds=[];
        self.gains=[];
        
        self.triggerCh=[];
        
        self.params=dict();
        self.numChs=0;
        self.numPtsPerCh=0;
        self.numSpikes=0;
        
        
        self.numSpikes=waveforms.shape[0];
        self.numChs=thresholds.shape[1];
        self.numPtsPerCh=waveforms.shape[1]/self.numChs;
        
        self.waveforms=np.array(np.copy(waveforms), dtype="float32");
        self.waveforms=self.waveforms.reshape((self.numSpikes, self.numChs, self.numPtsPerCh));
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
        self.triggerCh=np.zeros(self.numSpikes, dtype="int32");
        self.triggerCh[:]=-1;
        
        if(triggerCh!=None):
            self.triggerCh[:]=triggerCh;
            return;
        
        appendCol=np.zeros(self.numSpikes, dtype="bool")[np.newaxis].T;
        for i in np.r_[0:self.numChs]:
            aboveThresh=self.waveforms[i, :, 0:triggerEndPoint]>=(self.thresholds[i, :][np.newaxis].T);
            belowThresh=self.waveforms[i, :, 0:triggerEndPoint-1]<(self.thresholds[i, :][np.newaxis].T);
            
            belowThresh=np.hstack((appendCol, belowThresh));
            
            isTrigger=np.sum((aboveThresh & belowThresh), 1)>0;
                                         
            self.triggerCh[isTrigger]=i;
    
    
    def calcParams(self):
        return;
            
    def getChParamsTypes(self):
        return self.params.keys();
    
    def getChParam(self, chN, paramType):
        return self.params[paramType][chN, :];
    
    def getNumChannels(self):
        self.numChs;
        
    def getSpikeTimes(self):
        return self.timestamps;
    


# class SpikesData:
#     self.chs=[];
#     self.timestamps=[];
#     self.numChs=0;
#     self.numPtsPerCh=0;
#     
#     def __init__(self, nChannels, nPointsPerChannel, waveforms, gains, timestamps):
#         self.chs=[None]*nChannels;
#         
#         for i in np.r_[0:nChannels]:
#             waveStart=nPointsPerChannel*i;
#             waveEnd=waveStart+nPointsPerChannel;
#             
#             self.chs[i]=ChannelData(waveforms[:, waveStart, waveEnd], gains[:, i]);
#             
#             self.timestamps=timestamps;
#             
#             self.numChs=nChannels;
#             self.numPtsPerCh=nPointsPerChannel;
#         
#             
#     def getChParamsTypes(self, chN):
#         return self.chs[chN].getParamTypes();
#     
#     def getChParam(self, chN, paramType):
#         return self.chs[chN].getParam();
#     
#     def getNumChannels(self):
#         self.numChs;
#         
#     def getSpikeTimes(self):
#         return self.timestamps;
    