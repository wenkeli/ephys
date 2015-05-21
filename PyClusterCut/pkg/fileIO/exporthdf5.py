import h5py;

import numpy as np;

from ..data.dataset import DataSet;

def exportToHDF5(fileName, dataSet):
    fout=h5py.File(fileName, "w");
    
    initID=dataSet.getInitClustID();
    
    clustIDs=dataSet.getClusterInds();
    
    paramKeys=dataSet.getSamples().getParamNames();
    
    for i in clustIDs:
        if(i==initID):
            continue;
        
        cluster=dataSet.getCluster(i);
        
        clustGrp=fout.create_group(i);
        
        for j in paramKeys:
            clustGrp.create_dataset(j, data=cluster.getParamAllChs(j));
        
    fout.flush();
    fout.close();
