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

from .workboundary import WorkBoundary;
from .axiscontrol import AxisControl;
from .clustercontrol import ClusterControl;
from .mainplot import MainPlot;
from .waveplots import WavePlots;
from .plotw import PlotW;
        

class MainW(QMainWindow, Ui_MainW):
    def __init__(self, app, parent=None):
        super(MainW, self).__init__(parent);
        self.setupUi(self);
        self.setFocusPolicy(Qt.StrongFocus);
        self.setWindowFlags(Qt.CustomizeWindowHint
                            | Qt.WindowMinimizeButtonHint); 
        
        self.__app=app;
        self.__dataDir="";
        self.__dataFilter="";
        self.__dataSet=None;
        self.__dataValid=False;
        self.__viewValid=False;
        self.__drawType=0;
        
        self.__reportW=ReportW();
        
        self.__hAxis=AxisControl(self.hChannelSelect, self.hParamSelect);
        self.__vAxis=AxisControl(self.vChannelSelect, self.vParamSelect);
        
        screenSize=QApplication.desktop().availableGeometry(self);
        sh=screenSize.height();
        sw=screenSize.width();
        cpw=self.geometry().width();
        self.move(sw-cpw, 0);
        pW=sw-cpw-25;
        pH=sh; 
        self.__plotW=PlotW(pW, pH, self.__hAxis, self.__vAxis);
        
        self.__clustCtrl=ClusterControl(self.workClusterSelect, 
                                        self.viewClustersSelect,
                                        self.__plotW.getMainPlot().getPlot());
        
        self.__workBound=WorkBoundary(self.__plotW.getMainPlot().getPlot());
        
        self.__keyShortcuts=dict();
        self.__setupKeyShortcuts(self);
        self.__setupKeyShortcuts(self.__plotW.getWindow());
        self.__setupKeyShortcuts(self.__reportW);
        self.__enableKeyShortcuts(False);
        
        self.__resetState();
                                                    
       
    def __resetBound(self):
        if(not self.__dataValid):
            drawPen=None;
        else:
            drawPen=self.__clustCtrl.getWorkPen();
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
        exportWavesToHDF5(fileName, self.__clustCtrl.getPlotClusters());
        

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
        self.__dataValid=False;
        
        self.__plotW.reset();
            
        self.__resetFileButtonTexts();
        
        self.__enableClusterUI(False);
        self.__enableTimeSelectUI(False);
        self.__enableViewUI(False);
        self.__enableKeyShortcuts(False);
        self.__clearSelect();
                                                                                                     
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
        if(fileName[0]==""):
            return;
        fileType=fileName[1];
        self.__dataFilter=fileType;
        fileName=fileName[0];
        
        self.__dataDir=os.path.dirname(fileName);
        dataFName=os.path.basename(fileName);
        (self.__dataName, ext)=os.path.splitext(dataFName);
        self.__plotW.setWindowTitle(dataFName);
        
        self.__resetState();
        print("file name: "+fileName);
        
        if(fileType[0]=="1"):
            print("spikes datafile");
            self.__loadSpikesFile(fileName);
        if(fileType[0]=="2"):
            print("cluster data set");
            self.__loadClusterDataSetFile(fileName);
        if(self.__dataSet is None):
            return;
        
        numChannels=self.__dataSet.getSamples().getNumChannels();
        self.__plotW.initialize(numChannels);
        
    
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
        self.__clustCtrl.initalize(self.__dataSet);
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
        
        self.__dataSet.initializeWorkingSet(startTime, endTime);
        self.__clustCtrl.initalize(self.__dataSet);
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
        
    def __removeCluster(self, clustID):
        (success, workClustID)=self.__dataSet.deleteCluster(clustID);
        if(not success):
            return;
        self.__clustCtrl.removeCluster(clustID);

        
    def __clearSelect(self):
        self.invalidateView();
        self.__hAxis.reset();
        self.__vAxis.reset();
        self.__clustCtrl.reset();

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
        self.__drawType=0;
        self.updatePlotView();
        
    def plotLargePoints(self):
        self.__drawType=1;
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
        
        if((hCh is None) or (hParam is None) or (vCh is None) or (vParam is None)):
            return;            
        self.__clustCtrl.updatePlot(hCh, vCh, hParam, vParam, self.__drawType);
        
        self.__resetBound();
        self.__plotW.getMainPlot().updateLimits();
        
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
            self.__clustCtrl.addCluster(clustID, cluster, True);
            
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
        if(not self.__dataValid):
            return;
        self.__clustCtrl.changeWorkCluster();
        self.__resetBound();
        self.__validateView();
        self.clustRateBox.setValue(self.__dataSet.getWorkingCluster().getRating());
        
    def updateClustRating(self, rating):
        if(not self.__dataValid):
            return;
        self.__dataSet.getWorkingCluster().setRating(rating);
        
    def viewClustersChanged(self):
        if(not self.__dataValid):
            return;
        self.__clustCtrl.changeViewClusters();
        self.invalidateView();

        
    def toggleReport(self):
        if(not self.__dataValid):
            return;
        if(self.__reportW.isVisible()):
            self.__reportW.hide();
        else:
            self.__reportW.show();
            self.__reportW.generateReport(self.__dataSet);
            
    def drawPrevWaves(self):
        if(not self.__dataValid):
            return;
        (waves, xvals, conArrs, drawPen)=self.__getWaves(False);        
        self.__plotW.getWavePlots().drawWaves(waves, xvals, conArrs, drawPen);
        
    def drawNextWaves(self):
        if(not self.__dataValid):
            return;
        (waves, xvals, conArrs, drawPen)=self.__getWaves(True);
        self.__plotW.getWavePlots().drawWaves(waves, xvals, conArrs, drawPen);
        
    def __getWaves(self, getNext):
        if(not self.__dataValid):
            return (None, None, None, None);
        drawPen=self.__clustCtrl.getWorkPen();
        triggerOnly=self.refWaveChsOnlyBox.isChecked();
        workClust=self.__clustCtrl.getWorkPlotCluster();
        if(getNext):
            (nChs, nptsPerCh, waves, xvals, conArrs)=workClust.getNextWaves(self.numWavesIncBox.value(), triggerOnly);
        else:
            (nChs, nptsPerCh, waves, xvals, conArrs)=workClust.getPrevWaves(self.numWavesIncBox.value(), triggerOnly);
        return (waves, xvals, conArrs, drawPen);
           
        
    def clearWavePlots(self):
        self.__plotW.getWavePlots().clearPlots();            
        self.__clustCtrl.clearClusterSelWaves();
            
    def resetWaveInd(self):
        if(not self.__dataValid):
            return;
        workPlotClust=self.__clustCtrl.getWorkPlotCluster();
        workPlotClust.resetWaveInd();
        
    def toggleRefWaveChs(self):
        self.refWaveChsOnlyBox.toggle();
    
    def stepBackBoundary(self):
        if(not self.__viewValid):
            return;
        self.__workBound.stepBackBoundary();
