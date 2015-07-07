import pyqtgraph as pg;
import numpy as np;
from pyqtgraph.widgets.GraphicsLayoutWidget import GraphicsLayoutWidget;

class WavePlots(object):
    def __init__(self, layout):
        self.__layout=layout;
        self.__plots=[];
        self.__numPlots=0;        
        
    def reset(self):
        for i in np.r_[0:len(self.__plots)]:
            self.__layout.removeItem(self.__plots[0]);
            del(self.__plots[0]);
        self.__plots=[];
        self.__numPlots=0;
        
        
    def initializePlots(self, numPlots):
        self.__numPlots=numPlots;
        for i in np.r_[0:numPlots]:
            plot=self.__layout.addPlot(i, 0, enableMenu=False);
            self.__plots.append(plot);
            
    
    def drawWaves(self, waves, xvals, conArrs, drawPen):
        if(waves is None):
            return;
        yMin=100000.0;
        yMax=-100000.0;
        for i in np.r_[0:self.__numPlots]:
            if((waves[i] is None) or (len(waves[i])<=0)):
                continue;
            
            self.__plots[i].plot(xvals[i].flatten(), waves[i][:, :].flatten(),
                                 pen=drawPen, connect=conArrs[i].flatten());
            self.__plots[i].getViewBox().autoRange();
            boxRange=self.__plots[i].getViewBox().viewRange();
            boxMin=boxRange[1][0];
            boxMax=boxRange[1][1];
            if(boxMin<yMin):
                yMin=boxMin;
            if(boxMax>yMax):
                yMax=boxMax;
                
        for plot in self.__plots:
            plot.getViewBox().setYRange(yMin, yMax);
            
    
    def clearPlots(self):
        for plot in self.__plots:
            plot.getViewBox().autoRange();
            plot.clear();
            
            