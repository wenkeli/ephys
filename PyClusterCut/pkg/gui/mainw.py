import os;
import gc;

import numpy as np;

import PySide;
from PySide.QtGui import QMainWindow, QApplication;
from PySide.QtGui import QAbstractItemView, QListWidget, QListWidgetItem;
from PySide.QtGui import QKeySequence, QShortcut, QFileDialog;
from PySide.QtCore import Qt, QRect;

import pyqtgraph as pg;
from pyqtgraph.widgets.GraphicsLayoutWidget import GraphicsLayoutWidget;

from mainw_ui import Ui_MainW;
from reportw import ReportW;

from ..fileIO.loadOpenEphysSpikes import readSpikeFile;
from ..fileIO.exporthdf5 import exportToHDF5PerCluster, exportWavesToHDF5;
from ..fileIO.datasetpickle import saveDataSetPickle, loadDataSetPickle;


from ..data.samples import SamplesData; 
from ..data.samples import SamplesClustCount;
from ..data.cluster import Cluster, Boundary;
from ..data.dataset import DataSet;

from .clusterplotitem import ClusterPlotItem;
from .colortable import ColorTable;
from .workboundary import WorkBoundary;
from .axiscontrol import AxisControl;
        

class MainW(QMainWindow, Ui_MainW):
    def __init__(self, app, parent=None):
        super(MainW, self).__init__(parent);
        self.setupUi(self);
        
        self.setFocusPolicy(Qt.StrongFocus);
        self.setWindowFlags(Qt.CustomizeWindowHint
                            | Qt.WindowMinimizeButtonHint);
                            
        self.__dataDir="";
        self.__dataFilter="";
        self.__dataSet=None;
        self.__plotClusterItems=dict();
        self.__dataValid=False;
        
        self.__colorTable=ColorTable();
                            
        self.__app=app;
        
        self.__reportW=ReportW();
        
        screenSize=QApplication.desktop().availableGeometry(self);
        sh=screenSize.height();
        sw=screenSize.width();
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
        self.__plotScene=self.__plot.scene();
        self.__plotScene.setMoveDistance(200);
        self.__plotVBox=self.__plot.getViewBox();
        self.__plotVBox.setMouseMode(pg.ViewBox.RectMode);
        self.__plotVBox.disableAutoRange();
        self.__plotType=0;
        
        self.__wavePlotLayout=self.__plotW.addLayout(0, 1, 1, 1);
        self.__plotW.ci.layout.setColumnStretchFactor(0, 80);
        self.__plotW.ci.layout.setColumnStretchFactor(1, 20);
        self.__wavePlots=[];
        
        self.__keyShortcuts=dict();
        self.__setupKeyShortcuts(self);
        self.__setupKeyShortcuts(self.__plotW);
        self.__setupKeyShortcuts(self.__reportW);
        self.__enableKeyShortcuts(False);
        
        self.__hAxis=AxisControl(self.hChannelSelect, self.hParamSelect);
        self.__vAxis=AxisControl(self.vChannelSelect, self.vParamSelect);
        
        self.__selectDataRole=0;
        self.__workClustList=dict();
        self.__viewClustList=dict();
        self.__viewValid=False;
        
        self.__workBound=WorkBoundary(self.__plot);
        
        self.__resetState();
                                                    
       
    def __resetBound(self):
        if(self.__dataSet is None):
            drawPen=None;
        else:
            workClustID=self.__dataSet.getWorkClustID();
            drawPen=self.__plotClusterItems[workClustID].getCurPen();
        self.__workBound.reset(drawPen);
                                                    
        
    def saveClusterData(self):
        fileName=os.path.join(self.__dataDir,self.__dataName+".clusterdataset");
        saveDataSetPickle(fileName, self.__dataSet);
        self.saveFileButton.setText(QApplication.translate("MainW", "file saved!",
                                                           None, QApplication.UnicodeUTF8));
        
        
    def exportData(self):
        fileName=os.path.join(self.__dataDir,self.__dataName+".h5");
        
        print("exporting...");
        exportToHDF5PerCluster(fileName, self.__dataSet);

        print("done");
        self.exportDataButton.setText(QApplication.translate("MainW", "data exported!",
                                                             None, QApplication.UnicodeUTF8));
     
    
    def exportWaveforms(self):
        fileName=QFileDialog.getSaveFileName(self, self.tr("export cluster data"), 
                                             self.tr(self.__dataDir), 
                                             self.tr("HDF5 (*.h5)"));
        fileName=fileName[0];
        if(fileName==""):
            return;
        exportWavesToHDF5(fileName, self.__plotClusterItems);
        

    def __enableViewUI(self, enable):
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
        self.viewLargeButton.setEnabled(enable);
        self.reportClusterButton.setEnabled(enable);
        
        self.stepBackBoundButton.setEnabled(enable);
        
        self.nextWavesButton.setEnabled(enable);
        self.prevWavesButton.setEnabled(enable);
        self.clearWavePlotsButton.setEnabled(enable);
        self.resetWaveNButton.setEnabled(enable);
        self.toggleRefWaveChsButton.setEnabled(enable);
        self.refWaveChsOnlyBox.setEnabled(enable);
        self.numWavesIncBox.setEnabled(enable);
        
        self.clustRateBox.setEnabled(enable);
        
        
    def __enableClusterUI(self, enable):
        self.addButton.setEnabled(enable);
        self.copyButton.setEnabled(enable);
        self.refineButton.setEnabled(enable);
        self.deleteButton.setEnabled(enable);
        self.undoClustButton.setEnabled(enable);
        
        
    def __enableTimeSelectUI(self, enable):
        self.timeSelLabel.setEnabled(enable);
        self.timeSelStartLabel.setEnabled(enable);
        self.timeSelEndLabel.setEnabled(enable);
        self.timeSelButton.setEnabled(enable);
        self.timeResetButton.setEnabled(enable);
        self.timeSelStartBox.setEnabled(enable);
        self.timeSelEndBox.setEnabled(enable);

        
    def invalidateView(self):
        self.__viewValid=False;
        self.__workBound.setDrawBound(self.__viewValid);
        self.__enableClusterUI(False);
        
    def __validateView(self):
        self.__viewValid=True;
        self.__workBound.setDrawBound(self.__viewValid);
        self.__enableClusterUI(True);
        

    def quit(self):
        self.__app.closeAllWindows();
    
    def __resetState(self):
        self.__dataSet=None;
        self.__plotClusterItems.clear();
        self.__dataValid=False;
        
        self.__plot.clear();
        
        numWavePlots=len(self.__wavePlots);
        if(numWavePlots>0):
            for i in np.r_[0:numWavePlots]:
                self.__wavePlotLayout.removeItem(self.__wavePlots[0]);
                del(self.__wavePlots[0]);
            self.__wavePlots=[];
            
        self.__resetFileButtonTexts();
        
        self.__enableClusterUI(False);
        self.__enableTimeSelectUI(False);
        self.__enableViewUI(False);
        self.__enableKeyShortcuts(False);
        self.clearSelect();
                                                                                                     
        gc.collect();
        
        
    def __resetFileButtonTexts(self):
        self.saveFileButton.setText(QApplication.translate("MainW", "save file",
                                                           None, QApplication.UnicodeUTF8));
        self.exportDataButton.setText(QApplication.translate("MainW", "export data",
                                                             None, QApplication.UnicodeUTF8));

    
    def loadFile(self):
        print("loading fin");
        fileName=QFileDialog.getOpenFileName(self, self.tr("open data fin"), 
                                             self.tr(self.__dataDir), 
                                             self.tr("1. spike files (*.spikes);;2. cluster data set (*.clusterdataset)"),
                                             self.__dataFilter);
        fileType=fileName[1];
        self.__dataFilter=fileType;
        fileName=fileName[0];
        if(fileName==""):
            return;
        
        self.__dataDir=os.path.dirname(fileName);
        dataFName=os.path.basename(fileName);
        (self.__dataName, ext)=os.path.splitext(dataFName);
        self.__plotW.setWindowTitle(dataFName);
        
        self.__resetState();
        
        if(fileType[0]=="1"):
            print("spikes datafile");
            self.__loadSpikesFile(fileName);
            
        if(fileType[0]=="2"):
            print("cluster data set");
            self.__loadClusterDataSetFile(fileName);
        
        if(self.__dataSet is None):
            return;
        
        numChannels=self.__dataSet.getSamples().getNumChannels();
        for i in np.r_[0:numChannels]:
            wavePlot=self.__wavePlotLayout.addPlot(i, 0, enableMenu=False);
            self.__wavePlots.append(wavePlot);
            
            
    
    def __loadSpikesFile(self, fileName):
#         fileStat=os.stat(fileName);        
        data=readSpikeFile(fileName);
        if(data is None):
            self.__dataSet=None;
            return;
        
        print("calculating parameters");
        self.__dataSet=DataSet(data["waveforms"], data["timestamps"], data["numChs"], data["samplingHz"]);
        print("done");
        del(data);
        
        (startT, endT)=self.__dataSet.getSamplesStartEndTimes();
        self.__setTimeSelUI(startT, endT);
        
        
    def __setTimeSelUI(self, startT, endT):
        self.__enableTimeSelectUI(True);
        tSSVal=self.timeSelStartBox.value();
        tSEVal=self.timeSelEndBox.value();
        
        self.timeSelStartBox.setMinimum(startT);
        self.timeSelEndBox.setMinimum(startT);
        
        self.timeSelStartBox.setMaximum(endT);
        self.timeSelEndBox.setMaximum(endT);
        
        if((tSSVal<startT) or (tSSVal>endT) or (tSEVal<startT) or (tSEVal>endT)):
            self.timeSelStartBox.setValue(startT);
            self.timeSelEndBox.setValue(endT);
        
        
              
    def __loadClusterDataSetFile(self, fileName):
        self.__dataSet=loadDataSetPickle(fileName);
        
        clustIDs=self.__dataSet.getClusterIDs();
        initID=self.__dataSet.getInitClustID();
        workID=self.__dataSet.getWorkClustID();
        self.__dataSet.setWorkClustID(initID);
        for i in clustIDs:
            cluster=self.__dataSet.getCluster(i);
            pen=None;
            brush=None;
            if(i!=initID):
                (color, pen, brush)=self.__colorTable.getCurColor();
            self.__addClusterToView(i, cluster, pen, brush);
        
        self.__workClustList[workID].setSelected(True);
        self.changeWorkCluster();
        
        (startT, endT)=self.__dataSet.getWorkingStartEndTimes();
        self.__setTimeSelUI(startT, endT);
        self.__setDataIsValid();
        
    def resetTimeWindow(self):
        (startT, endT)=self.__dataSet.getSamplesStartEndTimes();
        self.timeSelStartBox.setValue(startT);
        self.timeSelEndBox.setValue(endT);
    
    def selectTimeWindow(self):
        startTime=self.timeSelStartBox.value();
        endTime=self.timeSelEndBox.value();
        if(endTime<=startTime):
            return;
        
        (clustID, cluster)=self.__dataSet.initializeWorkingSet(startTime, endTime);
        self.__addClusterToView(clustID, cluster);
        
        self.__setDataIsValid();
        
        
    def __setDataIsValid(self):
        self.__populateSelect();
        self.__resetBound();
        self.__enableViewUI(True);
        self.__enableClusterUI(False);
        self.__enableTimeSelectUI(False);
        self.__enableKeyShortcuts(True);
        self.__dataValid=True;
        self.invalidateView();

        
    def __addClusterToView(self, clustID, cluster, pen=None, brush=None):
        self.__plotClusterItems[clustID]=ClusterPlotItem(cluster, self.__plot, pen, brush);
        
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
    
        
    def __removeCluster(self, clustID):
        (success, workClustID)=self.__dataSet.deleteCluster(clustID);
        
        if(not success):
            return;
        
        row=self.workClusterSelect.row(self.__workClustList[clustID]);
        self.workClusterSelect.takeItem(row);
        del(self.__workClustList[clustID]);
        
        row=self.viewClustersSelect.row(self.__viewClustList[clustID]);
        self.viewClustersSelect.takeItem(row);
        del(self.__viewClustList[clustID]);
        
        del(self.__plotClusterItems[clustID]);
        
        self.__workClustList[workClustID].setSelected(True);
        self.changeWorkCluster();

        
    def clearSelect(self):
        self.invalidateView();
        self.__hAxis.reset();
        self.__vAxis.reset();


    def __populateSelect(self):
        self.__hAxis.populate(self.__dataSet);
        self.__vAxis.populate(self.__dataSet);
        
        
    def __setupKeyShortcuts(self, widget):
        widgetName=widget.objectName();
        self.__keyShortcuts[widgetName]=[];
        
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("V")),
                                                         widget, self.plotPoints));
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("C")),
                                                         widget, self.plotLargePoints));    
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("Shift+D")),
                                                         widget, self.deleteCluster));
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("F")),
                                                         widget, self.refineCluster));
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("A")),
                                                         widget, self.addCluster));
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("S")),
                                                         widget, self.copyCluster));
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("Shift+G")),
                                                         widget, self.undoCluster));
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("Z")),
                                                         widget, self.stepBackBoundary));     
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("X")),
                                                         widget, self.toggleReport));                                                               
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("Q")),
                                                         widget, self.drawPrevWaves));
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("W")),
                                                         widget, self.drawNextWaves));
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("E")),
                                                         widget, self.clearWavePlots));
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("R")),
                                                         widget, self.resetWaveInd));
        self.__keyShortcuts[widgetName].append(QShortcut(QKeySequence(self.tr("T")),
                                                         widget, self.toggleRefWaveChs));                       
                                          
        
    def __enableKeyShortcuts(self, enable):
        keys=self.__keyShortcuts.keys();
        
        for i in keys:
            numKeys=len(self.__keyShortcuts[i]);            
            for j in np.r_[0:numKeys]:
                self.__keyShortcuts[i][j].setEnabled(enable);
                
    
    def plotPoints(self):
        self.__plotType=0;
        self.updatePlotView();
        
    def plotLargePoints(self):
        self.__plotType=1;
        self.updatePlotView();
        
    def __setView(self, hChN, vChN, hParamName, vParamName):
        self.__hAxis.setSelected(hChN, hParamName);
        self.__vAxis.setSelected(vChN, vParamName)
        self.updatePlotView();
    
    
    def updatePlotView(self):
        if(not self.__dataValid):
            return;
        (hCh, hParam)=self.__hAxis.getSelected();
        (vCh, vParam)=self.__vAxis.getSelected();
        
        self.__plot.clear();
        self.__resetBound();
        
        if((hCh is None) or (hParam is None) or (vCh is None) or (vParam is None)):
            return;            

        workClustID=self.__dataSet.getWorkClustID();
        self.__viewClustList[workClustID].setSelected(True);
        self.__workClustList[workClustID].setSelected(True);
        viewClustItems=self.viewClustersSelect.selectedItems();
        for item in viewClustItems[::-1]:
            clustID=item.data(self.__selectDataRole);        
            self.__plotClusterItems[clustID].setPlotData(hCh, vCh, hParam, vParam, 
                                                         self.__plotType);
            self.__plotClusterItems[clustID].addToPlot(self.__plotType);
        
        hLim=self.__hAxis.getLimits();
        vLim=self.__vAxis.getLimits();
        self.__plotVBox.setXRange(hLim[0], hLim[1]);
        self.__plotVBox.setYRange(vLim[0], vLim[1]);
        
        self.__validateView();
        
        
    def undoCluster(self):
        if(not self.__dataValid):
            return;
        view=self.__dataSet.stepBackCluster();
        if(view is not None):
            self.__setView(view[0][0], view[0][1], view[1][0], view[1][1]);
        self.updatePlotView();
        
        
    def __addClustCommon(self, copy):
        if((not self.__workBound.getBoundClosed()) 
           or (not self.__dataValid) or (not self.__viewValid)):
            return;
        self.__resetFileButtonTexts();

        (hCh, hParam)=self.__hAxis.getSelected();
        (vCh, vParam)=self.__vAxis.getSelected();        
        (clustID, cluster)=self.__dataSet.addCluster(copy, hCh, vCh, hParam, vParam,
                                  self.__workBound.getBoundX(), 
                                  self.__workBound.getBoundY());
        if(clustID is not None):
            (color, pen, brush)=self.__colorTable.getCurColor();
            self.__addClusterToView(clustID, cluster, pen, brush);
            
        self.updatePlotView();
    
    def addCluster(self):
        self.__addClustCommon(False);
    
    def copyCluster(self):
        self.__addClustCommon(True);
    
    def deleteCluster(self):
        if((not self.__dataValid) or (not self.__viewValid)):
            return;
        self.__resetFileButtonTexts();
        
        workClustID=self.__dataSet.getWorkClustID();
        self.__removeCluster(workClustID);
        self.updatePlotView();
       
    
    def refineCluster(self):
        if((not self.__workBound.getBoundClosed()) 
           or (not self.__dataValid) or (not self.__viewValid)):
            return;
        self.__resetFileButtonTexts();

        (hCh, hParam)=self.__hAxis.getSelected();
        (vCh, vParam)=self.__vAxis.getSelected();        
        self.__dataSet.refineCluster(hCh, vCh, hParam, vParam,
                                     self.__workBound.getBoundX(), 
                                     self.__workBound.getBoundY());
        self.updatePlotView();
        
        
    def changeWorkCluster(self):
        selectItem=self.workClusterSelect.selectedItems();
        if(len(selectItem)<=0):
            return;
        workClustID=selectItem[0].data(self.__selectDataRole);
        self.__dataSet.setWorkClustID(workClustID);
        self.__resetBound();
        self.__validateView();
        if(not self.__viewClustList[workClustID].isSelected()):
            self.__viewClustList[workClustID].setSelected(True);
            self.invalidateView();
        self.clustRateBox.setValue(self.__dataSet.getWorkingCluster().getRating());
        
    def updateClustRating(self, rating):
        self.__dataSet.getWorkingCluster().setRating(rating);
        
    def viewClustersChanged(self):
        selectItems=self.viewClustersSelect.selectedItems();
        if(self.__dataSet is None):
            return;
        workClustID=self.__dataSet.getWorkClustID();
        
        if((len(self.__viewClustList.keys())<=0) or (len(self.__workClustList.keys())<=0)):
            return;
        if(not self.__viewClustList[workClustID].isSelected()):
            if(len(selectItems)<=0):
                workClustID=self.__dataSet.getInitClustID();
            else:
                workClustID=selectItems[0].data(self.__selectDataRole);
            self.__dataSet.setWorkClustID(workClustID);
            self.__workClustList[workClustID].setSelected(True);
            self.__viewClustList[workClustID].setSelected(True);
            
        self.invalidateView();
        

        
    def toggleReport(self):
        if(self.__reportW.isVisible()):
            self.__reportW.hide();
        else:
            self.__reportW.show();
            self.__reportW.generateReport(self.__dataSet);
            
    def drawPrevWaves(self):
        if(not self.__dataValid):
            return;
        
        workClustID=self.__dataSet.getWorkClustID();
        drawPen=self.__plotClusterItems[workClustID].getCurPen();
        
        triggerOnly=self.refWaveChsOnlyBox.isChecked();
        (nChs, nptsPerCh, waves, xvals, conArrs)=self.__plotClusterItems[workClustID].getPrevWaves(self.numWavesIncBox.value(), triggerOnly);
        self.__drawWavesCommon(nChs, waves, xvals, conArrs, drawPen);
        
    def drawNextWaves(self):
        if(not self.__dataValid):
            return;
        
        workClustID=self.__dataSet.getWorkClustID();
        drawPen=self.__plotClusterItems[workClustID].getCurPen();
        
        triggerOnly=self.refWaveChsOnlyBox.isChecked();
        (nChs, nptsPerCh, waves, xvals, conArrs)=self.__plotClusterItems[workClustID].getNextWaves(self.numWavesIncBox.value(), triggerOnly);
        self.__drawWavesCommon(nChs, waves, xvals, conArrs, drawPen);
    
    def __drawWavesCommon(self, nChs, waves, xvals, conArrs, drawPen):
        yMin=100000.0;
        yMax=-100000.0;
        for i in np.r_[0:nChs]:
            if((waves[i] is None) or (len(waves[i])<=0)):
                continue;
            self.__wavePlots[i].plot(xvals[i].flatten(), waves[i][:, :].flatten(), 
                                     pen=drawPen, connect=conArrs[i].flatten());
            self.__wavePlots[i].getViewBox().autoRange();
            boxRange=self.__wavePlots[i].getViewBox().viewRange();
            boxMin=boxRange[1][0];
            boxMax=boxRange[1][1];
            if(boxMin<yMin):
                yMin=boxMin;
            if(boxMax>yMax):
                yMax=boxMax;
                
        for i in np.r_[0:nChs]:
            self.__wavePlots[i].getViewBox().setYRange(yMin, yMax);            
        
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
        
    def toggleRefWaveChs(self):
        self.refWaveChsOnlyBox.toggle();
    
    def stepBackBoundary(self):
        if(not self.__viewValid):
            return;
        self.__workBound.stepBackBoundary();
