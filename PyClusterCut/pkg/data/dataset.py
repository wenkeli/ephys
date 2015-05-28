import numpy as np;

from .samples import SamplesData, SamplesClustCount;
from .cluster import Cluster, Boundary;

class DataSet(object):
    def __init__(self, waveforms, gains, thresholds, timestamps, samplingHz, triggerChs):
        self.__samples=SamplesData(waveforms, gains, thresholds, timestamps, samplingHz, triggerChs);
        self.__workingSet=None;
        self.__workingSetStartTime=-1;
        self.__workingSetEndTime=-1;
        
        self.__sampleClustCnt=SamplesClustCount(self.__samples.getNumSamples());
        
        self.__clusters=dict();
        self.__maxClustN=0;
        self.__maxClustID="";
        self.__workClustID="";
        self.__initClustID="";
        
        self.__workingSetInit=False;
        
        
    def initializeWorkingSet(self, startTime=-1, endTime=-1):
        if(self.__workingSetInit):
            return;
        
        timeStamps=self.__samples.getParam(0, "timestamp");
        if(startTime<0):
            startTime=timeStamps[0];
        if(endTime<0):
            endTime=timeStamps[-1];
            
        self.__workingSet=(timeStamps>=startTime) & (timeStamps<=endTime);
        self.__workingSetStartTime=startTime;
        self.__workingSetEndTime=endTime;
            
        self.__addClusterToList(False, False);
        self.__initClustID=self.__workClustID;
        
        self.__workingSetInit=True;
        
        return (self.__initClustID, self.__clusters[self.__initClustID]);
        
    def getSamplesStartEndTimes(self):
        timeStamps=self.__samples.getParam(0, "timestamp");
        return (timeStamps[0], timeStamps[-1]);
    
    def getWorkingStartEndTimes(self):
        return (self.__workingSetStartTime, self.__workingSetEndTime);
        
    def __addClusterToList(self, copy, isNotInitClust, clustBounds=[], pointsBA=[]):
        self.__maxClustID=str(self.__maxClustN);
         
        if(isNotInitClust):
            self.__clusters[self.__maxClustID]=Cluster(self.__samples, 
                                                       (pointsBA & self.__workingSet), 
                                                       self.__clusters[self.__initClustID],
                                                       self.__sampleClustCnt, clustBounds);
        else:
            self.__clusters[self.__maxClustID]=Cluster(self.__samples, self.__workingSet,
                                                       None, None, clustBounds);
            self.__workClustID=self.__maxClustID;
                                                   
        if((len(pointsBA)>0) and (self.__workClustID!="") and (not copy)):
            self.__clusters[self.__workClustID].removeSelect(pointsBA);
                    
        self.__maxClustN=self.__maxClustN+1;
        
        return  (self.__maxClustID, self.__clusters[self.__maxClustID]);

    
    def __calcPointsInBoundary(self, hChN, vChN, hParam, vParam, boundX, boundY):
        viewChs=[hChN, vChN];
        viewParams=[hParam, vParam];
        bound=Boundary(boundX, boundY, viewChs, viewParams);
        
        pointsBA=bound.calcPointsInBoundary(self.__samples.getParam(hChN, hParam),
                                            self.__samples.getParam(vChN, vParam));
                                            
        workingPoints=self.__clusters[self.__workClustID].getSelectArray();
        if(self.__workClustID==self.__initClustID):
            workingPoints=self.__workingSet;
            
        clusterPointsBA=pointsBA & workingPoints;
        
        return (bound, clusterPointsBA);
        
    
    def deleteCluster(self, ind):
        if(ind==self.__initClustID):
            return (False, self.__workClustID);
        
        del(self.__clusters[ind]);
        self.__workClustID=self.__initClustID;
        
        return (True, self.__workClustID);
    
    
    def addCluster(self, copy, hChN, vChN, hParam, vParam, boundX, boundY):
        (clustBound, pointsBA)=self.__calcPointsInBoundary(hChN, vChN, hParam, vParam,
                                                                boundX, boundY);
        if(np.sum(pointsBA)<=0):
            return (None, None);
        
        (clustID, cluster)=self.__addClusterToList(copy, True, [clustBound], pointsBA);
        return (clustID, cluster);
    
    
    def refineCluster(self, hChN, vChN, hParam, vParam, boundX, boundY):
        if(self.__workClustID==self.__initClustID):
            return;
        
        (clustBound, pointsBA)=self.__calcPointsInBoundary(hChN, vChN, hParam, vParam, 
                                                           boundX, boundY);
        self.__clusters[self.__workClustID].addBoundary(clustBound);
        self.__clusters[self.__workClustID].modifySelect(pointsBA);
    
    
    def setWorkClustID(self, id):
        self.__workClustID=id;
        
        return self.__clusters[self.__workClustID];
    
    
    def getWorkClustID(self):
        return self.__workClustID;
    
    def getInitClustID(self):
        return self.__initClustID;
    
    def getWorkingCluster(self):
        return self.getCluster(self.__workClustID);

    def getClusterIDs(self):
        keys=self.__clusters.keys();
        keys.sort(key=int);
        return keys;
    
    def compareClustersOverlap(self, ind, compInd):
        indSelArray=self.__clusters[ind].getSelectArray();
        compIndSelArray=self.__clusters[compInd].getSelectArray();
        indNumPoints=np.sum(indSelArray);
        overlapNumPoints=np.sum(indSelArray & compIndSelArray);
        return (indNumPoints, overlapNumPoints);
    
    def computeClusterOverlap(self, ind):
        indSelArray=self.__clusters[ind].getSelectArray();
        overlapPoints=self.__sampleClustCnt.getMinClustSamples(2);
        indNumPoints=np.sum(indSelArray);
        overlapNumPoints=np.sum(indSelArray & overlapPoints);
        return (indNumPoints, overlapNumPoints);

    def getCluster(self, id):
        return self.__clusters[id];
    
    def getSamples(self):
        return self.__samples;
    
    