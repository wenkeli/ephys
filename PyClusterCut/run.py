import sys;

from pkg.gui.mainw import MainW;

from PySide.QtGui import QApplication;

if __name__ =="__main__":
    app=QApplication(sys.argv);
    frame=MainW();
    frame.show();
    app.exec_();
