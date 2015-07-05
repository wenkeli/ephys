import os;

import h5py;

import numpy as np;

from ..data.dataset import DataSet;
from ..gui.clusterplotitem import ClusterPlotItem;

def exportToHDF5(fileName, dataSet):
    fout=h5py.File(fileName, "w");
    
    initID=dataSet.getInitClustID();
    
    clustIDs=dataSet.getClusterIDs();
    clustIDs.remove(initID);
    
    paramKeys=dataSet.getSamples().getParamNames();
    
    for i in clustIDs:
        cluster=dataSet.getCluster(i);
        
        clustGrp=fout.create_group(i);
        
        clustGrp.create_dataset("rating", data=cluster.getRating());
        for j in paramKeys:
            param=cluster.getParamAllChs(j);
            if(len(param.shape)>=2):
                param=param.T;
            clustGrp.create_dataset(j, data=param);
        
    fout.flush();
    fout.close();

def exportToHDF5PerCluster(fileName, dataSet):
    fName, fExt=os.path.splitext(fileName);
    
    initID=dataSet.getInitClustID();
    clustIDs=dataSet.getClusterIDs();
    clustIDs.remove(initID);
    
    paramKeys=dataSet.getSamples().getParamNames();
    
    for i in clustIDs:
        fout=h5py.File(fName+".C_"+str(i)+fExt, "w");
        cluster=dataSet.getCluster(i);
        fout.create_dataset("rating", data=cluster.getRating());
        for j in paramKeys:
            param=cluster.getParamAllChs(j);
            if(len(param.shape)>=2):
                param=param.T;
            fout.create_dataset(j, data=param);
        fout.flush();
        fout.close();

def exportWavesToHDF5(fileName, plotClusters):
    fout=h5py.File(fileName, "w");
    clustIDs=plotClusters.keys();
    
    for i in clustIDs:
        (waves, wAvg, wSEM)=plotClusters[i].getSelDispWaves();
        if(waves.size<=0):
            continue;
        clustGrp=fout.create_group("c_"+i);
        clustGrp.create_dataset("waveforms", data=waves.transpose(1, 0, 2));
        clustGrp.create_dataset("waveAverage", data=wAvg.T);
        clustGrp.create_dataset("waveSEM", data=wSEM.T);
        
    fout.flush();
    fout.close();
    
    
    
    
