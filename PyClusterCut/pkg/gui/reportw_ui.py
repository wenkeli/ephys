# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reportw.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ReportW(object):
    def setupUi(self, ReportW):
        ReportW.setObjectName("ReportW")
        ReportW.resize(1002, 391)
        self.reportDisp = QtWidgets.QTextEdit(ReportW)
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
        _translate = QtCore.QCoreApplication.translate
        ReportW.setWindowTitle(_translate("ReportW", "cluster report"))

