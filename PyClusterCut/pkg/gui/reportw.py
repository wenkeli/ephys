import PySide;

from PySide.QtGui import QWidget;
from PySide.QtCore import Qt;

from reportw_ui import Ui_ReportW;


class ReportW(QWidget, Ui_ReportW):
    def __init__(self, parent=None):
        super(ReportW, self).__init__(parent);
        self.setupUi(self);
        self.setFocusPolicy(Qt.StrongFocus);
        self.setWindowFlags(Qt.CustomizeWindowHint
                            | Qt.WindowMinimizeButtonHint);
        
        self.hide();
        
    def getReportDisp(self):
        return self.reportDisp;