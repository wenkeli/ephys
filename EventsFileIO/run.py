import sys;
import os;
from PySide.QtGui import QApplication, QFileDialog;

from events import Events
from exporthdf5 import exportEventsHDF5;
from loadopenephysevents import readEventFile;

if __name__ =="__main__":
    app=QApplication(sys.argv);
    
    fileName=QFileDialog.getOpenFileName(None, "open events file", 
                                         "", "events file (*.events)");
    fileName=fileName[0];
    if(fileName==""):
        exit(0);
    
    fName, fExt=os.path.splitext(fileName);
     
    data=readEventFile(fileName);
    events=Events(data["timestamps"], data["eventChs"], data["eventIDs"]);
    exportEventsHDF5(fName+".h5", events);
    
