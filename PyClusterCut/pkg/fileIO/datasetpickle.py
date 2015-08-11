import cPickle as pickle;
from ..data.dataset import DataSet;
from ..data.samples import SamplesData;

def saveDataSetPickle(fileName, dataSet):
    fout=open(fileName, "wb");
    pickle.dump(dataSet, fout, protocol=2);
    fout.close();
    
def loadDataSetPickle(fileName):
    fin=open(fileName, "rb");
    dataSet=pickle.load(fin);
    fin.close();
    
    paramNames=dataSet.getSamples().getParamNames();
    if(not ("peakFallAngle" in paramNames)):
        dataSet.getSamples().calcPeakFallAngle();
    if(not ("peakMax" in paramNames)):
        dataSet.getSamples().calcPeakMax();
        
    return dataSet;