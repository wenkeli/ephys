from .samples import SamplesData;
from .samples import SamplesClustCount;

from matplotlib.path import Path;

import numpy as np;

class Boundary(object):
    def __init__(self, x, y, viewChs, viewParams):
        self.__points=np.array([x, y], dtype="float32");
        if((x[0]!=x[-1]) or (y[0]!=y[-1])):
            self.__points=np.float32(np.hstack((self.__points, [[x[0]], [y[0]]])));
        self.__viewChs=viewChs;
        self.__viewParams=viewParams;
        
    def __del__(self):
        del(self.__points);
        
    def isView(self, testVChs, testVParams):
        return ((self.__viewChs==testVChs) and (self.__viewParams==testVParams));
    
    def getPoints(self):
        return self.__points;
    
    def calcPointsInBoundary(self, dataX, dataY):
        pathCodes=np.zeros(self.__points.shape[1], dtype="int32");
        pathCodes[0]=Path.MOVETO;
        pathCodes[-1]=Path.CLOSEPOLY;
        pathCodes[1:-1]=Path.LINETO;
        
        boundary=Path(self.__points.T, pathCodes);
        
        return boundary.contains_points(np.array([dataX, dataY]).T);

class Cluster(object):
#     @staticmethod
#     def mergeClusters(clustersList):
#         numClusters=len(clustersList);
#         if(numClusters<=0):
#             return None;
#         
#         __data=clustersList[0].__data;
#         numSamples=__data.getNumSamples();
#         __sBA=np.zeros(numSamples, dtype="bool");
#         for i in np.r_[0:numClusters]:
#             __sBA=__sBA | clustersList[i].getSelectArray();
#             
#         return  Cluster(__data, __sBA);
    def __init__(self, samples, selectArray, sourceClust=None, clustCount=None, boundaries=[]):
        self.__data=samples;
        self.__sourceCluster=sourceClust;
        self.__sampleClustCnt=clustCount;
        self.__sBA=None;
        self.__boundaries=boundaries;
        
        self.__sBA=np.copy(selectArray);
            
        if(self.__sampleClustCnt is not None):
            self.__sampleClustCnt.addClustCount(self.__sBA);
            
    def __del__(self):
        self.removeSelect(self.__sBA);
        del(self.__sBA);
        del(self.__boundaries[:]);
        
    def getSelectArray(self):
        return self.__sBA;
    
    def getWaveforms(self, sBA=None, chN=None):
        if(sBA is None):
            sBA=self.__sBA;
        return self.__data.getWaveforms(sBA, chN);
    
    def getParam(self, chN, paramName):
        return self.__data.getParam(chN, paramName)[self.__sBA];
    
    def getParamAllChs(self, paramName):
        nChs=self.getNumChannels();
        paramdata=self.__data.getParamAllChs(paramName);
        if(paramdata.shape[0]==nChs):
            paramdata=paramdata[:, self.__sBA];
        else:
            paramdata=paramdata[self.__sBA];
            
        return paramdata;
    
    def getNumChannels(self):
        return self.__data.getNumChannels();
    
    def modifySelect(self, selectMod):
        removePoints=self.__sBA & (~selectMod);
        self.removeSelect(removePoints);
    
    def __updateParentClustSelect(self):
        if((self.__sourceCluster is not None) and (self.__sampleClustCnt is not None)):
            self.__sourceCluster.setSelect(self.__sampleClustCnt.getNoClustSamples());
    
    def setSelect(self, selectMod):
        self.removeSelect(self.__sBA);
        self.addSelect(selectMod);
    
    def addSelect(self, selectMod):
        if(self.__sampleClustCnt is not None):
            self.__sampleClustCnt.addClustCount(selectMod & (~self.__sBA));
        self.__sBA=self.__sBA | selectMod;
        self.__updateParentClustSelect();
        
    def removeSelect(self, selectMod):
        if(self.__sampleClustCnt is not None):
            self.__sampleClustCnt.minusClustCount(selectMod & (self.__sBA));         
        self.__sBA=self.__sBA & (~selectMod);
        self.__updateParentClustSelect();
        
    def addBoundary(self, boundary):
        self.__boundaries.append(boundary);
    
    def getBoundaries(self, viewChs=[], viewParams=[]):
        if(len(viewChs)==0 or len(viewParams)==0):
            return self.__boundaries;
        
        retList=[];
        for i in np.r_[0:len(self.__boundaries)]:
            if(self.__boundaries[i].isView(viewChs, viewParams)):
                retList.append(self.__boundaries[i]);
        
        return retList;
        


        