from .samples import SamplesData;
from .samples import SamplesClustCount;

from matplotlib.path import Path;

import numpy as np;

class Boundary(object):
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

class Cluster(object):
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
    def __init__(self, samples, selectArray, sourceClust=None, clustCount=None, boundaries=[]):
        self.data=samples;
        self.sourceCluster=sourceClust;
        self.sampleClustCnt=clustCount;
        self.sBA=[];
        self.boundaries=boundaries;
        
        self.sBA=np.copy(selectArray);
            
        if(self.sampleClustCnt!=None):
            self.sampleClustCnt.addClustCount(self.sBA);
            
    def __del__(self):
        self.removeSelect(self.sBA);
        del(self.sBA);
        del(self.boundaries[:]);
        
    def getSelectArray(self):
        return self.sBA;
    
    def getWaveforms(self, chN=None):
        waveforms=self.data.getWaveforms(chN);
        if(chN==None):
            return waveforms[:, self.sBA, :];
        return waveforms[self.sBA, :];
    
    def getParam(self, chN, paramName):
        return self.data.getParam(chN, paramName)[self.sBA];
    
    def modifySelect(self, selectMod):
        removePoints=self.sBA & (~selectMod);
        self.removeSelect(removePoints);
    
    def updateParentClustSelect(self):
        if((self.sourceCluster!=None) and (self.sampleClustCnt!=None)):
            self.sourceCluster.setSelect(self.sampleClustCnt.getNoClustSamples());
    
    def setSelect(self, selectMod):
        self.removeSelect(self.sBA);
        self.addSelect(selectMod);
    
    def addSelect(self, selectMod):
        if(self.sampleClustCnt!=None):
            self.sampleClustCnt.addClustCount(selectMod & (~self.sBA));
        self.sBA=self.sBA | selectMod;
        self.updateParentClustSelect();
        
    def removeSelect(self, selectMod):
        if(self.sampleClustCnt!=None):
            self.sampleClustCnt.minusClustCount(selectMod & (self.sBA));         
        self.sBA=self.sBA & (~selectMod);
        self.updateParentClustSelect();
        
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
        


        