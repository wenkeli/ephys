# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reportw.ui'
#
# Created: Thu May 14 22:19:12 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ReportW(object):
    def setupUi(self, ReportW):
        ReportW.setObjectName("ReportW")
        ReportW.resize(823, 463)
        self.reportDisp = QtGui.QTextEdit(ReportW)
        self.reportDisp.setGeometry(QtCore.QRect(0, 10, 821, 451))
        self.reportDisp.setReadOnly(True)
        self.reportDisp.setAcceptRichText(False)
        self.reportDisp.setObjectName("reportDisp")

        self.retranslateUi(ReportW)
        QtCore.QMetaObject.connectSlotsByName(ReportW)

    def retranslateUi(self, ReportW):
        ReportW.setWindowTitle(QtGui.QApplication.translate("ReportW", "cluster report", None, QtGui.QApplication.UnicodeUTF8))

