from PySide.QtGui import QAbstractItemView, QListWidget, QListWidgetItem;
from .clusterplotitem import ClusterPlotItem;
from .colortable import ColorTable;

class ClusterControl(object):
    def __init__(self, workClustSelect, viewClustSelect, plot):
        self.__workClustSel=workClustSelect;
        self.__viewClustSel=viewClustSelect;
        self.__plot=plot;
        
        self.__workClustList=dict();
        self.__viewClustList=dict();
        
        self.__colorTable=ColorTable();
        self.__plotClusters=dict();
        
        self.__selDataRole=0;
        
        self.__dataSet=None;
        
    def reset(self):
        self.__workClustSel.clear();
        self.__workClustList.clear();
        self.__viewClustSel.clear();
        self.__viewClustList.clear();
        self.__dataSet=None;
        self.__colorTable.resetInd();
        
    def initalize(self, dataSet):
        self.reset();
        self.__dataSet=dataSet;
        
        clustIDs=self.__dataSet.getClusterIDs();
        initID=self.__dataSet.getInitClustID();
        workID=self.__dataSet.getWorkClustID();
        self.__dataSet.setWorkClustID(initID);
        
        for i in clustIDs:
            cluster=self.__dataSet.getCluster(i);
            self.addCluster(i, cluster, (i!=initID));
        
        self.__workClustList[workID].setSelected(True);
        self.changeWorkCluster();
        
    
    def addCluster(self, clustID, cluster, useColor):
        pen=None;
        brush=None;
        if(useColor):
            (color, pen, brush)=self.__colorTable.getCurColor();
        self.__plotClusters[clustID]=ClusterPlotItem(cluster, self.__plot, pen, brush);
        self.__addToSelect(clustID, brush, self.__workClustSel, self.__workClustList);
        self.__addToSelect(clustID, brush, self.__viewClustSel, self.__viewClustList);
        self.__viewClustList[clustID].setSelected(True);
        
        
    def removeCluster(self, clustID):
        self.__rmFromSelect(clustID, self.__workClustSel, self.__workClustList);
        self.__rmFromSelect(clustID, self.__viewClustSel, self.__viewClustList);
        del(self.__plotClusters[clustID]);
        
        workClustID=self.__dataSet.getWorkClustID();
        self.__workClustList[workClustID].setSelected(True);
        self.changeWorkCluster();
        
        
    def __addToSelect(self, clustID, brush, select, clustList):
        clustList[clustID]=QListWidgetItem(clustID);
        clustList[clustID].setData(self.__selDataRole, clustID);
        if(brush is not None):
            clustList[clustID].setBackground(brush);
        select.addItem(clustList[clustID]);
    
    def __rmFromSelect(self, clustID, select, clustList):
        row=select.row(clustList[clustID]);
        select.takeItem(row);
        del(clustList[clustID]);
        
        
    def updatePlot(self, hCh, vCh, hParam, vParam, drawType):
        self.__plot.clear();
        workClustID=self.__dataSet.getWorkClustID();
        self.__viewClustList[workClustID].setSelected(True);
        self.__workClustList[workClustID].setSelected(True);
        
        viewItems=self.__viewClustSel.selectedItems();
        for item in viewItems:
            clustID=item.data(self.__selDataRole);
            self.__plotClusters[clustID].setPlotData(hCh, vCh, hParam, vParam, drawType);
            self.__plotClusters[clustID].addToPlot(drawType);
            
    def changeWorkCluster(self):
        selectItem=self.__workClustSel.selectedItems();
        if(len(selectItem)<=0):
            return;
        selectItem=selectItem[0];
        workClustID=selectItem.data(self.__selDataRole);
        self.__dataSet.setWorkClustID(workClustID);
        if(not self.__viewClustList[workClustID].isSelected()):
            self.__viewClustList[workClustID].setSelected(True);
            
    def changeViewClusters(self):
        workClustID=self.__dataSet.getWorkClustID();
        if(not self.__viewClustList[workClustID].isSelected()):
            workClustID=self.__dataSet.getInitClustID();
            self.__dataSet.setWorkClustID(workClustID);
            self.__viewClustList[workClustID].setSelected(True);
            self.__workClustList[workClustID].setSelected(True);
        
    
    def getWorkPen(self):
        if(self.__dataSet is None):
            return None;
        workClustID=self.__dataSet.getWorkClustID();
        pen=self.__plotClusters[workClustID].getCurPen();
        return pen;
    
    
    def getPlotClusters(self):
        return self.__plotClusters;
    
    def getWorkPlotCluster(self):
        if(self.__dataSet is None):
            return None;
        workClustID=self.__dataSet.getWorkClustID();
        return self.__plotClusters[workClustID];
        
    def clearClusterSelWaves(self):
        clustIDs=self.__plotClusters.keys();
        for i in clustIDs:
            self.__plotClusters[i].clearSelDispWaves();

