from collections import deque
from itertools import repeat
try:
    from itertools import imap
except ImportError:
    imap = map

import numpy as np

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph.functions as fn
from pyqtgraph.graphicsItems.GraphicsObject import GraphicsObject
import pyqtgraph.debug as debug
from pyqtgraph.graphicsItems.ScatterPlotItem import renderSymbol, Symbols
import pyqtgraph as pg

__all__ = ['FastScatterPlotItem']


class Symbol(object):

    def __init__(self, pen='l', brush='s', symbol='o', size=7):
        self.size = size
        self.symbol = symbol
        
        if isinstance(pen,QtGui.QPen):
            self.pen = pen
        else:
            self.pen = fn.mkPen(pen)

        if isinstance(brush,QtGui.QBrush):
            self.brush = brush
        else:
            self.brush = fn.mkBrush(brush)
        
        self.pixmap = QtGui.QPixmap(renderSymbol(self.symbol, self.size, self.pen, self.brush))
        self.width = self.pixmap.width()

    def __eq__(self, other):
        attribute = ['pen', 'brush', 'symbol', 'size']
        for att in attribute:
            if self.__getattribute__(att) != other.__getattribute__(att):
                return False
        return True


class FastScatterPlotItem(GraphicsObject):
    
    
    def __init__(self, *args, **kargs):
        GraphicsObject.__init__(self)
        self.data = np.empty(0, dtype=[('x', float), ('y', float), ('symbol', np.uint16)])
        self._symbolList = []
        self._unusedSymbol = [] ## index of unused Symbol
        self.pointMode = False ## Draw only point instead of symbol
        self._maxWidth = 0
        self.bounds = [None, None]  ## caches data bounds
        self.setData(*args, **kargs)
        
    def name(self):
        return None;
        
    def setData(self, x, y, pen='l', brush='s', symbol='o', size=7, pointMode=True):
        self.pointMode = pointMode
        self.clear()
        self.bounds = [None, None]
        self.addPoints(x, y, pen, brush, symbol, size)
        self.cleanSymbol()

    def addPoints(self, x, y, pen='l', brush='s', symbol='o', size=7):
        symbol = Symbol(pen, brush, symbol, size)
        i = self._addSymbol(symbol)
        numPts = len(x)
        oldData = self.data
        self.data = np.empty(len(oldData)+numPts, dtype=self.data.dtype)
        self.data[:len(oldData)] = oldData
        newData = self.data[len(oldData):]
        newData['x'] = x
        newData['y'] = y
        newData['symbol'] = i
        self.bounds = [None, None]
        self.prepareGeometryChange()
        self.update()

    def _addSymbol(self, symbol):
        """
        Add a symbol to the list of symbol and return the index of the symbol
        """
        try: ## check if the symbol is already there
            i = self._symbolList.index(symbol)
            self._unusedSymbol[i] = False
            return i
        except ValueError:
            self._maxWidth = max(self._maxWidth, symbol.width)
            for i in xrange(len(self._unusedSymbol)):
                if self._unusedSymbol[i]:
                    self._unusedSymbol[i] = False
                    self._symbolList[i] = symbol
                    return i
        self._symbolList.append(symbol)
        self._unusedSymbol.append(True);
        i=len(self._symbolList) - 1
        return i


    def implements(self, interface=None):
        ints = ['plotData']
        if interface is None:
            return ints
        return interface in ints
    
    def clear(self):
        """Remove all spots from the scatter plot"""
        self.data = np.empty(0, dtype=self.data.dtype)
        self._QPoints = []
        self.bounds = [None, None]

    def cleanSymbol(self):
        """Remove unused symbol from the cache"""
        symbol = []
        self._maxWidth = 0
        used = np.unique(self.data['symbol'])
        used.sort() ## to make sure to keep good symbol
        i = 0
        if used.size>0:
            for x in used:
                symbol.append(self._symbolList[x])
                self.data['symbol'][self.data['symbol'] == x] = i
                i += 1
                self._maxWidth = max(self._maxWidth, self._symbolList[x].width)
        self._symbolList = symbol
        self._spriteValid = False

    def dataBounds(self, ax, frac=1.0, orthoRange=None):
        if frac >= 1.0 and orthoRange is None and self.bounds[ax] is not None:
            return self.bounds[ax]
        
        if self.data is None or len(self.data) == 0:
            return (None, None)
        
        if ax == 0:
            d = self.data['x']
            d2 = self.data['y']
        elif ax == 1:
            d = self.data['y']
            d2 = self.data['x']
        
        if orthoRange is not None:
            mask = (d2 >= orthoRange[0]) * (d2 <= orthoRange[1])
            d = d[mask]
            d2 = d2[mask]
            
        if frac >= 1.0:
            self.bounds[ax] = (np.nanmin(d), np.nanmax(d))
            return self.bounds[ax]
        elif frac <= 0.0:
            raise Exception("Value for parameter 'frac' must be > 0. (got %s)" % str(frac))
        else:
            mask = np.isfinite(d)
            d = d[mask]
            return (np.percentile(d, 50 - (frac * 50)), np.percentile(d, 50 + (frac * 50)))
            
    def pixelPadding(self):
        if self.pointMode:
            return 0.7072
        return self._maxWidth*0.7072

    def boundingRect(self):
        (xmn, xmx) = self.dataBounds(ax=0)
        (ymn, ymx) = self.dataBounds(ax=1)
        if xmn is None or xmx is None:
            xmn = 0
            xmx = 0
        if ymn is None or ymx is None:
            ymn = 0
            ymx = 0
        
        px = py = 0.0
        pxPad = self.pixelPadding()
        if pxPad > 0:
            # determine length of pixel in local x, y directions    
            px, py = self.pixelVectors()
            px = 0 if px is None else px.length() 
            py = 0 if py is None else py.length()
            
            # return bounds expanded by pixel size
            px *= pxPad
            py *= pxPad
        return QtCore.QRectF(xmn-px, ymn-py, (2*px)+xmx-xmn, (2*py)+ymx-ymn)

    def viewTransformChanged(self):
        self.prepareGeometryChange()
        GraphicsObject.viewTransformChanged(self)
        self.bounds = [None, None]
        self.fragments = None

    def setExportMode(self, *args, **kwds):
        GraphicsObject.setExportMode(self, *args, **kwds)
        self.invalidate()
        
    @debug.warnOnException  ## raising an exception here causes crash
    def paint(self, p, *args):
        
        if self._exportOpts is not False:
            aa = self._exportOpts.get('antialias', True)
            scale = self._exportOpts.get('resolutionScale', 1.0)  ## exporting to image; pixel resolution may have changed
        else:
            aa = True #self.opts['antialias']
            scale = 1.0
        
        p.setRenderHint(p.Antialiasing, aa)
        p.resetTransform()
        tr = self.deviceTransform()
        if tr is None:
            return
        range = self.getViewBox().viewRange()
        mask = np.logical_and(
               np.logical_and(self.data['x'] > range[0][0],
                              self.data['x'] < range[0][1]), 
               np.logical_and(self.data['y'] > range[1][0],
                              self.data['y'] < range[1][1])) ## remove out of view points 
        data = self.data[mask]
        pts = np.empty((2,len(data['x'])))
        pts[0] = data['x']
        pts[1] = data['y']
        pts = fn.transformCoordinates(tr, pts)

        for i in xrange(len(self._symbolList)):
            mask = data['symbol'] == i
            if self.pointMode:
                p.setPen(self._symbolList[i].pen)
                list(imap(p.drawPoint, pts[0,mask], pts[1,mask]))
            else:
                x = pts[0,mask] - self._symbolList[i].width/2.0
                y = pts[1,mask] - self._symbolList[i].width/2.0
                list(imap(p.drawPixmap, x, y, 
                    repeat(self._symbolList[i].pixmap)))
