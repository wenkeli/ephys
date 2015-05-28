from events import Events;
import h5py;
import numpy as np;

def exportEventsHDF5(fileName, events):
    fout=h5py.File(fileName, "w");
    
    chInds=events.getChs();
    
    for i in chInds:
        fout.create_dataset(i, data=events.getChTimes(i));
        
    fout.flush();
    fout.close();
