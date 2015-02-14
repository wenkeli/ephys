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
    def __init__(self, cluster, plot, pen=None):
        self.cluster=cluster;
        if(pen==None):
            self.pen=pg.mkPen("w");
        else:
            self.pen=pen;
#         self.plotData=pg.ScatterPlotItem(x=[0, 1], y=[0, 1],
#                                       symbol="s", pen=pg.mkPen("w"),
#                                       size=1);
        self.plotData=fscatter.FastScatterPlotItem(x=[0], y=[0],
                                      symbol="s", pen=self.pen,
                                      size=1, pointMode=True);
        self.plotBoundaryData=pg.PlotDataItem(x=[0], y=[0], pen=self.pen);     
        self.plot=plot;
        
    
    def setPlotData(self, xChN, yChN, xChParamT, yChParamT):
        self.plotData.setData(x=self.cluster.getParam(xChN, xChParamT),
                              y=self.cluster.getParam(yChN, yChParamT),
                              symbol="s", pen=self.pen,
                              size=1, pointMode=True);
        boundaries=self.cluster.getBoundaries([xChN, yChN], [xChParamT, yChParamT]);
        if(len(boundaries)>0):
            points=boundaries[0].getPoints();
            self.plotBoundaryData.setData(x=points[0, :], y=points[1, :]);
        else:
            self.plotBoundaryData.setData(x=[0], y=[0]);
                              
    def addToPlot(self):
        self.plot.addItem(self.plotData);
        self.plot.addItem(self.plotBoundaryData);
        
    def removeFromPlot(self):
        self.plot.removeItem(self.plotData);
        self.plot.removeItem(self.plotBoundaryData);
        


class MainW(QMainWindow, Ui_MainW):
    def __init__(self, app, parent=None):
        super(MainW, self).__init__(parent);
        self.setupUi(self);
        self.enableViewUI(False);
        self.enableClusterUI(False);
        self.setFocusPolicy(Qt.StrongFocus);
        self.setWindowFlags(Qt.CustomizeWindowHint
                            | Qt.WindowMinimizeButtonHint);
                            
        self.app=app;
        screenSize=QApplication.desktop().availableGeometry(self);
        sh=screenSize.height();
        sw=screenSize.width();
        
        cpw=self.geometry().width();
        self.move(sw-cpw, 0);
        self.plotW=GraphicsLayoutWidget();
        self.plotW.resize(sw-cpw-25, sh);
        self.plotW.move(0, 0);
#         self.plotW.resize(1500, 1000);
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
        
        self.keyShortcuts=dict();
        self.setupKeyShortcuts(self);
        self.setupKeyShortcuts(self.plotW);
        self.enableKeyShortcuts(False);
        
        self.hChList=[];
        self.vChList=[];
        self.hParamList=[];
        self.vParamList=[];
        self.selectDataRole=0;
        self.hChN=None;
        self.vChN=None;
        self.hParamT=None;
        self.vParamT=None;
        self.workClustList=dict();
        self.viewClustList=dict();
        self.viewValid=False;
        self.pens=[];
        self.curPenInd=0;
        self.setupPens();
        
        self.boundPoints=[];
        self.drawMovingBound=False;
        self.closedBound=False;
        self.boundPlotItem=None;
        self.movingBoundItem=None;
        self.proxyConList=[];
        self.curMousePos=np.zeros(2, dtype="float32");
        self.initBound();
        
        self.dataDir="";
        self.data=None;
        self.clusters=dict();
        self.parentClustIDs=dict();
        self.plotClusterItems=dict();
        self.maxClustN=0;
        self.maxClustID="";
        self.workClustID="";
        self.initClustID="";
        self.dataValid=False;


    def setupPens(self):
        self.pens.append(pg.mkPen(pg.mkColor("#FF4444"))); #red
        self.pens.append(pg.mkPen(pg.mkColor("#4444FF"))); #blue
        self.pens.append(pg.mkPen(pg.mkColor("#44FF44"))); #green
        self.pens.append(pg.mkPen(pg.mkColor("#FF00FF"))); #magenta
        self.pens.append(pg.mkPen(pg.mkColor("#00FFFF"))); #cyan
        self.pens.append(pg.mkPen(pg.mkColor("#FFFF00"))); #yellow
        self.pens.append(pg.mkPen(pg.mkColor("#9370DB"))); #medium purple
        self.pens.append(pg.mkPen(pg.mkColor("#FF69B4"))); #hot pink
        self.pens.append(pg.mkPen(pg.mkColor("#CD853F"))); #Peru
        self.pens.append(pg.mkPen(pg.mkColor("#8A2BE2"))); #blue violet
        
    def getPen(self):
        curPen=self.pens[self.curPenInd];
        self.curPenInd=(self.curPenInd+1)%len(self.pens);
        return curPen;  

    def initBound(self):
        self.boundPoints=np.zeros((2, 0));
        self.drawMovingBound=False;
        self.closedBound=False;
        
        if((self.boundPlotItem==None) or (self.movingBoundItem==None)):
            self.boundPlotItem=pg.PlotDataItem(x=[0], y=[0], pen="w");
            self.movingBoundItem=pg.PlotDataItem(x=[0], y=[0], pen="w");
        else:
            self.boundPlotItem.setData(x=[0], y=[0]);
            self.movingBoundItem.setData(x=[0], y=[0]);
            
        self.plot.addItem(self.boundPlotItem);
        self.plot.addItem(self.movingBoundItem);
            
        if(len(self.proxyConList)<=0):
            self.proxyConList.append(pg.SignalProxy(self.plot.scene().sigMouseClicked, 
                                                    rateLimit=100, 
                                                    slot=self.plotMouseClicked));
            self.proxyConList.append(pg.SignalProxy(self.plot.scene().sigMouseMoved,
                                                    rateLimit=100, slot=self.plotMouseMoved));
        

    def enableViewUI(self, enable):
        self.saveFileButton.setEnabled(enable);
        
        self.hChannelSelect.setEnabled(enable);
        self.hParamSelect.setEnabled(enable);
        
        self.vChannelSelect.setEnabled(enable);
        self.vParamSelect.setEnabled(enable);
        
        self.workClusterSelect.setEnabled(enable);
        self.viewClustersSelect.setEnabled(enable);
        
        self.viewButton.setEnabled(enable);
        
        
    def enableClusterUI(self, enable):
        self.addButton.setEnabled(enable);
        self.copyButton.setEnabled(enable);
        self.refineButton.setEnabled(enable);
        self.deleteButton.setEnabled(enable);
        
    def invalidateView(self):
        self.viewValid=False;
        self.enableClusterUI(False);
        
    def validateView(self):
        self.viewValid=True;
        self.enableClusterUI(True);
        

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
        
        self.clearSelect();
        print("calculating parameters");
        self.data=SamplesData(data["waveforms"], data["gains"], data["thresholds"], data["timestamps"], None);
        print("done");

        self.populateSelect();
        self.addToClusterList(False, False);
        self.initClustID=self.workClustID;
        
        self.initBound();
        self.enableViewUI(True);
        self.enableClusterUI(False);
        self.enableKeyShortcuts(True);
        self.dataValid=True;
        self.viewValid=False;
        
        del(data);
        
        
    def addToClusterList(self, copy, useParent, clustBounds=[], pointsBA=[], pen=None):
        self.maxClustID=str(self.maxClustN);
        if(useParent):
            self.clusters[self.maxClustID]=Cluster(self.data, self.clusters[self.workClustID],
                                                   clustBounds, pointsBA);
            self.parentClustIDs[self.maxClustID]=self.workClustID;
        else:
            self.clusters[self.maxClustID]=Cluster(self.data, None,
                                                   clustBounds, pointsBA);
            self.parentClustIDs[self.maxClustID]=None;
                                                   
        self.plotClusterItems[self.maxClustID]=ClusterPlotItem(self.clusters[self.maxClustID], 
                                                               self.plot, pen);
        
        self.workClustList[self.maxClustID]=QListWidgetItem(str(self.maxClustID));
        self.workClustList[self.maxClustID].setData(self.selectDataRole, self.maxClustID);
        self.workClusterSelect.addItem(self.workClustList[self.maxClustID]);
        
        self.viewClustList[self.maxClustID]=QListWidgetItem(str(self.maxClustID));
        self.viewClustList[self.maxClustID].setData(self.selectDataRole, self.maxClustID);
        self.viewClustersSelect.addItem(self.viewClustList[self.maxClustID]);
        
        if((len(pointsBA)>0) and (not copy) and self.workClustID!=""):
            self.clusters[self.workClustID].removeSelect(pointsBA);
        
        self.workClustID=self.maxClustID;
        
        selWorkClust=self.workClusterSelect.selectedItems();
        self.workClustList[self.workClustID].setSelected(True);
        if(len(selWorkClust)>0):
            selWorkClust[0].setSelected(False);
        self.changeWorkCluster();
        
        self.maxClustN=self.maxClustN+1;
    
        
    def removeFromClusterList(self, ind):
        if(ind==self.initClustID):
            return;
            
        row=self.workClusterSelect.row(self.workClustList[ind]);
        self.workClusterSelect.takeItem(row);
        del(self.workClustList[ind]);
        
        row=self.viewClustersSelect.row(self.viewClustList[ind]);
        self.viewClustersSelect.takeItem(row);
        del(self.viewClustList[ind]);
        
        del(self.plotClusterItems[ind]);
        
        
        for k in self.parentClustIDs.keys():
            if(self.parentClustIDs[k]==ind):
                self.parentClustIDs[k]=self.parentClustIDs[ind];
                if(self.parentClustIDs[k]!=None):
                    self.clusters[k].setParentClust(self.clusters[self.parentClustIDs[k]]);
                else:
                    self.clusters[k].setParentClust(None);
        
        
        if(self.parentClustIDs[ind]!=None):
            self.workClustID=self.parentClustIDs[ind];
        else:
            self.workClustID=self.initClustID;
            self.clusters[self.initClustID].addSelect(self.clusters[ind].getSelectArray());
            
        del(self.parentClustIDs[ind]);
        
        del(self.clusters[ind]);
        
        self.workClustList[self.workClustID].setSelected(True);
        self.changeWorkCluster();

        
    def clearSelect(self):
        self.hChannelSelect.clear();
        self.hChList[:]=[];
        self.hParamSelect.clear();
        self.hParamList[:]=[];
        self.vChannelSelect.clear();
        self.vChList[:]=[];
        self.vParamSelect.clear();
        self.vParamList[:]=[];
        self.workClusterSelect.clear();
        self.workClustList.clear();
        self.viewClustersSelect.clear();
        self.viewClustList.clear();
    
    def populateSelect(self):
        numChannels=self.data.getNumChannels();
        self.hChList=[None]*numChannels;
        self.vChList=[None]*numChannels;
        for i in np.r_[0:numChannels]:
            self.hChList[i]=QListWidgetItem(str(i));
            self.hChList[i].setData(self.selectDataRole, i);
            self.hChannelSelect.addItem(self.hChList[i]);
            
            self.vChList[i]=QListWidgetItem(str(i));
            self.vChList[i].setData(self.selectDataRole, i);
            self.vChannelSelect.addItem(self.vChList[i]);
            
        paramKeys=self.data.getChParamTypes();
        numParams=len(paramKeys);
        self.hParamList=[None]*numParams;
        self.vParamList=[None]*numParams;
        for i in np.r_[0:numParams]:
            self.hParamList[i]=QListWidgetItem(paramKeys[i]);
            self.hParamList[i].setData(self.selectDataRole, paramKeys[i]);
            self.hParamSelect.addItem(self.hParamList[i]);
            
            self.vParamList[i]=QListWidgetItem(paramKeys[i]);
            self.vParamList[i].setData(self.selectDataRole, paramKeys[i]);
            self.vParamSelect.addItem(self.vParamList[i]);
            
        
    def setupKeyShortcuts(self, widget):
        widgetName=widget.objectName();
        self.keyShortcuts[widgetName]=[];
        
        self.keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("V")),
                                                       widget, self.updatePlotView));
        self.keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("D")),
                                                       widget, self.deleteCluster));
        self.keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("R")),
                                                       widget, self.refineCluster));
        self.keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("A")),
                                                       widget, self.addCluster));
        self.keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("C")),
                                               widget, self.copyCluster));                                                       
                                          
        
    def enableKeyShortcuts(self, enable):
        keys=self.keyShortcuts.keys();
        
        for i in keys:
            numKeys=len(self.keyShortcuts[i]);            
            for j in np.r_[0:numKeys]:
                self.keyShortcuts[i][j].setEnabled(enable);
                
                
    def updatePlotView(self):
        if(not self.dataValid):
            return;
        hChSel=self.hChannelSelect.selectedItems();
        vChSel=self.vChannelSelect.selectedItems();
        hParamSel=self.hParamSelect.selectedItems();
        vParamSel=self.vParamSelect.selectedItems();
        
        self.plot.clear();
        self.initBound();
        
        if((len(hChSel)==0) or (len(vChSel)==0) or (len(hParamSel)==0) or (len(vParamSel)==0)):
            return;
        self.hChN=hChSel[0].data(self.selectDataRole);
        self.vChN=vChSel[0].data(self.selectDataRole);
        self.hParamT=hParamSel[0].data(self.selectDataRole);
        self.vParamT=vParamSel[0].data(self.selectDataRole);

        self.viewClustList[self.workClustID].setSelected(True);
        viewClustItems=self.viewClustersSelect.selectedItems();
        for item in viewClustItems:
            clustID=item.data(self.selectDataRole);        
            self.plotClusterItems[clustID].setPlotData(self.hChN, self.vChN, self.hParamT, self.vParamT);
            self.plotClusterItems[clustID].addToPlot();
         
        self.plotVBox.autoRange();
        self.validateView();
        
    
    def calcPointsInBound(self):
        viewChs=[self.hChN, self.vChN];
        viewParams=[self.hParamT, self.vParamT];
        clustBound=Boundary(self.boundPoints[0, :], self.boundPoints[1, :],
                            viewChs, viewParams);                            
        pointsBA=clustBound.calcPointsInBoundary(self.data.getChParam(self.hChN, self.hParamT),
                                                 self.data.getChParam(self.vChN, self.vParamT));                                             
        clusterPointsBA=pointsBA & self.clusters[self.workClustID].getSelectArray();
        self.initBound();
        return (clustBound, clusterPointsBA);
        
    def addClustCommon(self, copy):
        if((not self.closedBound) or (not self.dataValid) or (not self.viewValid)):
            return;
        (clustBound, clusterPointsBA)=self.calcPointsInBound();
        if(np.sum(clusterPointsBA)>0):
            self.addToClusterList(copy, True, [clustBound], clusterPointsBA, self.getPen());
        self.updatePlotView();
    
    def addCluster(self):
        self.addClustCommon(False);
    
    def copyCluster(self):
        self.addClustCommon(True);
    
    def deleteCluster(self):
        if((not self.dataValid) or (not self.viewValid)):
            return;
        self.removeFromClusterList(self.workClustID);
        self.updatePlotView();
        
        
    
    def refineCluster(self):
        if((not self.closedBound) or (not self.dataValid) or (not self.viewValid)):
            return;
        if(self.workClustID==self.initClustID):
            return;
        
        viewChs=[self.hChN, self.vChN];
        viewParams=[self.hParamT, self.vParamT];
        clustBound=Boundary(self.boundPoints[0, :], self.boundPoints[1, :],
                            viewChs, viewParams);
                            
        self.clusters[self.workClustID].addBoundary(clustBound);
        clusterPointsBA=clustBound.calcPointsInBoundary(self.data.getChParam(self.hChN, self.hParamT),
                                                        self.data.getChParam(self.vChN, self.vParamT));
        retPoints=self.clusters[self.workClustID].modifySelect(clusterPointsBA);
        self.initBound();
        self.updatePlotView();
        
        
    def changeWorkCluster(self):
        selectItem=self.workClusterSelect.selectedItems();
        self.workClustID=selectItem[0].data(self.selectDataRole);
        self.viewClustersSelect.clearSelection();
        self.viewClustList[self.workClustID].setSelected(True);

    
    def plotMouseClicked(self, evt):
#         print(str(self.closedBound)+" "+str(self.drawMovingBound));
        if((not self.viewValid) or (self.closedBound)):
            return;
        numPoints=self.boundPoints.shape[1];
        if(evt[0].button()==Qt.MouseButton.RightButton):
            if(numPoints<3):
                return;
            
            self.boundPoints=np.hstack((self.boundPoints, 
                                        [[self.boundPoints[0, 0]], [self.boundPoints[1, 0]]]));
            self.boundPlotItem.setData(x=self.boundPoints[0, :], y=self.boundPoints[1, :]);
            self.movingBoundItem.setData(x=[0], y=[0]);
            
            self.closedBound=True;
            self.drawMovingBound=False;
            return;
        
        pos=evt[0].scenePos();
        mousePoint=self.plotVBox.mapSceneToView(pos);
        
        point=[[mousePoint.x()], [mousePoint.y()]];
        self.boundPoints=np.hstack((self.boundPoints, point));
        self.boundPlotItem.setData(x=self.boundPoints[0, :], y=self.boundPoints[1, :]);
        
        self.drawMovingBound=True;
        self.closedBound=False;
        
            
    def plotMouseMoved(self, evt):
        if(not self.viewValid):
            return;
        pos=evt[0];
        if((not self.plot.sceneBoundingRect().contains(pos)) 
           or (not self.drawMovingBound) or (self.closedBound)):
            return;
        
        mousePoint=self.plotVBox.mapSceneToView(pos);
        self.curMousePos[0]=mousePoint.x();
        self.curMousePos[1]=mousePoint.y();
        self.movingBoundItem.setData(x=[self.boundPoints[0, -1], mousePoint.x()],
                                     y=[self.boundPoints[1, -1], mousePoint.y()]);

    
    
    
