import numpy as np;
import pyqtgraph as pg;
from PySide.QtCore import Qt;

class WorkBoundary(object):
    def __init__(self, plot):
        self.__boundPoints=None;
        self.__drawMovingBound=False;
        self.__closedBound=False;
        self.__drawBound=False;
        
        self.__boundPlotItem=None;
        self.__movingBoundItem=None;
        self.__proxyConList=[];
        
        self.__curMousePos=np.zeros(2, dtype="float32");
        
        self.__plot=plot;
        self.__plotVBox=self.__plot.getViewBox();
        
        self.reset(None);
        
    def reset(self, drawPen):
        self.__boundPoints=np.zeros((2, 0));
        self.__drawMovingBound=False;
        self.__closedBound=False;
        self.__drawBound=False;
        
        if(drawPen is None):
            drawPen="w";
            
        if((self.__boundPlotItem is None) or (self.__movingBoundItem is None)):
            self.__boundPlotItem=pg.PlotDataItem(x=[0], y=[0], pen=drawPen);
            self.__movingBoundItem=pg.PlotDataItem(x=[0], y=[0], pen=drawPen);
        else:
            self.__plot.removeItem(self.__boundPlotItem);
            self.__plot.removeItem(self.__movingBoundItem);
            self.__boundPlotItem.setData(x=[0], y=[0], pen=drawPen);
            self.__movingBoundItem.setData(x=[0], y=[0], pen=drawPen);
            
        self.__plot.addItem(self.__boundPlotItem);
        self.__plot.addItem(self.__movingBoundItem);
        
        if(len(self.__proxyConList)<=0):
            self.__proxyConList.append(pg.SignalProxy(self.__plot.scene().sigMouseClicked, 
                                                    rateLimit=100, 
                                                    slot=self.plotMouseClicked));
            self.__proxyConList.append(pg.SignalProxy(self.__plot.scene().sigMouseMoved,
                                                    rateLimit=100, slot=self.plotMouseMoved));
                                                    
    def plotMouseClicked(self, evt):
        if(self.__closedBound or (not self.__drawBound)):
            return;
        numPoints=self.__boundPoints.shape[1];
        if(evt[0].button()==Qt.MouseButton.RightButton):
            if(numPoints<3):
                return;
            
            self.__boundPoints=np.hstack((self.__boundPoints, 
                                        [[self.__boundPoints[0, 0]], [self.__boundPoints[1, 0]]]));
            self.__boundPlotItem.setData(x=self.__boundPoints[0, :], y=self.__boundPoints[1, :]);
            self.__movingBoundItem.setData(x=[0], y=[0]);
            
            self.__closedBound=True;
            self.__drawMovingBound=False;
            return;
        
        pos=evt[0].scenePos();
        mousePoint=self.__plotVBox.mapSceneToView(pos);
        
        point=[[mousePoint.x()], [mousePoint.y()]];
        self.__boundPoints=np.hstack((self.__boundPoints, point));
        self.__boundPlotItem.setData(x=self.__boundPoints[0, :], y=self.__boundPoints[1, :]);
        
        self.__drawMovingBound=True;
        self.__closedBound=False;
        
    
    def plotMouseMoved(self, evt):
        if(not self.__drawBound):
            return;
        pos=evt[0];
        if((not self.__plot.sceneBoundingRect().contains(pos)) 
           or (not self.__drawMovingBound) or (self.__closedBound)):
            return;
        
        mousePoint=self.__plotVBox.mapSceneToView(pos);
        self.__curMousePos[0]=mousePoint.x();
        self.__curMousePos[1]=mousePoint.y();
        self.__movingBoundItem.setData(x=[self.__boundPoints[0, -1], mousePoint.x()],
                                     y=[self.__boundPoints[1, -1], mousePoint.y()]);
                                     
                                     
    def stepBackBoundary(self):
        if(not self.__drawBound):
            return;
        numPoints=self.__boundPoints.shape[1];
        if(numPoints<=0):
            return;
        
        self.__boundPoints=self.__boundPoints[:, 0:-1];
        self.__boundPlotItem.setData(x=self.__boundPoints[0, :], y=self.__boundPoints[1, :]);
        
        numPoints=self.__boundPoints.shape[1];
        self.__drawMovingBound=numPoints>0;
        if(not self.__drawMovingBound):
            self.__movingBoundItem.setData(x=[0], y=[0]);
        self.__closedBound=False;
        
        
    def setDrawBound(self, draw):
        self.__drawBound=draw;
        
    def getBoundX(self):
        return self.__boundPoints[0, :];

    def getBoundY(self):
        return self.__boundPoints[1, :];
    
    def getBoundPoints(self):
        return self.__boundPoints;
    
    def getBoundClosed(self):
        return self.__closedBound;
    