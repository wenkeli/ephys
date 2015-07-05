# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reportw.ui'
#
# Created: Sun Jul  5 17:02:52 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ReportW(object):
    def setupUi(self, ReportW):
        ReportW.setObjectName("ReportW")
        ReportW.resize(1002, 391)
        self.reportDisp = QtGui.QTextEdit(ReportW)
        self.reportDisp.setGeometry(QtCore.QRect(0, 0, 1001, 391))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(11)
        font.setItalic(False)
        self.reportDisp.setFont(font)
        self.reportDisp.setReadOnly(True)
        self.reportDisp.setTabStopWidth(30)
        self.reportDisp.setAcceptRichText(False)
        self.reportDisp.setObjectName("reportDisp")

        self.retranslateUi(ReportW)
        QtCore.QMetaObject.connectSlotsByName(ReportW)

    def retranslateUi(self, ReportW):
        ReportW.setWindowTitle(QtGui.QApplication.translate("ReportW", "cluster report", None, QtGui.QApplication.UnicodeUTF8))

