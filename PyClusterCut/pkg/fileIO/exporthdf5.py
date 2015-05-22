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
            param=cluster.getParamAllChs(j);
            if(len(param.shape)>=2):
                param=param.T;
            clustGrp.create_dataset(j, data=param);
        
    fout.flush();
    fout.close();
