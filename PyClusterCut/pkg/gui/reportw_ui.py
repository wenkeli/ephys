# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reportw.ui'
#
# Created: Mon May 18 14:43:21 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ReportW(object):
    def setupUi(self, ReportW):
        ReportW.setObjectName("ReportW")
        ReportW.resize(502, 330)
        self.reportDisp = QtGui.QTextEdit(ReportW)
        self.reportDisp.setGeometry(QtCore.QRect(0, 0, 501, 321))
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(12)
        self.reportDisp.setFont(font)
        self.reportDisp.setReadOnly(True)
        self.reportDisp.setTabStopWidth(30)
        self.reportDisp.setAcceptRichText(False)
        self.reportDisp.setObjectName("reportDisp")

        self.retranslateUi(ReportW)
        QtCore.QMetaObject.connectSlotsByName(ReportW)

    def retranslateUi(self, ReportW):
        ReportW.setWindowTitle(QtGui.QApplication.translate("ReportW", "cluster report", None, QtGui.QApplication.UnicodeUTF8))

