import os;

import numpy as np;

import PySide;

from PySide.QtGui import QMainWindow, QApplication;
from PySide.QtGui import QAbstractItemView, QListWidget, QListWidgetItem;
from PySide.QtGui import QKeySequence, QKeySequence, QShortcut, QFileDialog;
from PySide.QtGui import QBrush, QColor;

from PySide.QtCore import Qt, QRect;

import pyqtgraph as pg;
from pyqtgraph.widgets.GraphicsLayoutWidget import GraphicsLayoutWidget;

from mainw_ui import Ui_MainW;
from reportw import ReportW;

import FastScatterPlotItem as fscatter;

from ..fileIO.loadOpenEphysSpikes import readSamples;

from ..data.samples import SamplesData;
from ..data.samples import SamplesClustCount;
from ..data.cluster import Cluster, Boundary;

from ..data.dataset import DataSet;

class ClusterPlotItem(object):
    def __init__(self, cluster, plot, pen=None):
        self.__cluster=cluster;
        self.__numSelPoints=None;
        
        self.__calcNumSelPoints();
        if(pen==None):
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
        
    
    def setPlotData(self, xChN, yChN, xChParamT, yChParamT):
        self.__plotData.setData(x=self.__cluster.getParam(xChN, xChParamT),
                              y=self.__cluster.getParam(yChN, yChParamT),
                              symbol="s", pen=self.__pen,
                              size=1, pointMode=True);
        self.__calcNumSelPoints();
        
        boundaries=self.__cluster.getBoundaries([xChN, yChN], [xChParamT, yChParamT]);
        if(len(boundaries)>0):
            points=boundaries[0].getPoints();
            self.__plotBoundaryData.setData(x=points[0, :], y=points[1, :]);
        else:
            self.__plotBoundaryData.setData(x=[0], y=[0]);
                              
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
        
    def getSelPointsByRange(self, startInd, endInd):
        sBA=self.__cluster.getSelectArray();
        return sBA & ((self.__numSelPoints>=startInd) & (self.__numSelPoints<endInd));
    
    def getTotalSelPoints(self):
        return self.__numSelPoints[-1];
        
        

class MainW(QMainWindow, Ui_MainW):
    def __init__(self, app, parent=None):
        super(MainW, self).__init__(parent);
        self.setupUi(self);
        self.enableViewUI(False);
        self.enableClusterUI(False);
        self.setFocusPolicy(Qt.StrongFocus);
        self.setWindowFlags(Qt.CustomizeWindowHint
                            | Qt.WindowMinimizeButtonHint);
                            
        self.__dataDir="";
        self.__dataSet=None;
        self.__plotClusterItems=dict();
        self.__dataValid=False;
                            
        self.__app=app;
        screenSize=QApplication.desktop().availableGeometry(self);
        sh=screenSize.height();
        sw=screenSize.width();
        
        self.__reportW=ReportW();
        self.__reportDisp=self.__reportW.getReportDisp();
        
        cpw=self.geometry().width();
        self.move(sw-cpw, 0);
        
        self.__plotW=GraphicsLayoutWidget();
        self.__plotW.resize(sw-cpw-25, sh);
        self.__plotW.move(0, 0);
#         self.__plotW.resize(1500, 1000);
        self.__plotW.setFocusPolicy(Qt.StrongFocus);
        self.__plotW.setObjectName("plotWindow");
        self.__plotW.setWindowFlags(Qt.CustomizeWindowHint
                                    | Qt.WindowMinimizeButtonHint);
        self.__plotW.show();
        
        self.__plot=self.__plotW.addPlot(0, 0, 1, 1, enableMenu=False);
#         self.__plotW.ci.layout.setColumnMaximumWidth(1, 25);
        
        self.__plotScene=self.__plot.scene();
        self.__plotScene.setMoveDistance(200);
        
        self.__plotVBox=self.__plot.getViewBox();
        self.__plotVBox.setMouseMode(pg.ViewBox.RectMode);
        self.__plotVBox.disableAutoRange();
        
        self.__wavePlotLayout=self.__plotW.addLayout(0, 1, 1, 1);
        self.__plotW.ci.layout.setColumnStretchFactor(0, 80);
        self.__plotW.ci.layout.setColumnStretchFactor(1, 20);
        self.__wavePlots=[];
        self.__waveStartInd=0;
        
        self.__keyShortcuts=dict();
        self.__setupKeyShortcuts(self);
        self.__setupKeyShortcuts(self.__plotW);
        self.__setupKeyShortcuts(self.__reportW);
        self.enableKeyShortcuts(False);
        
        self.__hChList=[];
        self.__vChList=[];
        self.__hParamList=[];
        self.__vParamList=[];
        self.__selectDataRole=0;
        self.__hChN=None;
        self.__vChN=None;
        self.__hParamName=None;
        self.__vParamName=None;
        self.__workClustList=dict();
        self.__viewClustList=dict();
        self.__viewValid=False;
        self.__colors=[];
        self.__pens=[];
        self.__brushes=[];
        self.__curColorInd=0;
        self.__setupPens();
        
        self.__boundPoints=[];
        self.__drawMovingBound=False;
        self.__closedBound=False;
        self.__boundPlotItem=None;
        self.__movingBoundItem=None;
        self.__proxyConList=[];
        self.__curMousePos=np.zeros(2, dtype="float32");
        self.__initBound();
        


    def __setupPens(self):
        self.__colors.append(pg.mkColor("#FF4444")); #red
        self.__colors.append(pg.mkColor("#4444FF")); #blue
        self.__colors.append(pg.mkColor("#44FF44")); #green
        self.__colors.append(pg.mkColor("#FF00FF")); #magenta
        self.__colors.append(pg.mkColor("#00FFFF")); #cyan
        self.__colors.append(pg.mkColor("#FFFF00")); #yellow
        self.__colors.append(pg.mkColor("#9370DB")); #medium purple
        self.__colors.append(pg.mkColor("#FF69B4")); #hot pink
        self.__colors.append(pg.mkColor("#CD853F")); #Peru
        self.__colors.append(pg.mkColor("#8A2BE2")); #blue violet
        
        for i in self.__colors:
            self.__pens.append(pg.mkPen(i));
            brushColor=QColor(i);
            brushColor.setAlphaF(0.8);
            self.__brushes.append(QBrush(brushColor));
        
    def getCurColor(self):
        curPen=self.__pens[self.__curColorInd];
        curColor=self.__colors[self.__curColorInd];
        curBrush=self.__brushes[self.__curColorInd];
        
        self.__curColorInd=(self.__curColorInd+1)%len(self.__pens);
        return (curColor, curPen, curBrush);  

    def __initBound(self):
        self.__boundPoints=np.zeros((2, 0));
        self.__drawMovingBound=False;
        self.__closedBound=False;
        
        if(self.__dataValid):
            workClustID=self.__dataSet.getWorkClustID();
            drawPen=self.__plotClusterItems[workClustID].getCurPen();
        else:
            drawPen="w";
        
        if((self.__boundPlotItem==None) or (self.__movingBoundItem==None)):
            self.__boundPlotItem=pg.PlotDataItem(x=[0], y=[0], pen=drawPen);
            self.__movingBoundItem=pg.PlotDataItem(x=[0], y=[0], pen=drawPen);
        else:
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
        

    def enableViewUI(self, enable):
        self.saveFileButton.setEnabled(enable);
        
        self.hChannelSelect.setEnabled(enable);
        self.hParamSelect.setEnabled(enable);
        
        self.vChannelSelect.setEnabled(enable);
        self.vParamSelect.setEnabled(enable);
        
        self.workClusterSelect.setEnabled(enable);
        self.viewClustersSelect.setEnabled(enable);
        
        self.viewButton.setEnabled(enable);
        self.reportClusterButton.setEnabled(enable);
        
        
    def enableClusterUI(self, enable):
        self.addButton.setEnabled(enable);
        self.copyButton.setEnabled(enable);
        self.refineButton.setEnabled(enable);
        self.deleteButton.setEnabled(enable);
        self.nextWavesButton.setEnabled(enable);
        self.prevWavesButton.setEnabled(enable);
        self.clearWavePlotsButton.setEnabled(enable);

        
    def invalidateView(self):
        self.__viewValid=False;
        self.enableClusterUI(False);
        
    def validateView(self):
        self.__viewValid=True;
        self.enableClusterUI(True);
        

    def quit(self):
        self.__app.closeAllWindows();
        
    def loadFile(self):
        print("loading file");
        fileName=QFileDialog.getOpenFileName(self, self.tr("open spike file"), 
                                             self.tr(self.__dataDir), 
                                             self.tr("spike files (*.spikes)"));
        fileName=fileName[0];
        if(fileName==""):
            return;
        
        self.__dataDir=os.path.dirname(fileName);
        
        file=open(fileName, "rb");
        fileStat=os.stat(fileName);        
        data=readSamples(file, fileStat.st_size, 1024, "=Bq3H", "H", "H", 2, "H", 3, 4);
        file.close();
        
        self.clearSelect();
        print("calculating parameters");
        self.__dataSet=DataSet(data["waveforms"], data["gains"], data["thresholds"],
                               data["timestamps"], None);
        print("done");
        
        (clustID, cluster)=self.__dataSet.initializeWorkingSet();
        self.__addClusterToView(clustID, cluster);
        self.populateSelect();
        
        self.__initBound();
        self.enableViewUI(True);
        self.enableClusterUI(False);
        self.enableKeyShortcuts(True);
        self.__dataValid=True;
        self.__viewValid=False;
        
        del(data);
        
        numWavePlots=len(self.__wavePlots);
        if(numWavePlots>0):
            for i in np.r_[0:numWavePlots]:
                self.__wavePlotLayout.removeItem(self.__wavePlots[i]);
                del(self.__wavePlots[i]);
            self.__wavePlots=[];
        
        numChannels=self.__dataSet.getSamples().getNumChannels();
        for i in np.r_[0:numChannels]:
            wavePlot=self.__wavePlotLayout.addPlot(i, 0, enableMenu=False);
            self.__wavePlots.append(wavePlot);
            
        self.__waveStartInd=0;
            
        
    def __addClusterToView(self, clustID, cluster, pen=None, brush=None):
        self.__plotClusterItems[clustID]=ClusterPlotItem(cluster, self.__plot, pen);
        
        self.__workClustList[clustID]=QListWidgetItem(clustID);
        self.__workClustList[clustID].setData(self.__selectDataRole, clustID);
        if(brush!=None):
            self.__workClustList[clustID].setBackground(brush);
        self.workClusterSelect.addItem(self.__workClustList[clustID]);
        
        self.__viewClustList[clustID]=QListWidgetItem(clustID);
        self.__viewClustList[clustID].setData(self.__selectDataRole, clustID);
        if(brush!=None):
            self.__viewClustList[clustID].setBackground(brush);
        self.viewClustersSelect.addItem(self.__viewClustList[clustID]);
        self.__viewClustList[clustID].setSelected(True);
        
        workClustID=self.__dataSet.getWorkClustID();
        if(not (self.__workClustList[workClustID].isSelected())):
            self.__workClustList[workClustID].setSelected(True);
            self.changeWorkCluster();
    
        
    def __removeCluster(self, ind):
        (success, workClustID)=self.__dataSet.deleteCluster(ind);
        
        if(not success):
            return;
        
        row=self.workClusterSelect.row(self.__workClustList[ind]);
        self.workClusterSelect.takeItem(row);
        del(self.__workClustList[ind]);
        
        row=self.viewClustersSelect.row(self.__viewClustList[ind]);
        self.viewClustersSelect.takeItem(row);
        del(self.__viewClustList[ind]);
        
        del(self.__plotClusterItems[ind]);
        
        self.__workClustList[workClustID].setSelected(True);
        self.changeWorkCluster();

        
    def clearSelect(self):
        self.hChannelSelect.clear();
        self.__hChList[:]=[];
        self.hParamSelect.clear();
        self.__hParamList[:]=[];
        self.vChannelSelect.clear();
        self.__vChList[:]=[];
        self.vParamSelect.clear();
        self.__vParamList[:]=[];
        self.workClusterSelect.clear();
        self.__workClustList.clear();
        self.viewClustersSelect.clear();
        self.__viewClustList.clear();
    
    def populateSelect(self):
        numChannels=self.__dataSet.getSamples().getNumChannels();
        self.__hChList=[None]*numChannels;
        self.__vChList=[None]*numChannels;
        for i in np.r_[0:numChannels]:
            self.__hChList[i]=QListWidgetItem(str(i));
            self.__hChList[i].setData(self.__selectDataRole, i);
            self.hChannelSelect.addItem(self.__hChList[i]);
            
            self.__vChList[i]=QListWidgetItem(str(i));
            self.__vChList[i].setData(self.__selectDataRole, i);
            self.vChannelSelect.addItem(self.__vChList[i]);
            
        paramNames=self.__dataSet.getSamples().getParamNames();
        
        ignoredParamNames=["peakTime", "valleyTime", "PVWidth"];
        
        modParamNames=[];
        if("peak" in paramNames):
            modParamNames.append("peak");
        if("valley" in paramNames):
            modParamNames.append("valley");
        if("peakAngle" in paramNames):
            modParamNames.append("peakAngle");
        if("time" in paramNames):
            modParamNames.append("time");
        
        for i in paramNames:
            if(i in ignoredParamNames):
                continue;
            if(i in modParamNames):
                continue;
            modParamNames.append(i);
        
        numParams=len(modParamNames);
        self.__hParamList=[None]*numParams;
        self.__vParamList=[None]*numParams;
        for i in np.r_[0:numParams]:
            self.__hParamList[i]=QListWidgetItem(modParamNames[i]);
            self.__hParamList[i].setData(self.__selectDataRole, modParamNames[i]);
            self.hParamSelect.addItem(self.__hParamList[i]);
            
            self.__vParamList[i]=QListWidgetItem(modParamNames[i]);
            self.__vParamList[i].setData(self.__selectDataRole, modParamNames[i]);
            self.vParamSelect.addItem(self.__vParamList[i]);
            
        
    def __setupKeyShortcuts(self, widget):
        widgetName=widget.objectName();
        self.__keyShortcuts[widgetName]=[];
        
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("V")),
                                                       widget, self.updatePlotView));
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("D")),
                                                       widget, self.deleteCluster));
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("F")),
                                                       widget, self.refineCluster));
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("A")),
                                                       widget, self.addCluster));
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("C")),
                                               widget, self.copyCluster));
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("R")),
                                               widget, self.showReport));                                                               
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("Q")),
                                               widget, self.drawPrevWaves));
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("W")),
                                               widget, self.drawNextWaves));
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("E")),
                                               widget, self.clearWavePlots));        
                                          
        
    def enableKeyShortcuts(self, enable):
        keys=self.__keyShortcuts.keys();
        
        for i in keys:
            numKeys=len(self.__keyShortcuts[i]);            
            for j in np.r_[0:numKeys]:
                self.__keyShortcuts[i][j].setEnabled(enable);
                
                
    def updatePlotView(self):
        if(not self.__dataValid):
            return;
        hChSel=self.hChannelSelect.selectedItems();
        vChSel=self.vChannelSelect.selectedItems();
        hParamSel=self.hParamSelect.selectedItems();
        vParamSel=self.vParamSelect.selectedItems();
        
        self.__plot.clear();
        self.__initBound();
        
        if((len(hChSel)==0) or (len(vChSel)==0) or (len(hParamSel)==0) or (len(vParamSel)==0)):
            return;
        self.__hChN=hChSel[0].data(self.__selectDataRole);
        self.__vChN=vChSel[0].data(self.__selectDataRole);
        self.__hParamName=hParamSel[0].data(self.__selectDataRole);
        self.__vParamName=vParamSel[0].data(self.__selectDataRole);

        workClustID=self.__dataSet.getWorkClustID();
        self.__viewClustList[workClustID].setSelected(True);
        self.__workClustList[workClustID].setSelected(True);
        viewClustItems=self.viewClustersSelect.selectedItems();
        for item in viewClustItems[::-1]:
            clustID=item.data(self.__selectDataRole);        
            self.__plotClusterItems[clustID].setPlotData(self.__hChN, self.__vChN, self.__hParamName, self.__vParamName);
            self.__plotClusterItems[clustID].addToPlot();
         
        self.__plotVBox.autoRange();
        self.validateView();
        
        
    def addClustCommon(self, copy):
        if((not self.__closedBound) or (not self.__dataValid) or (not self.__viewValid)):
            return;
        (clustID, cluster)=self.__dataSet.addCluster(copy, self.__hChN, self.__vChN,
                                  self.__hParamName, self.__vParamName,
                                  self.__boundPoints[0, :], self.__boundPoints[1, :]);
        if(clustID!=None):
            (color, pen, brush)=self.getCurColor();
            self.__addClusterToView(clustID, cluster, pen, brush);

        self.__initBound();
        self.updatePlotView();
    
    def addCluster(self):
        self.addClustCommon(False);
    
    def copyCluster(self):
        self.addClustCommon(True);
    
    def deleteCluster(self):
        if((not self.__dataValid) or (not self.__viewValid)):
            return;
        workClustID=self.__dataSet.getWorkClustID();
        self.__removeCluster(workClustID);
        self.updatePlotView();
       
    
    def refineCluster(self):
        if((not self.__closedBound) or (not self.__dataValid) or (not self.__viewValid)):
            return;
        
        viewChs=[self.__hChN, self.__vChN];
        viewParams=[self.__hParamName, self.__vParamName];
        
        self.__dataSet.refineCluster(self.__hChN, self.__vChN, 
                                     self.__hParamName, self.__vParamName,
                                     self.__boundPoints[0, :], self.__boundPoints[1, :]);
        
        self.__initBound();
        self.updatePlotView();
        
        
    def changeWorkCluster(self):
        selectItem=self.workClusterSelect.selectedItems();
        workClustID=selectItem[0].data(self.__selectDataRole);
        self.__viewClustList[workClustID].setSelected(True);
        self.__dataSet.setWorkClustID(workClustID);
        self.updatePlotView();
        
        self.__waveStartInd=0;
        
    def showReport(self):
        if(self.__reportW.isVisible()):
            self.__reportW.hide();
        else:
            self.__reportW.show();
            self.generateReport();
            
    def generateReport(self):
        self.__reportDisp.clear();
#         self.__reportDisp.insertPlainText("testtesttest1234test1234\n");
#         self.__reportDisp.insertPlainText("\ttest1\n");
        clustInds=self.__dataSet.getClusterInds();
        initClustID=self.__dataSet.getInitClustID();
        clustInds.remove(initClustID);
        
        for i in clustInds:
            (numPoints, numOverlap)=self.__dataSet.computeClusterOverlap(i);
            percOverlap=numOverlap/float(numPoints)*100;
            output="cluster "+str(i)+": "+str(numPoints)+" samples, overlap: "+str(numOverlap)+" samples, "+str(percOverlap)+"%\n";
            self.__reportDisp.insertPlainText(output);
            for j in clustInds:
                if(i==j):
                    continue;
                (numPoints, numOverlap)=self.__dataSet.compareClustersOverlap(i, j);
                percOverlap=numOverlap/float(numPoints)*100;
                if(numOverlap<=0):
                    continue;
                output="\toverlap cluster "+str(j)+": "+str(numOverlap)+" samples, "+str(percOverlap)+"%\n";
                self.__reportDisp.insertPlainText(output);
            self.__reportDisp.insertPlainText("\n");
            
    def drawPrevWaves(self):
        if((not self.__viewValid) or (not self.__dataValid)):
            return;
        self.__waveStartInd=self.__waveStartInd-100;
        if(self.__waveStartInd<0):
            self.__waveStartInd=0;
            
        self.__drawWavesCommon();
        
    def drawNextWaves(self):
        if((not self.__viewValid) or (not self.__dataValid)):
            return;
        self.__drawWavesCommon();
        workClustID=self.__dataSet.getWorkClustID();
        totalPoints=self.__plotClusterItems[workClustID].getTotalSelPoints();
        self.__waveStartInd=self.__waveStartInd+100;
        if(self.__waveStartInd+100>=totalPoints):
            self.__waveStartInd=totalPoints-100;
    
    def __drawWavesCommon(self):
        workClustID=self.__dataSet.getWorkClustID();
        drawPen=self.__plotClusterItems[workClustID].getCurPen();
        sBA=self.__plotClusterItems[workClustID].getSelPointsByRange(self.__waveStartInd, self.__waveStartInd+100);       
        for i in np.r_[0:len(self.__wavePlots)]:
            (nPts, waves, xval, connectArr)=self.__dataSet.getSamples().getWaveforms(sBA, i);
            self.__wavePlots[i].plot(xval.flatten(), waves.flatten(), pen=drawPen, connect=connectArr.flatten());

        
    def clearWavePlots(self):
        for i in np.r_[0:len(self.__wavePlots)]:
            self.__wavePlots[i].getViewBox().autoRange();
            self.__wavePlots[i].clear();
        
    
    def plotMouseClicked(self, evt):
#         print(str(self.__closedBound)+" "+str(self.__drawMovingBound));
        if((not self.__viewValid) or (self.__closedBound)):
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
        if(not self.__viewValid):
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

    
    
    
