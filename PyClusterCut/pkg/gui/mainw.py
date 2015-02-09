import os;

import numpy as np;

import PySide;

from PySide.QtGui import QMainWindow, QApplication;
from PySide.QtGui import QAbstractItemView, QListWidget, QListWidgetItem;
from PySide.QtGui import QKeySequence, QKeySequence, QShortcut, QFileDialog;

from PySide.QtCore import Qt;

import pyqtgraph as pg;
from pyqtgraph.widgets.GraphicsLayoutWidget import GraphicsLayoutWidget;

from mainw_ui import Ui_MainW;


from ..fileIO.loadOpenEphysSpikes import readSamples;

from ..data.spikes import SamplesData;


class MainW(QMainWindow, Ui_MainW):
    def __init__(self, app, parent=None):
        super(MainW, self).__init__(parent);
        self.setupUi(self);
        self.setUIEnabled(False);
        self.setFocusPolicy(Qt.StrongFocus);
        self.setWindowFlags(Qt.CustomizeWindowHint
                            | Qt.WindowMinimizeButtonHint);
                            
        self.app=app;
        
        self.plotW=GraphicsLayoutWidget();
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
        self.dataRole=0;
        
        self.dataDir="";
        self.data=None;
        
    
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
        
        self.setUIEnabled(True);
        self.populateSelect();
        
        self.enableKeyShortcuts(True);
        
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
            self.hChsList[i].setData(self.dataRole, i);
            self.hChannelSelect.addItem(self.hChsList[i]);
            
            self.vChsList[i]=QListWidgetItem(str(i));
            self.vChsList[i].setData(self.dataRole, i);
            self.vChannelSelect.addItem(self.vChsList[i]);
            
        paramKeys=self.data.getChParamTypes();
        numParams=len(paramKeys);
        self.hParamsList=[None]*numParams;
        self.vParamsList=[None]*numParams;
        for i in np.r_[0:numParams]:
            self.hParamsList[i]=QListWidgetItem(paramKeys[i]);
            self.hParamsList[i].setData(self.dataRole, paramKeys[i]);
            self.hParamSelect.addItem(self.hParamsList[i]);
            
            self.vParamsList[i]=QListWidgetItem(paramKeys[i]);
            self.vParamsList[i].setData(self.dataRole, paramKeys[i]);
            self.vParamSelect.addItem(self.vParamsList[i]);
            
                 
    
    def setUIEnabled(self, enable):
        self.saveFileButton.setEnabled(enable);
        
        self.hChannelSelect.setEnabled(enable);
        self.hParamSelect.setEnabled(enable);
        
        self.vChannelSelect.setEnabled(enable);
        self.vParamSelect.setEnabled(enable);
        
        self.workClusterSelect.setEnabled(enable);
        self.viewClustersSelect.setEnabled(enable);
        
        self.viewButton.setEnabled(enable);
        
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
        print("update view");
        self.plotVBox.autoRange();
                

    
    
    
