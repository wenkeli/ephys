from PyQt5.QtWidgets import QWidget;
from PyQt5.QtCore import Qt;

from .reportw_ui import Ui_ReportW;

from ..data.dataset import DataSet;


class ReportW(QWidget, Ui_ReportW):
    def __init__(self, parent=None):
        super(ReportW, self).__init__(parent);
        self.setupUi(self);
        self.setFocusPolicy(Qt.StrongFocus);
        self.setWindowFlags(Qt.CustomizeWindowHint
                            | Qt.WindowMinimizeButtonHint);
        
        self.hide();
        
    def generateReport(self, dataSet):
        self.reportDisp.clear();
#         self.reportDisp.insertPlainText("testtesttest1234test1234\n");
#         self.reportDisp.insertPlainText("\ttest1\n");
        clustIDs=dataSet.getClusterIDs();
        initClustID=dataSet.getInitClustID();
        clustIDs.remove(initClustID);
        
        output="clusters: ";
        for i in clustIDs:
            output=output+str(i)+" ";
        output=output+"\n";
        self.reportDisp.insertPlainText(output);
        
        for i in clustIDs:
            (numPoints, numOverlap)=dataSet.computeClusterOverlap(i);
            percOverlap=int(numOverlap/float(numPoints)*1000);
            percOverlap=percOverlap/10.0;
            rating=dataSet.getCluster(i).getRating();
            output="cluster "+str(i)+": rating "+str(rating)+", "+str(numPoints)+" pts, overlap: "+str(numOverlap)+" pts, "+str(percOverlap)+"%\n";
            self.reportDisp.insertPlainText(output);
            for j in clustIDs:
                if(i==j):
                    continue;
                (numPoints, numOverlap)=dataSet.compareClustersOverlap(i, j);
                percOverlap=int(numOverlap/float(numPoints)*1000);
                percOverlap=percOverlap/10.0;
                if(numOverlap<=0):
                    continue;
                output="\toverlap cluster "+str(j)+": "+str(numOverlap)+" pts, "+str(percOverlap)+"%\n";
                self.reportDisp.insertPlainText(output);
            self.reportDisp.insertPlainText("\n");