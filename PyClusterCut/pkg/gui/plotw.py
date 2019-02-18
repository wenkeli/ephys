from PyQt5.QtCore import Qt;

from pyqtgraph.widgets.GraphicsLayoutWidget import GraphicsLayoutWidget;

from .mainplot import MainPlot;
from .waveplots import WavePlots;

class PlotW(object):
    def __init__(self, width, height, hAxisCtrl, vAxisCtrl):
        self.__window=GraphicsLayoutWidget();
        self.__window.resize(width, height);
        self.__window.move(0, 0);
        
        self.__window.setFocusPolicy(Qt.StrongFocus);
        self.__window.setObjectName("plotWindow");
        self.__window.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint);
        self.__window.show();
        
        plot=self.__window.addPlot(0, 0, 1, 1, enableMenu=False);
        self.__mainPlot=MainPlot(plot, hAxisCtrl, vAxisCtrl);
        
        waveLayout=self.__window.addLayout(0, 1, 1, 1);
        self.__wavePlots=WavePlots(waveLayout);
        
        self.__window.ci.layout.setColumnStretchFactor(0, 80);
        self.__window.ci.layout.setColumnStretchFactor(1, 20);
        
    
    def reset(self):
        self.__mainPlot.reset();
        self.__wavePlots.reset();
        
    
    def initialize(self, numChs):
        self.__wavePlots.initializePlots(numChs);
    
        
    def getWindow(self):
        return self.__window;
    
    def setWindowTitle(self, title):
        self.__window.setWindowTitle(title);
        
        
    def getMainPlot(self):
        return self.__mainPlot;
    
    def getWavePlots(self):
        return self.__wavePlots;
        
        

