import os;

import cPickle as pickle;

import h5py;

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

from ..fileIO.loadOpenEphysSpikes import readSpikeFile, readSamples;

from ..fileIO.exporthdf5 import exportToHDF5, exportToHDF5PerCluster;

from ..data.samples import SamplesData;
from ..data.samples import SamplesClustCount;
from ..data.cluster import Cluster, Boundary;

from ..data.dataset import DataSet;

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
        
        

class MainW(QMainWindow, Ui_MainW):
    def __init__(self, app, parent=None):
        super(MainW, self).__init__(parent);
        self.setupUi(self);
        self.enableViewUI(False);
        self.enableClusterUI(False);
        self.enableTimeSelectUI(False);
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
        self.numWavesIncBox.setMinimum(1);
        self.numWavesIncBox.setMaximum(1000000);
        self.numWavesIncBox.setValue(100);
        
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
        
        if((self.__boundPlotItem is None) or (self.__movingBoundItem is None)):
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
        
    def saveClusterData(self):
#         fileName=QFileDialog.getSaveFileName(self, self.tr("save cluster data set"), 
#                                              self.tr(os.path.join(self.__dataDir,self.__dataName+".clusterdataset")), 
#                                              self.tr("cluster data set (*.clusterdataset)"));
#         fileName=fileName[0];
#         if(fileName==""):
#             return;

        fileName=os.path.join(self.__dataDir,self.__dataName+".clusterdataset");
        
        file=open(fileName, "wb");
        pickle.dump(self.__dataSet, file, protocol=2);
        
        file.close();
        
    def exportData(self):
#         fileName=QFileDialog.getSaveFileName(self, self.tr("export cluster data"), 
#                                              self.tr(os.path.join(self.__dataDir, self.__dataName+".h5")), 
#                                              self.tr("1. individual clusters HDF5 (*.h5);; 2. all clusters HDF5 (*.h5)"));
#         fileType=fileName[1];
#         fileName=fileName[0];
#         if(fileName==""):
#             return;

        fileName=os.path.join(self.__dataDir,self.__dataName+".h5");
        
        print("exporting...");
        exportToHDF5PerCluster(fileName, self.__dataSet);
#         if(fileType[0]=="1"):
#             print("individual cluster per HDF5");
#             exportToHDF5PerCluster(fileName, self.__dataSet);
#         elif(fileType[0]=="2"):
#             print("single HDF5");
#             exportToHDF5(fileName, self.__dataSet);
        print("done");
     
    
    def exportWaveforms(self):
        fileName=QFileDialog.getSaveFileName(self, self.tr("export cluster data"), 
                                             self.tr(self.__dataDir), 
                                             self.tr("HDF5 (*.h5)"));
#         fileType=fileName[1];
        fileName=fileName[0];
        if(fileName==""):
            return;
        
        fout=h5py.File(fileName, "w");
        
        clusterIDs=self.__plotClusterItems.keys();
        
        for i in clusterIDs:
            (waves, wAvg, wSEM)=self.__plotClusterItems[i].getSelDispWaves();
            if(waves.size<=0):
                continue;
            clustGrp=fout.create_group("c_"+i);
            clustGrp.create_dataset("waveforms", data=waves.transpose(1, 0, 2));
            clustGrp.create_dataset("waveAverage", data=wAvg.T);
            clustGrp.create_dataset("waveSEM", data=wSEM.T);
            
        fout.flush();
        fout.close();
        

    def enableViewUI(self, enable):
        self.saveFileButton.setEnabled(enable);
        self.exportDataButton.setEnabled(enable);
        self.exportWavesButton.setEnabled(enable);
        
        self.hChannelSelect.setEnabled(enable);
        self.hParamSelect.setEnabled(enable);
        
        self.vChannelSelect.setEnabled(enable);
        self.vParamSelect.setEnabled(enable);
        
        self.workClusterSelect.setEnabled(enable);
        self.viewClustersSelect.setEnabled(enable);
        
        self.viewButton.setEnabled(enable);
        self.reportClusterButton.setEnabled(enable);
        
        self.undoBoundaryButton.setEnabled(enable);
        
        self.nextWavesButton.setEnabled(enable);
        self.prevWavesButton.setEnabled(enable);
        self.clearWavePlotsButton.setEnabled(enable);
        self.resetWaveNButton.setEnabled(enable);
        self.numWavesIncBox.setEnabled(enable);
        
        
    def enableClusterUI(self, enable):
        self.addButton.setEnabled(enable);
        self.copyButton.setEnabled(enable);
        self.refineButton.setEnabled(enable);
        self.deleteButton.setEnabled(enable);
        
        
    def enableTimeSelectUI(self, enable):
        self.timeSelLabel.setEnabled(enable);
        self.timeSelStartLabel.setEnabled(enable);
        self.timeSelEndLabel.setEnabled(enable);
        self.timeSelButton.setEnabled(enable);
        self.timeSelStartBox.setEnabled(enable);
        self.timeSelEndBox.setEnabled(enable);

        
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
        fileName=QFileDialog.getOpenFileName(self, self.tr("open data file"), 
                                             self.tr(self.__dataDir), 
                                             self.tr("1. spike files (*.spikes);; 2. cluster data set (*.clusterdataset)"));
        fileType=fileName[1];
        fileName=fileName[0];
        
        if(fileName==""):
            return;
        
        self.__dataDir=os.path.dirname(fileName);
        self.__dataName=os.path.basename(fileName);
        (self.__dataName, ext)=os.path.splitext(self.__dataName);
        
        file=open(fileName, "rb");
        self.clearSelect(); 
        
        if(fileType[0]=="1"):
            print("spikes datafile");
            self.__loadSpikesFile(fileName, file);
            
        if(fileType[0]=="2"):
            print("cluster data set");
            self.__loadClusterDataSetFile(file);     

        file.close();

        dataValid=False;
        viewValid=False;
        
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
            
            
    
    def __loadSpikesFile(self, fileName, fh):
#         fileStat=os.stat(fileName);        
        data=readSpikeFile(fh, fileName);
        print("calculating parameters");
        self.__dataSet=DataSet(data["waveforms"], data["gains"], data["thresholds"],
                               data["timestamps"], data["samplingHz"], data["triggerChs"]);
        print("done");
        del(data);
        
        (startT, endT)=self.__dataSet.getSamplesStartEndTimes();
        self.__setTimeSelUI(startT, endT);
        
        
        
    def __setTimeSelUI(self, startT, endT):
        self.enableTimeSelectUI(True);
        self.timeSelStartBox.setMinimum(startT);
        self.timeSelEndBox.setMinimum(startT);
        
        self.timeSelStartBox.setMaximum(endT);
        self.timeSelEndBox.setMaximum(endT);
        
        self.timeSelStartBox.setValue(startT);
        self.timeSelEndBox.setValue(endT);
        
        
              
    def __loadClusterDataSetFile(self, fh):
        self.__dataSet=pickle.load(fh);
        
        clustIDs=self.__dataSet.getClusterIDs();
        initID=self.__dataSet.getInitClustID();
        workID=self.__dataSet.getWorkClustID();
        self.__dataSet.setWorkClustID(initID);
        for i in clustIDs:
            cluster=self.__dataSet.getCluster(i);
            pen=None;
            brush=None;
            if(i!=initID):
                (color, pen, brush)=self.getCurColor();
            self.__addClusterToView(i, cluster, pen, brush);
        
        self.__workClustList[workID].setSelected(True);
        self.changeWorkCluster();
        
        (startT, endT)=self.__dataSet.getWorkingStartEndTimes();
        self.__setTimeSelUI(startT, endT);
        self.__setDataIsValid();
        
    
    def selectTimeWindow(self):
        startTime=self.timeSelStartBox.value();
        endTime=self.timeSelEndBox.value();
        if(endTime<=startTime):
            return;
        
        (clustID, cluster)=self.__dataSet.initializeWorkingSet(startTime, endTime);
        self.__addClusterToView(clustID, cluster);
        
        self.__setDataIsValid();
        
        
    def __setDataIsValid(self):
        self.populateSelect();
        self.__initBound();
        self.enableViewUI(True);
        self.enableClusterUI(False);
        self.enableTimeSelectUI(False);
        self.enableKeyShortcuts(True);
        self.__dataValid=True;
        self.__viewValid=False;

        
    def __addClusterToView(self, clustID, cluster, pen=None, brush=None):
        self.__plotClusterItems[clustID]=ClusterPlotItem(cluster, self.__plot, pen);
        
        self.__workClustList[clustID]=QListWidgetItem(clustID);
        self.__workClustList[clustID].setData(self.__selectDataRole, clustID);
        if(brush is not None):
            self.__workClustList[clustID].setBackground(brush);
        self.workClusterSelect.addItem(self.__workClustList[clustID]);
        
        self.__viewClustList[clustID]=QListWidgetItem(clustID);
        self.__viewClustList[clustID].setData(self.__selectDataRole, clustID);
        if(brush is not None):
            self.__viewClustList[clustID].setBackground(brush);
        self.viewClustersSelect.addItem(self.__viewClustList[clustID]);
        self.__viewClustList[clustID].setSelected(True);
        
        workClustID=self.__dataSet.getWorkClustID();
        if(not (self.__workClustList[workClustID].isSelected())):
            self.__workClustList[workClustID].setSelected(True);
            self.changeWorkCluster();
    
        
    def __removeCluster(self, id):
        (success, workClustID)=self.__dataSet.deleteCluster(id);
        
        if(not success):
            return;
        
        row=self.workClusterSelect.row(self.__workClustList[id]);
        self.workClusterSelect.takeItem(row);
        del(self.__workClustList[id]);
        
        row=self.viewClustersSelect.row(self.__viewClustList[id]);
        self.viewClustersSelect.takeItem(row);
        del(self.__viewClustList[id]);
        
        del(self.__plotClusterItems[id]);
        
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
        
        ignoredParamNames=["peakTime", "valleyTime", "PVWidth", "timestamp"];
        
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
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("S")),
                                                         widget, self.copyCluster));
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("Z")),
                                                         widget, self.undoBoundaryStep));     
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("X")),
                                                         widget, self.showReport));                                                               
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("Q")),
                                                         widget, self.drawPrevWaves));
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("W")),
                                                         widget, self.drawNextWaves));
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("E")),
                                                         widget, self.clearWavePlots));
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("R")),
                                                         widget, self.resetWaveInd));                           
                                          
        
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
        if(clustID is not None):
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
        self.__dataSet.setWorkClustID(workClustID);
        self.__initBound();
        if(not self.__viewClustList[workClustID].isSelected()):
            self.__viewClustList[workClustID].setSelected(True);
            self.invalidateView();
        
    def viewClustersChanged(self):
        selectItems=self.viewClustersSelect.selectedItems();
        workClustID=self.__dataSet.getWorkClustID();
        if(not self.__viewClustList[workClustID].isSelected()):
            if(len(selectItems)<=0):
                workClustID=self.__dataSet.getInitClustID();
            else:
                workClustID=selectItems[0].data(self.__selectDataRole);
            self.__dataSet.setWorkClustID(workClustID);
            self.__workClustList[workClustID].setSelected(True);
            self.__viewClustList[workClustID].setSelected(True);
            
        self.invalidateView();
        

        
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
        clustIDs=self.__dataSet.getClusterIDs();
        initClustID=self.__dataSet.getInitClustID();
        clustIDs.remove(initClustID);
        
        output="clusters: ";
        for i in clustIDs:
            output=output+str(i)+" ";
        output=output+"\n";
        self.__reportDisp.insertPlainText(output);
        
        for i in clustIDs:
            (numPoints, numOverlap)=self.__dataSet.computeClusterOverlap(i);
            percOverlap=int(numOverlap/float(numPoints)*1000);
            percOverlap=percOverlap/10.0;
            output="cluster "+str(i)+": "+str(numPoints)+" pts, overlap: "+str(numOverlap)+" pts, "+str(percOverlap)+"%\n";
            self.__reportDisp.insertPlainText(output);
            for j in clustIDs:
                if(i==j):
                    continue;
                (numPoints, numOverlap)=self.__dataSet.compareClustersOverlap(i, j);
                percOverlap=int(numOverlap/float(numPoints)*1000);
                percOverlap=percOverlap/10.0;
                if(numOverlap<=0):
                    continue;
                output="\toverlap cluster "+str(j)+": "+str(numOverlap)+" pts, "+str(percOverlap)+"%\n";
                self.__reportDisp.insertPlainText(output);
            self.__reportDisp.insertPlainText("\n");
            
    def drawPrevWaves(self):
        if(not self.__dataValid):
            return;
        
        workClustID=self.__dataSet.getWorkClustID();
        drawPen=self.__plotClusterItems[workClustID].getCurPen();
        
        (nChs, nptsPerCh, waves, xvals, conArr)=self.__plotClusterItems[workClustID].getPrevWaves(self.numWavesIncBox.value());
        self.__drawWavesCommon(nChs, waves, xvals, conArr, drawPen);
        
    def drawNextWaves(self):
        if(not self.__dataValid):
            return;
        
        workClustID=self.__dataSet.getWorkClustID();
        drawPen=self.__plotClusterItems[workClustID].getCurPen();
        
        (nChs, nptsPerCh, waves, xvals, conArr)=self.__plotClusterItems[workClustID].getNextWaves(self.numWavesIncBox.value());
        self.__drawWavesCommon(nChs, waves, xvals, conArr, drawPen);
    
    def __drawWavesCommon(self, nChs, waves, xvals, conArr, drawPen):   
        for i in np.r_[0:nChs]:
            self.__wavePlots[i].plot(xvals.flatten(), waves[i, :, :].flatten(), 
                                     pen=drawPen, connect=conArr.flatten());
            self.__wavePlots[i].getViewBox().autoRange();
        
    def clearWavePlots(self):
        for i in np.r_[0:len(self.__wavePlots)]:
            self.__wavePlots[i].getViewBox().autoRange();
            self.__wavePlots[i].clear();
            
            clustIDs=self.__plotClusterItems.keys();
            for i in clustIDs:
                self.__plotClusterItems[i].clearSelDispWaves();
            
    def resetWaveInd(self):
        workClustID=self.__dataSet.getWorkClustID();
        self.__plotClusterItems[workClustID].resetWaveInd();
        
    
    def plotMouseClicked(self, evt):
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

    
    def undoBoundaryStep(self):
        if(not self.__viewValid):
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
