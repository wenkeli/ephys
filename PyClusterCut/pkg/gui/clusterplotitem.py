import numpy as np;
import pyqtgraph as pg;
import FastScatterPlotItem as fscatter;

from ..data.cluster import Cluster;

class ClusterPlotItem(object):
    def __init__(self, cluster, plot, pen=None):
        self.__cluster=cluster;
        self.__numSelPoints=None;
        
        self.__calcNumSelPoints();
        if(pen is None):
            self.__pen=pg.mkPen("w");
        else:
            self.__pen=pen;
#         self.__plotData=pg.ScatterPlotItem(x=[0, 1], y=[0, 1],
#                                       symbol="s", __pen=pg.mkPen("w"),
#                                       size=1);
        

        self.__plotData=fscatter.FastScatterPlotItem(x=[0], y=[0],
                                      symbol="s", pen=self.__pen,
                                      size=1, pointMode=True);
        self.__plotBoundaryData=pg.PlotDataItem(x=[0], y=[0], pen=self.__pen);     
        self.__plot=plot;
        self.__waveStartInd=0;
        self.__selDispWaves=np.zeros(self.__cluster.getSelectArray().shape, dtype="bool");
        
        
    
    def setPlotData(self, xChN, yChN, xChParamT, yChParamT):
        self.__plotData.setData(x=self.__cluster.getParam(xChN, xChParamT),
                              y=self.__cluster.getParam(yChN, yChParamT),
                              symbol="s", pen=self.__pen,
                              size=1, pointMode=True);
        self.__calcNumSelPoints();
        
        boundaries=self.__cluster.getBoundaries([xChN, yChN], [xChParamT, yChParamT]);
        if(len(boundaries)>0):
            points=np.zeros((2, 0));
            connArr=np.zeros(0, dtype="bool");
            for i in boundaries:
                curPoints=i.getPoints();
                points=np.hstack((points, curPoints));
                curCon=np.zeros(curPoints.shape[1], dtype="bool");
                curCon[:-1]=True;
                connArr=np.hstack((connArr, curCon));
            self.__plotBoundaryData.setData(x=points[0, :], y=points[1, :], 
                                            connect=connArr);
        else:
            self.__plotBoundaryData.setData(x=[0], y=[0], connect="all");
            
            
                              
    def addToPlot(self):
        self.__plot.addItem(self.__plotData);
        self.__plot.addItem(self.__plotBoundaryData);
        
    def removeFromPlot(self):
        self.__plot.removeItem(self.__plotData);
        self.__plot.removeItem(self.__plotBoundaryData);
        
    def getCurPen(self):
        return self.__pen;
    
    def __calcNumSelPoints(self):
        sBA=self.__cluster.getSelectArray();
        self.__numSelPoints=np.cumsum(sBA);
        
    def getPrevWaves(self, indIncSize):
        if(self.__waveStartInd<=0):
            return (None, None, None, None, None);
        self.__waveStartInd=self.__waveStartInd-indIncSize;
        if(self.__waveStartInd+indIncSize>=self.__getTotalSelPoints()):
            self.__waveStartInd=self.__getTotalSelPoints()-indIncSize;
#         self.__waveStartInd=self.__waveStartInd%self.__getTotalSelPoints();
        if(self.__waveStartInd<=0):
            self.__waveStartInd=0;
        sBA=self.__getSelPointsByRange(self.__waveStartInd, self.__waveStartInd+indIncSize);
        self.__selDispWaves=self.__selDispWaves | sBA;
        
        (nptsPerCh, waves, xvals, connArr)=self.__cluster.getWaveforms(sBA, None);
        return (self.__cluster.getNumChannels(), nptsPerCh, waves, xvals, connArr);
        
    def getNextWaves(self, indIncSize):
        if(self.__waveStartInd>=self.__getTotalSelPoints()):
            return (None, None, None, None, None);
        sBA=self.__getSelPointsByRange(self.__waveStartInd, self.__waveStartInd+indIncSize);
        self.__selDispWaves=self.__selDispWaves | sBA;
        
        self.__waveStartInd=self.__waveStartInd+indIncSize;
        
        (nptsPerCh, waves, xvals, connArr)=self.__cluster.getWaveforms(sBA, None);
        return (self.__cluster.getNumChannels(), nptsPerCh, waves, xvals, connArr);
    
    def resetWaveInd(self):
        self.__waveStartInd=0;
        
    def clearSelDispWaves(self):
        self.__selDispWaves[:]=False;
        
    def getSelDispWaves(self):
        (nptsPerCh, waves, xvals, conArr)=self.__cluster.getWaveforms(None, None);
        
        wAvg=np.average(waves, 1);
        wSEM=np.std(waves, 1)/np.sqrt(waves.shape[1]);
        
        (nptsPerCh, waves, xvals, conArr)=self.__cluster.getWaveforms(self.__selDispWaves, None);
        return (waves, wAvg, wSEM);
    
    def __getSelPointsByRange(self, startInd, endInd):
        sBA=self.__cluster.getSelectArray();
        return sBA & ((self.__numSelPoints>=startInd) & (self.__numSelPoints<endInd));
    
    def __getTotalSelPoints(self):
        return self.__numSelPoints[-1];
