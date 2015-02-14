from .spikes import SamplesData;

from matplotlib.path import Path;

import numpy as np;

class Boundary:
    def __init__(self, x, y, viewChs, viewParams):
        self.points=np.array([x, y], dtype="float32");
        if((x[0]!=x[-1]) or (y[0]!=y[-1])):
            self.points=np.float32(np.hstack((self.points, [[x[0]], [y[0]]])));
        self.viewChs=viewChs;
        self.viewParams=viewParams;
        
    def __del__(self):
        del(self.points);
        
    def isView(self, testVChs, testVParams):
        return ((self.viewChs==testVChs) and (self.viewParams==testVParams));
    
    def getPoints(self):
        return self.points;
    
    def calcPointsInBoundary(self, dataX, dataY):
        pathCodes=np.zeros(self.points.shape[1], dtype="int32");
        pathCodes[0]=Path.MOVETO;
        pathCodes[-1]=Path.CLOSEPOLY;
        pathCodes[1:-1]=Path.LINETO;
        
        boundary=Path(self.points.T, pathCodes);
        
        return boundary.contains_points(np.array([dataX, dataY]).T);

class Cluster:
#     @staticmethod
#     def mergeClusters(clustersList):
#         numClusters=len(clustersList);
#         if(numClusters<=0):
#             return None;
#         
#         data=clustersList[0].data;
#         numSamples=data.getNumSamples();
#         sBA=np.zeros(numSamples, dtype="bool");
#         for i in np.r_[0:numClusters]:
#             sBA=sBA | clustersList[i].getSelectArray();
#             
#         return  Cluster(data, sBA);
    def __init__(self, samples, parent=None, boundaries=[], selectArray=[]):
        self.data=samples;
        self.parentClust=parent;
        self.sBA=[];
        self.boundaries=boundaries;
        
        if(len(selectArray)<=0):
            self.sBA=np.zeros(self.data.getNumSamples(), dtype="bool");
            self.sBA[:]=True;
        else:
            self.sBA=np.copy(selectArray);
            
    def __del__(self):
        self.addToParentClust();
        del(self.sBA);
        del(self.boundaries[:]);
        
    def getSelectArray(self):
        return self.sBA;
    
    def getWaveforms(self, chN=None):
        waveforms=self.data.getWaveforms(chN);
        if(chN==None):
            return waveforms[:, self.sBA, :];
        return waveforms[self.sBA, :];
    
    def getSampleTimes(self):
        return self.data.getSampleTimes()[self.sBA];
    
    def getParam(self, chN, paramType):
        return self.data.getChParam(chN, paramType)[self.sBA];
    
    def modifySelect(self, selectMod):
        retPoints=self.sBA & (~selectMod);
        self.sBA=self.sBA & selectMod;
        if(self.parentClust!=None):
            self.parentClust.addSelect(retPoints);
        return retPoints;
    
    def setParentClust(self, parentClust):
        self.parentClust=parentClust;
    
    def addToParentClust(self):
        if(self.parentClust==None):
            return;
        self.parentClust.addSelect(self.sBA);
    
    def addSelect(self, selectMod):
        self.sBA=self.sBA | selectMod;
        
    def removeSelect(self, selectMod):
        self.sBA=self.sBA & (~selectMod);
        
    def addBoundary(self, boundary):
        self.boundaries.append(boundary);
    
    def getBoundaries(self, viewChs=[], viewParams=[]):
        if(len(viewChs)==0 or len(viewParams)==0):
            return self.boundaries;
        
        retList=[];
        for i in np.r_[0:len(self.boundaries)]:
            if(self.boundaries[i].isView(viewChs, viewParams)):
                retList.append(self.boundaries[i]);
        
        return retList;
        


        