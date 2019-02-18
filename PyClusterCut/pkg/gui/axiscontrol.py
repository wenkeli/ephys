import numpy as np;
from PyQt5.QtWidgets import QAbstractItemView, QListWidget, QListWidgetItem;
from ..data.dataset import DataSet;

class AxisControl(object):
    def __init__(self, chSelect, paramSelect):
        self.__chSelect=chSelect;
        self.__paramSelect=paramSelect;
        
        self.__chList=dict();
        self.__paramList=dict();
        
        self.__chN=None;
        self.__paramName=None;
        
        self.__selDataRole=0;
        
        self.__limits=dict();
        
        
    def reset(self):
        self.__chSelect.clear();
        self.__paramSelect.clear();
        self.__chList.clear();
        self.__paramList.clear();
        self.__chN=None;
        self.__paramName=None;
        self.__limits.clear();
        
        
    def populate(self, dataSet):
        self.reset();
        numChs=dataSet.getSamples().getNumChannels();
        for i in np.r_[0:numChs]:
            strI=str(i);
            self.__chList[strI]=QListWidgetItem(strI);
            self.__chList[strI].setData(self.__selDataRole, i);
            self.__chSelect.addItem(self.__chList[strI]);
            
        paramNames=dataSet.getSamples().getParamNames();
        
        ignoredParamNames=["peakTime", "valleyTime", "timestamp"];
        
        modParamNames=[];
        if("peak" in paramNames):
            modParamNames.append("peak");
        if("valley" in paramNames):
            modParamNames.append("valley");
        if("peakAngle" in paramNames):
            modParamNames.append("peakAngle");
        if("peakFallAngle" in paramNames):
            modParamNames.append("peakFallAngle");
        if("time" in paramNames):
            modParamNames.append("time");
        if("peakEnergy" in paramNames):
            modParamNames.append("peakEnergy");
        if("peakMax" in paramNames):
            modParamNames.append("peakMax");
        if("valleyEnergy" in paramNames):
            modParamNames.append("valleyEnergy");
        if("PVWidth" in paramNames):
            modParamNames.append("PVWidth");
        
        for name in paramNames:
            if(name in ignoredParamNames):
                continue;
            if(name in modParamNames):
                continue;
            modParamNames.append(name);
            
        for name in modParamNames:
            self.__paramList[name]=QListWidgetItem(name);
            self.__paramList[name].setData(self.__selDataRole, name);
            self.__paramSelect.addItem(self.__paramList[name]);
            
        self.updateViewLimits(dataSet);
            
                
    def updateViewLimits(self, dataSet):
        numChs=dataSet.getSamples().getNumChannels();
        for name in self.__paramList.keys():
            self.__limits[name]=dict();
            for j in np.r_[0:numChs]:
                bounds=dataSet.getParamBounds(j, name);
                self.__limits[name][j]=bounds;  
        
        
    
    def setSelected(self, chN, paramName):
        self.__chList[str(chN)].setSelected(True);
        self.__paramList[paramName].setSelected(True);

    def getSelected(self):
        chSel=self.__chSelect.selectedItems();
        paramSel=self.__paramSelect.selectedItems();
        
        if((len(chSel)<=0) or (len(paramSel)<=0)):
            self.__chN=None;
            self.__paramName=None;
            return (None, None);
        
        self.__chN=int(chSel[0].data(self.__selDataRole));
        self.__paramName=paramSel[0].data(self.__selDataRole);
        return (self.__chN, self.__paramName);
    
    
    
    def getLimits(self, chN=None, paramName=None):
        if(chN is None):
            chN=self.__chN;
        if(paramName is None):
            paramName=self.__paramName;
        return self.__limits[paramName][int(chN)];
    
    
    