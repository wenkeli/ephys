import numpy as np;
import pyqtgraph as pg;

from PyQt5.QtGui import QBrush, QColor;

from .FastScatterPlotItem import FastScatterPlotItem;

from pyqtgraph.graphicsItems.ScatterPlotItem import ScatterPlotItem;

from ..data.cluster import Cluster;

class ClusterPlotItem(object):
    def __init__(self, cluster, plot, pen=None, brush=None):
        self.__cluster=cluster;
        
        if(pen is None):
            self.__pen=pg.mkPen(QColor("#DFDFDF"));
        else:
            self.__pen=pen;
            
        if(brush is None):
            self.__brush=QBrush(QColor("#DFDFDF"));
        else:
            self.__brush=brush;
#         self.__plotData=pg.ScatterPlotItem(x=[0, 1], y=[0, 1],
#                                       symbol="s", __pen=pg.mkPen("w"),
#                                       size=1);
        
#         self.__plotData=FastScatterPlotItem(x=[0], y=[0],
#                                       symbol="s", pen=self.__pen,
#                                       size=1, pointMode=False);
        self.__plotData=ScatterPlotItem(x=[0], y=[0], symbol="s",
                                            pen=self.__pen, brush=self.__brush, size=1);
        self.__plotDataBigP=ScatterPlotItem(x=[0], y=[0], symbol="s",
                                            pen=self.__pen, brush=self.__brush, size=2);
        self.__plotBoundaryData=pg.PlotDataItem(x=[0], y=[0], pen=self.__pen);     
        self.__plot=plot;
        self.__waveStartInd=0;
        self.__selPtsSequence=None;
        self.__calcSelPtsSequence();
        self.__selDispWaves=np.zeros(self.__cluster.getSelectArray().shape, dtype="bool");
        
    
    def setPlotData(self, xChN, yChN, xChParamT, yChParamT, drawType=0):
        if(drawType==0):
#             self.__plotData.setData(x=self.__cluster.getParam(xChN, xChParamT),
#                                   y=self.__cluster.getParam(yChN, yChParamT),
#                                   symbol="s", pen=self.__pen,
#                                   size=1, pointMode=False);
            self.__plotDataBigP.setData(x=self.__cluster.getParam(xChN, xChParamT),
                                        y=self.__cluster.getParam(yChN, yChParamT),
                                        symbol="s", pen=self.__pen, brush=self.__brush,
                                        size=1);
        else:
            self.__plotDataBigP.setData(x=self.__cluster.getParam(xChN, xChParamT),
                                        y=self.__cluster.getParam(yChN, yChParamT),
                                        symbol="s", pen=self.__pen, brush=self.__brush,
                                        size=2);
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
            
    
                              
    def addToPlot(self, drawType=0):
        if(drawType==0):
            self.__plot.addItem(self.__plotData);
        else:
            self.__plot.addItem(self.__plotDataBigP);
        self.__plot.addItem(self.__plotBoundaryData);
        
    def removeFromPlot(self, plotType=0):
        if(plotType==0):
            self.__plot.removeItem(self.__plotData);
        else:
            self.__plot.RemoveItem(self.__plotDataBigP);
        self.__plot.removeItem(self.__plotBoundaryData);
        
    def getCurPen(self):
        return self.__pen;
    
    def __calcSelPtsSequence(self):
        sBA=self.__cluster.getSelectArray();
        self.__selPtsSequence=np.cumsum(sBA);
        
    def getPrevWaves(self, indIncSize, trigChOnly):
        self.__calcSelPtsSequence();
        if(self.__waveStartInd<=0):
            return (None, None, None, None, None);
        self.__waveStartInd=self.__waveStartInd-indIncSize;
        if(self.__waveStartInd+indIncSize>=self.__getNumSelPts()):
            self.__waveStartInd=self.__getNumSelPts()-indIncSize;
#         self.__waveStartInd=self.__waveStartInd%self.__getNumSelPts();
        if(self.__waveStartInd<=0):
            self.__waveStartInd=0;
        sBA=self.__getSelPointsByRange(self.__waveStartInd, self.__waveStartInd+indIncSize);
        self.__selDispWaves=self.__selDispWaves | sBA;
        
        (nptsPerCh, waves, xvals, connArrs)=self.__cluster.getWaveforms(sBA, None, trigChOnly);
        return (self.__cluster.getNumChannels(), nptsPerCh, waves, xvals, connArrs);
        
    def getNextWaves(self, indIncSize, trigChOnly):
        self.__calcSelPtsSequence();
        if(self.__waveStartInd>=self.__getNumSelPts()):
            return (None, None, None, None, None);
        sBA=self.__getSelPointsByRange(self.__waveStartInd, self.__waveStartInd+indIncSize);
        self.__selDispWaves=self.__selDispWaves | sBA;
        
        self.__waveStartInd=self.__waveStartInd+indIncSize;
        
        (nptsPerCh, waves, xvals, connArrs)=self.__cluster.getWaveforms(sBA, None, trigChOnly);
        return (self.__cluster.getNumChannels(), nptsPerCh, waves, xvals, connArrs);
    
    def resetWaveInd(self):
        self.__waveStartInd=0;
        
    def clearSelDispWaves(self):
        self.__selDispWaves[:]=False;
        
    def resetViewWaves(self):
        self.__calcSelPtsSequence();
        
    def getSelDispWaves(self):
        (wAvg, wSEM, w25P, wMed, w75P)=self.__cluster.calcWaveStats();
        
        (nptsPerCh, waves, xvals, conArrs)=self.__cluster.getWaveforms(self.__selDispWaves, 
                                                                       None, False)
        return (waves, wAvg, wSEM, w25P, wMed, w75P);
    
    def __getSelPointsByRange(self, startInd, endInd):
        sBA=self.__cluster.getSelectArray();
        return sBA & ((self.__selPtsSequence>=startInd) & (self.__selPtsSequence<endInd));
    
    def __getNumSelPts(self):
        return self.__selPtsSequence[-1];
