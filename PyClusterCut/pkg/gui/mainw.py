import os;

import numpy as np;

import PySide;

from PySide.QtGui import QMainWindow, QApplication;
from PySide.QtGui import QAbstractItemView, QListWidget, QListWidgetItem;
from PySide.QtGui import QKeySequence, QKeySequence, QShortcut, QFileDialog;

from PySide.QtCore import Qt, QRect;

import pyqtgraph as pg;
from pyqtgraph.widgets.GraphicsLayoutWidget import GraphicsLayoutWidget;

from mainw_ui import Ui_MainW;

import FastScatterPlotItem as fscatter;

from ..fileIO.loadOpenEphysSpikes import readSamples;

from ..data.spikes import SamplesData;
from ..data.cluster import Cluster, Boundary;

class ClusterPlotItem:
    def __init__(self, cluster):
        self.cluster=cluster;
#         self.plotData=pg.ScatterPlotItem(x=[0, 1], y=[0, 1],
#                                       symbol="s", pen=pg.mkPen("w"),
#                                       size=1);
        self.plotData=fscatter.FastScatterPlotItem(x=[0, 1], y=[0, 1],
                                      symbol="s", pen=pg.mkPen("w"),
                                      size=1, pointMode=True);

    def setPlotData(self, xChN, yChN, xChParamT, yChParamT):
        self.plotData.setData(self.cluster.getParam(xChN, xChParamT),
                              self.cluster.getParam(yChN, yChParamT),
                              symbol="s", pen=pg.mkPen("w"),
                              size=1, pointMode=True);
                              
    def addToPlot(self, plot):
        plot.addItem(self.plotData);
        


class MainW(QMainWindow, Ui_MainW):
    def __init__(self, app, parent=None):
        super(MainW, self).__init__(parent);
        self.setupUi(self);
        self.setUIEnabled(False);
        self.setFocusPolicy(Qt.StrongFocus);
        self.setWindowFlags(Qt.CustomizeWindowHint
                            | Qt.WindowMinimizeButtonHint);
                            
        self.app=app;
        screenSize=QApplication.desktop().screenGeometry();
        sh=screenSize.height();
        sw=screenSize.width();
        
        cpw=self.geometry().width();
        
        self.plotW=GraphicsLayoutWidget();
#         self.plotW.resize(sw-cpw-50, sh);
        self.plotW.resize(1500, 1000);
        self.plotW.setFocusPolicy(Qt.StrongFocus);
        self.plotW.setObjectName("GraphicsWindow");
        self.plotW.setWindowFlags(Qt.CustomizeWindowHint
                                  | Qt.WindowMinimizeButtonHint);
        self.plotW.show();
        
        self.plot=self.plotW.addPlot(enableMenu=False);
        
        self.plotScene=self.plot.scene();
        self.plotScene.setMoveDistance(200);
        
        self.plotVBox=self.plot.getViewBox();
        self.plotVBox.setMouseMode(pg.ViewBox.RectMode);
        self.plotVBox.disableAutoRange();
        
        self.shortCuts=dict();
        self.setupKeyShortcuts(self);
        self.setupKeyShortcuts(self.plotW);
        self.enableKeyShortcuts(False);
        
        self.hChsList=[];
        self.vChsList=[];
        self.hParamsList=[];
        self.vParamsList=[];
        self.selectDataRole=0;
        self.xChN=None;
        self.yChN=None;
        self.xParamT=None;
        self.yParamT=None;
        self.workClustN=0;
        self.viewValid=False;
        
        self.boundPoints=[];
        self.drawBound=False;
        self.closedBound=False;
        self.boundPlotItem=None;
        self.movingBoundItem=None;
        self.proxyConList=[];
        self.curMousePos=np.zeros(2, dtype="float32");
        self.initBound();
        
        self.dataDir="";
        self.data=None;
        self.clusters=[];
        self.plotClusterItems=[];
        self.dataValid=False;


    def initBound(self):
        self.boundPoints=np.zeros((2, 0));
        self.drawBound=False;
        self.closedBound=False;
        if((self.boundPlotItem==None) or (self.movingBoundItem==None)):
            self.boundPlotItem=pg.PlotDataItem(x=[0], y=[0], pen="w");
            self.movingBoundItem=pg.PlotDataItem(x=[0], y=[0], pen="w");
            self.plot.addItem(self.boundPlotItem);
            self.plot.addItem(self.movingBoundItem);
        else:
            self.boundPlotItem.setData(x=[0], y=[0]);
            self.movingBoundItem.setData(x=[0], y=[0]);
            
        if(len(self.proxyConList)<=0):
            self.proxyConList.append(pg.SignalProxy(self.plot.scene().sigMouseClicked, 
                                                    rateLimit=100, 
                                                    slot=self.plotMouseClicked));
            self.proxyConList.append(pg.SignalProxy(self.plot.scene().sigMouseMoved,
                                                    rateLimit=100, slot=self.plotMouseMoved));
        
    
        

    def setUIEnabled(self, enable):
        self.saveFileButton.setEnabled(enable);
        
        self.hChannelSelect.setEnabled(enable);
        self.hParamSelect.setEnabled(enable);
        
        self.vChannelSelect.setEnabled(enable);
        self.vParamSelect.setEnabled(enable);
        
        self.workClusterSelect.setEnabled(enable);
        self.viewClustersSelect.setEnabled(enable);
        
        self.viewButton.setEnabled(enable);



    def quit(self):
        self.app.closeAllWindows();
        
    def loadFile(self):
        print("loading file");
        fileName=QFileDialog.getOpenFileName(self, self.tr("open spike file"), 
                                             self.tr(self.dataDir), 
                                             self.tr("spike files (*.spikes)"));
        fileName=fileName[0];
        if(fileName==""):
            return;
        
        self.dataDir=os.path.dirname(fileName);
        
        file=open(fileName, "rb");
        fileStat=os.stat(fileName);        
        data=readSamples(file, fileStat.st_size, 1024, "=Bq3H", "H", "H", 2, "H", 3, 4);
        file.close();
        
        print("calculating parameters");
        self.data=SamplesData(data["waveforms"], data["gains"], data["thresholds"], data["timestamps"], None);
        print("done");
        self.clusters.append(Cluster(self.data));
        self.plotClusterItems.append(ClusterPlotItem(self.clusters[0]));
        
        self.initBound();
        self.setUIEnabled(True);
        self.populateSelect();
        self.enableKeyShortcuts(True);
        self.dataValid=True;
        self.viewValid=False;
        
        
        
    def populateSelect(self):
        self.hChannelSelect.clear();
        self.hParamSelect.clear();
        self.vChannelSelect.clear();
        self.vParamSelect.clear();
        self.workClusterSelect.clear();
        self.viewClustersSelect.clear();
        
        numChannels=self.data.getNumChannels();
        self.hChsList=[None]*numChannels;
        self.vChsList=[None]*numChannels;
        for i in np.r_[0:numChannels]:
            self.hChsList[i]=QListWidgetItem(str(i));
            self.hChsList[i].setData(self.selectDataRole, i);
            self.hChannelSelect.addItem(self.hChsList[i]);
            
            self.vChsList[i]=QListWidgetItem(str(i));
            self.vChsList[i].setData(self.selectDataRole, i);
            self.vChannelSelect.addItem(self.vChsList[i]);
            
        paramKeys=self.data.getChParamTypes();
        numParams=len(paramKeys);
        self.hParamsList=[None]*numParams;
        self.vParamsList=[None]*numParams;
        for i in np.r_[0:numParams]:
            self.hParamsList[i]=QListWidgetItem(paramKeys[i]);
            self.hParamsList[i].setData(self.selectDataRole, paramKeys[i]);
            self.hParamSelect.addItem(self.hParamsList[i]);
            
            self.vParamsList[i]=QListWidgetItem(paramKeys[i]);
            self.vParamsList[i].setData(self.selectDataRole, paramKeys[i]);
            self.vParamSelect.addItem(self.vParamsList[i]);
            
        
    def setupKeyShortcuts(self, widget):
        widgetName=widget.objectName();
        self.shortCuts[widgetName]=[];
        
        self.shortCuts[widgetName].append(QShortcut(QKeySequence(self.tr("V")),
                                          widget, self.updatePlotView));      
        
    def enableKeyShortcuts(self, enable):
        keys=self.shortCuts.keys();
        
        for i in keys:
            numKeys=len(self.shortCuts[i]);            
            for j in np.r_[0:numKeys]:
                self.shortCuts[i][j].setEnabled(enable);
                
    def updatePlotView(self):
        hChSel=self.hChannelSelect.selectedItems();
        vChSel=self.vChannelSelect.selectedItems();
        hParamSel=self.hParamSelect.selectedItems();
        vParamSel=self.vParamSelect.selectedItems();
        
        self.plot.clear();
        self.initBound();
        
        if((len(hChSel)==0) or (len(vChSel)==0) or (len(hParamSel)==0) or (len(vParamSel)==0)):
            return;
        self.xChN=hChSel[0].data(self.selectDataRole);
        self.yChN=vChSel[0].data(self.selectDataRole);
        self.xParamT=hParamSel[0].data(self.selectDataRole);
        self.yParamT=vParamSel[0].data(self.selectDataRole);
        
        self.plotClusterItems[0].setPlotData(self.xChN, self.yChN, self.xParamT, self.yParamT);
        self.plotClusterItems[0].addToPlot(self.plot);
         
        self.plotVBox.autoRange();
        self.viewValid=True;
        
    
    def addCluster(self):
        if(not self.closedBound or (not self.dataValid) or (not self.viewValid)):
            return;

        viewChs=[hChSel, vChSel];
        viewParams=[hParamSel, vParamSel];
        clustBound=Boundary(self.boundPoints[0, :], self.boundPoints[1, :],
                            viewChs, viewParams);
                            
        pointsBA=clustBound.calcPointsInBoundary(self.data.getChParam(self.xChN, self.xParamT),
                                                 self.data.getChParam(self.yChN, self.yParamT));
                                                 
        clusterPointsBA=pointsBA & self.clusters[self.workClustN].getSelectArray();
        
        curCluster=Cluster(self.data, [clustBound], clusterPointsBA);
        self.clusters.append(curCluster);
        self.plotClusterItems.append(ClusterPlotItem(curCluster));
        
        self.initBound();
    
    def plotMouseClicked(self, evt):
        numPoints=self.boundPoints.shape[1];
        if(evt[0].button()==Qt.MouseButton.RightButton):
            if(numPoints<3):
                return;
            
            self.boundPoints=np.hstack((self.boundPoints, 
                                        [[self.boundPoints[0, -1]], [self.boundPoints[1, -1]]]));
            self.closedBound=True;
            return;
        
        pos=evt[0].scenePos();
        mousePoint=self.plotVBox.mapSceneToView(pos);
        
        point=[[mousePoint.x()], [mousePoint.y()]];
        self.boundPoints=np.hstack((self.boundPoints, point));
        
        self.boundPlotItem.setData(x=self.boundPoints[0, :], y=self.boundPoints[1, :]);
        self.drawBound=True;
            
    def plotMouseMoved(self, evt):
        pos=evt[0];
        if((not self.plot.sceneBoundingRect().contains(pos)) 
           or (not self.drawBound) or (self.closedBound)):
            return;
        
        mousePoint=self.plotVBox.mapSceneToView(pos);
        self.curMousePos[0]=mousePoint.x();
        self.curMousePos[1]=mousePoint.y();
        self.movingBoundItem.setData(x=[self.boundPoints[0, -1], mousePoint.x()],
                                     y=[self.boundPoints[1, -1], mousePoint.y()]);

    
    
    
