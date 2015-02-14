# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainw.ui'
#
# Created: Sat Feb 14 11:34:33 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainW(object):
    def setupUi(self, MainW):
        MainW.setObjectName("MainW")
        MainW.resize(261, 781)
        MainW.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.openFileButton = QtGui.QPushButton(MainW)
        self.openFileButton.setGeometry(QtCore.QRect(10, 10, 84, 25))
        self.openFileButton.setObjectName("openFileButton")
        self.saveFileButton = QtGui.QPushButton(MainW)
        self.saveFileButton.setGeometry(QtCore.QRect(170, 10, 84, 25))
        self.saveFileButton.setObjectName("saveFileButton")
        self.hParamSelect = QtGui.QListWidget(MainW)
        self.hParamSelect.setGeometry(QtCore.QRect(130, 80, 121, 141))
        self.hParamSelect.setObjectName("hParamSelect")
        self.hChannelSelect = QtGui.QListWidget(MainW)
        self.hChannelSelect.setGeometry(QtCore.QRect(30, 80, 61, 141))
        self.hChannelSelect.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.hChannelSelect.setObjectName("hChannelSelect")
        self.vChannelSelect = QtGui.QListWidget(MainW)
        self.vChannelSelect.setGeometry(QtCore.QRect(30, 230, 61, 141))
        self.vChannelSelect.setObjectName("vChannelSelect")
        self.vParamSelect = QtGui.QListWidget(MainW)
        self.vParamSelect.setGeometry(QtCore.QRect(130, 230, 121, 141))
        self.vParamSelect.setObjectName("vParamSelect")
        self.workClusterSelect = QtGui.QListWidget(MainW)
        self.workClusterSelect.setGeometry(QtCore.QRect(20, 440, 61, 141))
        self.workClusterSelect.setObjectName("workClusterSelect")
        self.viewClustersSelect = QtGui.QListWidget(MainW)
        self.viewClustersSelect.setGeometry(QtCore.QRect(170, 440, 61, 141))
        self.viewClustersSelect.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.viewClustersSelect.setObjectName("viewClustersSelect")
        self.chLabel = QtGui.QLabel(MainW)
        self.chLabel.setGeometry(QtCore.QRect(30, 60, 51, 16))
        self.chLabel.setObjectName("chLabel")
        self.hLabel = QtGui.QLabel(MainW)
        self.hLabel.setGeometry(QtCore.QRect(10, 140, 16, 16))
        self.hLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.hLabel.setObjectName("hLabel")
        self.vLabel = QtGui.QLabel(MainW)
        self.vLabel.setGeometry(QtCore.QRect(10, 290, 16, 16))
        self.vLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.vLabel.setObjectName("vLabel")
        self.paramLabel = QtGui.QLabel(MainW)
        self.paramLabel.setGeometry(QtCore.QRect(150, 60, 71, 20))
        self.paramLabel.setObjectName("paramLabel")
        self.viewingClusterLabel = QtGui.QLabel(MainW)
        self.viewingClusterLabel.setGeometry(QtCore.QRect(170, 400, 61, 41))
        self.viewingClusterLabel.setWordWrap(True)
        self.viewingClusterLabel.setObjectName("viewingClusterLabel")
        self.workingClusterLabel = QtGui.QLabel(MainW)
        self.workingClusterLabel.setGeometry(QtCore.QRect(30, 400, 51, 41))
        self.workingClusterLabel.setWordWrap(True)
        self.workingClusterLabel.setMargin(0)
        self.workingClusterLabel.setObjectName("workingClusterLabel")
        self.viewButton = QtGui.QPushButton(MainW)
        self.viewButton.setGeometry(QtCore.QRect(190, 670, 41, 25))
        self.viewButton.setObjectName("viewButton")
        self.quitButton = QtGui.QPushButton(MainW)
        self.quitButton.setGeometry(QtCore.QRect(0, 761, 63, 21))
        self.quitButton.setObjectName("quitButton")
        self.addButton = QtGui.QPushButton(MainW)
        self.addButton.setGeometry(QtCore.QRect(10, 640, 41, 25))
        self.addButton.setObjectName("addButton")
        self.refineButton = QtGui.QPushButton(MainW)
        self.refineButton.setGeometry(QtCore.QRect(170, 610, 41, 25))
        self.refineButton.setObjectName("refineButton")
        self.copyButton = QtGui.QPushButton(MainW)
        self.copyButton.setGeometry(QtCore.QRect(140, 670, 41, 25))
        self.copyButton.setObjectName("copyButton")
        self.deleteButton = QtGui.QPushButton(MainW)
        self.deleteButton.setGeometry(QtCore.QRect(180, 640, 41, 25))
        self.deleteButton.setObjectName("deleteButton")

        self.retranslateUi(MainW)
        QtCore.QObject.connect(self.openFileButton, QtCore.SIGNAL("clicked()"), MainW.loadFile)
        QtCore.QObject.connect(self.viewButton, QtCore.SIGNAL("clicked()"), MainW.updatePlotView)
        QtCore.QObject.connect(self.quitButton, QtCore.SIGNAL("clicked()"), MainW.quit)
        QtCore.QObject.connect(self.addButton, QtCore.SIGNAL("clicked()"), MainW.addCluster)
        QtCore.QObject.connect(self.refineButton, QtCore.SIGNAL("clicked()"), MainW.refineCluster)
        QtCore.QObject.connect(self.workClusterSelect, QtCore.SIGNAL("itemSelectionChanged()"), MainW.changeWorkCluster)
        QtCore.QObject.connect(self.hChannelSelect, QtCore.SIGNAL("itemSelectionChanged()"), MainW.invalidateView)
        QtCore.QObject.connect(self.vChannelSelect, QtCore.SIGNAL("itemSelectionChanged()"), MainW.invalidateView)
        QtCore.QObject.connect(self.hParamSelect, QtCore.SIGNAL("itemSelectionChanged()"), MainW.invalidateView)
        QtCore.QObject.connect(self.vParamSelect, QtCore.SIGNAL("itemSelectionChanged()"), MainW.invalidateView)
        QtCore.QObject.connect(self.viewClustersSelect, QtCore.SIGNAL("itemSelectionChanged()"), MainW.invalidateView)
        QtCore.QObject.connect(self.deleteButton, QtCore.SIGNAL("clicked()"), MainW.deleteCluster)
        QtCore.QObject.connect(self.copyButton, QtCore.SIGNAL("clicked()"), MainW.copyCluster)
        QtCore.QMetaObject.connectSlotsByName(MainW)

    def retranslateUi(self, MainW):
        MainW.setWindowTitle(QtGui.QApplication.translate("MainW", "control", None, QtGui.QApplication.UnicodeUTF8))
        self.openFileButton.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>load a data file</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.openFileButton.setText(QtGui.QApplication.translate("MainW", "load file", None, QtGui.QApplication.UnicodeUTF8))
        self.saveFileButton.setText(QtGui.QApplication.translate("MainW", "save file", None, QtGui.QApplication.UnicodeUTF8))
        self.hParamSelect.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>select the parameter to display on the horizontal axis</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.hChannelSelect.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>select the channel to display on the horizontal axis</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.vChannelSelect.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>select the channel to display on the vertical axis</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.vParamSelect.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>select the parameter to display on the vertical axis</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.workClusterSelect.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>select the working cluster</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.viewClustersSelect.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>select the clusters to view</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.chLabel.setText(QtGui.QApplication.translate("MainW", "channel", None, QtGui.QApplication.UnicodeUTF8))
        self.hLabel.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>horizontal axis</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.hLabel.setText(QtGui.QApplication.translate("MainW", "H", None, QtGui.QApplication.UnicodeUTF8))
        self.vLabel.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>vertical axis</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.vLabel.setText(QtGui.QApplication.translate("MainW", "V", None, QtGui.QApplication.UnicodeUTF8))
        self.paramLabel.setText(QtGui.QApplication.translate("MainW", "parameter", None, QtGui.QApplication.UnicodeUTF8))
        self.viewingClusterLabel.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>the clusters that are displayed</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.viewingClusterLabel.setText(QtGui.QApplication.translate("MainW", "<html><head/><body><p align=\"center\">viewing clusters</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.workingClusterLabel.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>the cluster that the cluster operations (add, delete, refine, copy) apply to</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.workingClusterLabel.setText(QtGui.QApplication.translate("MainW", "<html><head/><body><p align=\"center\">working cluster</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.viewButton.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>update the data viewed in the plot window</p><p>keyboard shortcut: V</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.viewButton.setText(QtGui.QApplication.translate("MainW", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.quitButton.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>exit the application</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.quitButton.setText(QtGui.QApplication.translate("MainW", "quit", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>add a cluster from the selected working cluster with the points in the boundary.</p><p>Keyboard shortcut: A</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("MainW", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.refineButton.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>refine the selected working cluster with points in the boundaries, All the points outside of the boundary is returned to the parent cluster that the cluster was created from.</p><p>keyboard shortcut: R</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.refineButton.setText(QtGui.QApplication.translate("MainW", "Refine", None, QtGui.QApplication.UnicodeUTF8))
        self.copyButton.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>add a cluster from the currently selected work cluster with points in the boundary, but also keep the points in the parent cluster also</p><p>keyboard shortcut: C</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.copyButton.setText(QtGui.QApplication.translate("MainW", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>delete the selected working cluster, all the points will be returned to the parent cluster that the cluster was created from.</p><p>keyboard shortcut: D</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("MainW", "Delet", None, QtGui.QApplication.UnicodeUTF8))

