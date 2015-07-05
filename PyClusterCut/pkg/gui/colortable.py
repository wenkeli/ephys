import pyqtgraph as pg;
from PySide.QtGui import QBrush, QColor;

class ColorTable(object):
    def __init__(self):
        self.__colors=[];
        self.__pens=[];
        self.__brushes=[];
        
        self.__curColorInd=0;
        
        self.__colors.append(pg.mkColor("#FF00FF")); #magenta
        self.__colors.append(pg.mkColor("#00FFFF")); #cyan
        self.__colors.append(pg.mkColor("#00FF00")); #lime
        self.__colors.append(pg.mkColor("#FFFF00")); #yellow
        self.__colors.append(pg.mkColor("#B041FF")); #purple daffadil
        self.__colors.append(pg.mkColor("#F87217")); #pumpkin orange
        self.__colors.append(pg.mkColor("#3BB9FF")); #deep sky blue
        self.__colors.append(pg.mkColor("#7FFFD4")); #aquamarine
        self.__colors.append(pg.mkColor("#87F717")); #lawn green
        self.__colors.append(pg.mkColor("#FDD017")); #bright gold
        self.__colors.append(pg.mkColor("#F660AB")); #hot pink
        self.__colors.append(pg.mkColor("#FF0000")); #red
        
        for color in self.__colors:
            self.__pens.append(pg.mkPen(color));
            brushColor=QColor(color);
            brushColor.setAlphaF(0.8);
            self.__brushes.append(QBrush(brushColor));
            
    def getCurColor(self):
        curPen=self.__pens[self.__curColorInd];
        curColor=self.__colors[self.__curColorInd];
        curBrush=self.__brushes[self.__curColorInd];
        
        self.__curColorInd=(self.__curColorInd+1)%len(self.__pens);
        return (curColor, curPen, curBrush);