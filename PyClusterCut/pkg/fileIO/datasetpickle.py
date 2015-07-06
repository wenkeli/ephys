import cPickle as pickle;
from ..data.dataset import DataSet;

def saveDataSetPickle(fileName, dataSet):
    fout=open(fileName, "wb");
    pickle.dump(dataSet, fout, protocol=2);
    fout.close();
    
def loadDataSetPickle(fileName):
    fin=open(fileName, "rb");
    dataSet=pickle.load(fin);
    fin.close();
    return dataSet;