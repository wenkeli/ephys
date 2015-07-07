import pyqtgraph as pg;
from pyqtgraph.widgets.GraphicsLayoutWidget import GraphicsLayoutWidget;

from .axiscontrol import AxisControl; 

class MainPlot(object):
    def __init__(self, plot, hAxis, vAxis):
        self.__hAxis=hAxis;
        self.__vAxis=vAxis;
        
#         self.__plot=plotW.addPlot(0, 0, 1, 1, enableMenu=False);
        self.__plot=plot;
        self.__plotScene=self.__plot.scene();
        self.__plotScene.setMoveDistance(200);
        self.__plotVBox=self.__plot.getViewBox();
        self.__plotVBox.setMouseMode(pg.ViewBox.RectMode);
        self.__plotVBox.disableAutoRange();
        
    def reset(self):
        self.__plot.clear();
        
    def getPlot(self):
        return self.__plot;
    
    def updateLimits(self):
        hLim=self.__hAxis.getLimits();
        vLim=self.__vAxis.getLimits();
        self.__plotVBox.setXRange(hLim[0], hLim[1]);
        self.__plotVBox.setYRange(vLim[0], vLim[1]);
        
    
