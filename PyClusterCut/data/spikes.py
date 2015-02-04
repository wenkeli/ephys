import numpy as np

from ..fileIO.loadOpenEphysSpikes import readSpikes;

# class ChannelData:
#     self.waveForms=[];
#     self.gains=[];
#     self.params=dict();
#     
#     def __init(self, waveForms, gains):
#         self.waveForms=np.zeros(waveForms.shape, dtype="float32");
#         self.waveForms[:]=waveForms;
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
#         self.params["peak"]=np.max(self.waveForms[:, peakStart:peakEnd], 1);
#     
#     def calcPeakTime(self, peakStart=7, peakEnd=10):
#         self.params["peakTime"]=np.argmax(self.waveForms[:, peakStart:peakEnd], 1)+peakStart;
#     
#     def calcValley(self, valleyStart=10, valleyEnd=30):
#         self.params["valley"]=np.min(self.waveForms[:, valleyStart:valleyEnd], 1);
#         
#     def calcValley(self, valleyStart=10, valleyEnd=30):
#         self.params["valleyTime"]=np.argmin(self.waveForms[:, valleyStart:valley], 1)+valleyStart;
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
    def __init__(self, nChannels, nPointsPerChannel, waveForms, gains, thresholds, timeStamps, triggerChs=None):
        self.waveForms=[];
        self.timeStamps=[];
        
        self.thresholds=[];
        self.gains=[];
        
        self.triggerCh=[];
        
        self.params=dict();
        self.numChs=0;
        self.pointsPerCh=0;
        self.numSpikes=0;
        
        
        self.numSpikes=waveForms.shape(0);
        
        self.waveForms=np.array(np.copy(waveForms), dtype="float32");
        self.waveForms=self.waveForms.reshape((self.numSpikes, nChannels, nPointsPerChannel));
        self.waveForms=self.waveForms.transpose(1, 0, 3);
        
        self.timeStamps=np.zeros(timeStamps.shape, dtype="uint64");
        self.timeStamps[:]=timeStamps;
        
        self.thresholds=np.zeros(thresholds.T.shape, dtype="float32");
        self.thresholds[:]=thresholds.T;
        
        self.gains=np.zeros(gains.T.shape, dtype="float32");
        self.gains[:]=gains.T;
        
        calcTriggerChannel(triggerChs);
        
        calcParams();
        
    def calcTriggerChannel(self, triggerChs, triggerEndPoint=5):
        self.triggerCh=np.zeros(self.numSpikes, dtype="uint16");
        
        if(triggerChs!=None):
            self.triggerCh[:]=triggerChs;
            return;
        
        for i in np.r_[0:self.numChs]:
            isTrigger=np.sum((self.waveForms[i, :, 0:triggerEndPoint]>
                              self.thresholds[i, :]), 1)>0;
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
        return self.timeStamps;
    


# class SpikesData:
#     self.chs=[];
#     self.timeStamps=[];
#     self.numChs=0;
#     self.pointsPerCh=0;
#     
#     def __init__(self, nChannels, nPointsPerChannel, waveForms, gains, timeStamps):
#         self.chs=[None]*nChannels;
#         
#         for i in np.r_[0:nChannels]:
#             waveStart=nPointsPerChannel*i;
#             waveEnd=waveStart+nPointsPerChannel;
#             
#             self.chs[i]=ChannelData(waveForms[:, waveStart, waveEnd], gains[:, i]);
#             
#             self.timeStamps=timeStamps;
#             
#             self.numChs=nChannels;
#             self.pointsPerCh=nPointsPerChannel;
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
#         return self.timeStamps;
    