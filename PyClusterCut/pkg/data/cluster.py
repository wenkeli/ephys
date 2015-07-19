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
    
    def getView(self):
        return (self.__viewChs, self.__viewParams);
    
    def getPoints(self):
        return self.__points;
    
    def calcPointsInBoundary(self, dataX, dataY):
        pathCodes=np.zeros(self.__points.shape[1], dtype="int32");
        pathCodes[0]=Path.MOVETO;
        pathCodes[-1]=Path.CLOSEPOLY;
        pathCodes[1:-1]=Path.LINETO;
        
        boundary=Path(self.__points.T, pathCodes);
        
        return boundary.contains_points(np.array([dataX, dataY]).T);
    
class ClustHistStep(object):
    def __init__(self, selectArr, boundary):
        self.__sBA=selectArr;
        self.__boundary=boundary;
        
    def getView(self):
        if(self.__boundary is None):
            return None;
        return self.__boundary.getView();
    
    def getSelectArr(self):
        return self.__sBA;
    
    def getBoundary(self):
        return self.__boundary;
    
    

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
        self.__rating=-1;
        self.__history=None;
        
        self.__sBA=np.copy(selectArray);
            
        if(self.__sampleClustCnt is not None):
            self.__sampleClustCnt.addClustCount(self.__sBA);
        self.__initHistory();
        
    def __initHistory(self):
        self.__history=[];
        if(len(self.__boundaries)>0):
            self.__addToHist(self.__sBA, self.__boundaries[-1]);
        else:
            self.__addToHist(self.__sBA);
            
    def __del__(self):
        self.__removeSelect(self.__sBA);
        del(self.__sBA);
        del(self.__boundaries[:]);
        try:
            del(self.__history[:]);
        except AttributeError:
            self.__history=[];
        
    def getRating(self):
        try:
            rating=self.__rating;
        except AttributeError:
            self.__rating=-1;
            rating=self.__rating;
        return rating;
    
    
    def setRating(self, rating):
        self.__rating=rating;
        
    def getSelectArray(self):
        return self.__sBA;
    
    def getWaveforms(self, sBA=None, chN=None, trigChOnly=False):
        if(sBA is None):
            sBA=self.__sBA;
        return self.__data.getWaveforms(sBA, chN, trigChOnly);
    
    def calcWaveStats(self):
        (nptsPerCh, waves, xvals, conArrs)=self.__data.getWaveforms(self.__sBA, None, False);
        waves=np.array(waves);
        wAvg=np.average(waves, 1);
        wSEM=np.std(waves, 1)/np.sqrt(waves.shape[1]);
        w25P=np.percentile(waves, 25.0, 1);
        w75P=np.percentile(waves, 75.0, 1);
        wMed=np.percentile(waves, 50.0, 1);
        return (wAvg, wSEM, w25P, wMed, w75P);
#         
    
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
    
    def __modifySelect(self, selectMod):
        removePoints=self.__sBA & (~selectMod);
        self.__removeSelect(removePoints);
    
    def __updateParentClustSelect(self):
        if((self.__sourceCluster is not None) and (self.__sampleClustCnt is not None)):
            self.__sourceCluster.__setSelect(self.__sampleClustCnt.getNoClustSamples());
    
    def __validateHistory(self):
        try:
            histLen=len(self.__history);
            if(histLen<=0):
                self.__initHistory();
        except AttributeError:
            self.__initHistory();
            
    
    def removePoints(self, sBA, addToHist):
        self.__validateHistory();
        self.__removeSelect(sBA);
        if(addToHist):
            self.__addToHist(self.__sBA);
    
    def refineClust(self, clustBound, sBA):
        self.__validateHistory();
        self.__addBoundary(clustBound);
        self.__modifySelect(sBA);
        self.__addToHist(self.__sBA, clustBound);
        
    def stepBack(self):
        self.__validateHistory();
        if(len(self.__history)<=1):
            return self.__history[-1].getView();
        
        step=self.__history.pop();
        boundary=step.getBoundary();
        if(boundary is not None):
            self.__boundaries.remove(boundary);
        
        step=self.__history[-1];
        sBA=step.getSelectArr();
        self.__setSelect(sBA);
        return step.getView();
            
        
    def __addToHist(self, sBA, boundary=None):
        histStep=ClustHistStep(sBA, boundary);
        try:
            self.__history.append(histStep);
        except AttributeError:
            self.__history=[];
            self.__addToHist(self.__sBA, self.__boundaries[-1]);
            self.__history.append(histStep);
        
    
    def __setSelect(self, selectMod):
        self.__removeSelect(self.__sBA);
        self.__addSelect(selectMod);
    
    def __addSelect(self, selectMod):
        if(self.__sampleClustCnt is not None):
            self.__sampleClustCnt.addClustCount(selectMod & (~self.__sBA));
        self.__sBA=self.__sBA | selectMod;
        self.__updateParentClustSelect();
        
    def __removeSelect(self, selectMod):
        if(self.__sampleClustCnt is not None):
            self.__sampleClustCnt.minusClustCount(selectMod & (self.__sBA));         
        self.__sBA=self.__sBA & (~selectMod);
        self.__updateParentClustSelect();
        
    def __addBoundary(self, boundary):
        self.__boundaries.append(boundary);
    
    def getBoundaries(self, viewChs=[], viewParams=[]):
        if(len(viewChs)==0 or len(viewParams)==0):
            return self.__boundaries;
        
        retList=[];
        for i in np.r_[0:len(self.__boundaries)]:
            if(self.__boundaries[i].isView(viewChs, viewParams)):
                retList.append(self.__boundaries[i]);
        
        return retList;
        


        