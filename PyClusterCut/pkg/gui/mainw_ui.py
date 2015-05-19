# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainw.ui'
#
# Created: Tue May 19 00:03:47 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainW(object):
    def setupUi(self, MainW):
        MainW.setObjectName("MainW")
        MainW.resize(261, 746)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainW.sizePolicy().hasHeightForWidth())
        MainW.setSizePolicy(sizePolicy)
        MainW.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.openFileButton = QtGui.QPushButton(MainW)
        self.openFileButton.setGeometry(QtCore.QRect(10, 10, 84, 21))
        self.openFileButton.setObjectName("openFileButton")
        self.saveFileButton = QtGui.QPushButton(MainW)
        self.saveFileButton.setGeometry(QtCore.QRect(170, 10, 84, 21))
        self.saveFileButton.setObjectName("saveFileButton")
        self.hParamSelect = QtGui.QListWidget(MainW)
        self.hParamSelect.setGeometry(QtCore.QRect(130, 90, 121, 101))
        self.hParamSelect.setObjectName("hParamSelect")
        self.hChannelSelect = QtGui.QListWidget(MainW)
        self.hChannelSelect.setGeometry(QtCore.QRect(30, 90, 61, 101))
        self.hChannelSelect.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.hChannelSelect.setObjectName("hChannelSelect")
        self.vChannelSelect = QtGui.QListWidget(MainW)
        self.vChannelSelect.setGeometry(QtCore.QRect(30, 200, 61, 101))
        self.vChannelSelect.setObjectName("vChannelSelect")
        self.vParamSelect = QtGui.QListWidget(MainW)
        self.vParamSelect.setGeometry(QtCore.QRect(130, 200, 121, 101))
        self.vParamSelect.setObjectName("vParamSelect")
        self.workClusterSelect = QtGui.QListWidget(MainW)
        self.workClusterSelect.setGeometry(QtCore.QRect(20, 350, 61, 151))
        self.workClusterSelect.setObjectName("workClusterSelect")
        self.viewClustersSelect = QtGui.QListWidget(MainW)
        self.viewClustersSelect.setGeometry(QtCore.QRect(170, 350, 61, 151))
        self.viewClustersSelect.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.viewClustersSelect.setObjectName("viewClustersSelect")
        self.chLabel = QtGui.QLabel(MainW)
        self.chLabel.setGeometry(QtCore.QRect(30, 70, 51, 16))
        self.chLabel.setObjectName("chLabel")
        self.hLabel = QtGui.QLabel(MainW)
        self.hLabel.setGeometry(QtCore.QRect(10, 130, 16, 16))
        self.hLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.hLabel.setObjectName("hLabel")
        self.vLabel = QtGui.QLabel(MainW)
        self.vLabel.setGeometry(QtCore.QRect(10, 240, 16, 16))
        self.vLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.vLabel.setObjectName("vLabel")
        self.paramLabel = QtGui.QLabel(MainW)
        self.paramLabel.setGeometry(QtCore.QRect(150, 70, 71, 20))
        self.paramLabel.setObjectName("paramLabel")
        self.viewingClusterLabel = QtGui.QLabel(MainW)
        self.viewingClusterLabel.setGeometry(QtCore.QRect(170, 310, 61, 41))
        self.viewingClusterLabel.setWordWrap(True)
        self.viewingClusterLabel.setObjectName("viewingClusterLabel")
        self.workingClusterLabel = QtGui.QLabel(MainW)
        self.workingClusterLabel.setGeometry(QtCore.QRect(30, 310, 51, 41))
        self.workingClusterLabel.setWordWrap(True)
        self.workingClusterLabel.setMargin(0)
        self.workingClusterLabel.setObjectName("workingClusterLabel")
        self.viewButton = QtGui.QPushButton(MainW)
        self.viewButton.setGeometry(QtCore.QRect(190, 600, 41, 25))
        self.viewButton.setObjectName("viewButton")
        self.quitButton = QtGui.QPushButton(MainW)
        self.quitButton.setGeometry(QtCore.QRect(0, 720, 63, 21))
        self.quitButton.setObjectName("quitButton")
        self.addButton = QtGui.QPushButton(MainW)
        self.addButton.setGeometry(QtCore.QRect(30, 570, 41, 25))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setItalic(False)
        font.setBold(False)
        self.addButton.setFont(font)
        self.addButton.setObjectName("addButton")
        self.refineButton = QtGui.QPushButton(MainW)
        self.refineButton.setGeometry(QtCore.QRect(180, 570, 41, 25))
        self.refineButton.setObjectName("refineButton")
        self.copyButton = QtGui.QPushButton(MainW)
        self.copyButton.setGeometry(QtCore.QRect(140, 600, 41, 25))
        self.copyButton.setObjectName("copyButton")
        self.deleteButton = QtGui.QPushButton(MainW)
        self.deleteButton.setGeometry(QtCore.QRect(130, 570, 41, 25))
        self.deleteButton.setObjectName("deleteButton")
        self.clearWavePlotsButton = QtGui.QPushButton(MainW)
        self.clearWavePlotsButton.setGeometry(QtCore.QRect(120, 540, 41, 25))
        self.clearWavePlotsButton.setObjectName("clearWavePlotsButton")
        self.reportClusterButton = QtGui.QPushButton(MainW)
        self.reportClusterButton.setGeometry(QtCore.QRect(90, 600, 41, 25))
        self.reportClusterButton.setObjectName("reportClusterButton")
        self.nextWavesButton = QtGui.QPushButton(MainW)
        self.nextWavesButton.setGeometry(QtCore.QRect(70, 540, 41, 25))
        self.nextWavesButton.setObjectName("nextWavesButton")
        self.undoButton = QtGui.QPushButton(MainW)
        self.undoButton.setGeometry(QtCore.QRect(40, 600, 41, 25))
        self.undoButton.setObjectName("undoButton")
        self.prevWavesButton = QtGui.QPushButton(MainW)
        self.prevWavesButton.setGeometry(QtCore.QRect(20, 540, 41, 25))
        self.prevWavesButton.setObjectName("prevWavesButton")
        self.resetWaveNButton = QtGui.QPushButton(MainW)
        self.resetWaveNButton.setGeometry(QtCore.QRect(170, 540, 41, 25))
        self.resetWaveNButton.setObjectName("resetWaveNButton")
        self.numWavesIncBox = QtGui.QSpinBox(MainW)
        self.numWavesIncBox.setGeometry(QtCore.QRect(90, 510, 101, 22))
        self.numWavesIncBox.setObjectName("numWavesIncBox")
        self.timeSelEndBox = QtGui.QSpinBox(MainW)
        self.timeSelEndBox.setGeometry(QtCore.QRect(60, 690, 131, 22))
        self.timeSelEndBox.setObjectName("timeSelEndBox")
        self.timeSelStartBox = QtGui.QSpinBox(MainW)
        self.timeSelStartBox.setGeometry(QtCore.QRect(60, 660, 131, 22))
        self.timeSelStartBox.setObjectName("timeSelStartBox")
        self.timeSelButton = QtGui.QPushButton(MainW)
        self.timeSelButton.setGeometry(QtCore.QRect(200, 670, 61, 41))
        self.timeSelButton.setObjectName("timeSelButton")
        self.timeSelLabel = QtGui.QLabel(MainW)
        self.timeSelLabel.setGeometry(QtCore.QRect(90, 640, 91, 16))
        self.timeSelLabel.setObjectName("timeSelLabel")
        self.timeSelStartLabel = QtGui.QLabel(MainW)
        self.timeSelStartLabel.setGeometry(QtCore.QRect(20, 660, 31, 21))
        self.timeSelStartLabel.setObjectName("timeSelStartLabel")
        self.timeSelEndLabel = QtGui.QLabel(MainW)
        self.timeSelEndLabel.setGeometry(QtCore.QRect(20, 690, 31, 21))
        self.timeSelEndLabel.setObjectName("timeSelEndLabel")
        self.label_4 = QtGui.QLabel(MainW)
        self.label_4.setGeometry(QtCore.QRect(10, 510, 81, 21))
        self.label_4.setObjectName("label_4")

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
        QtCore.QObject.connect(self.viewClustersSelect, QtCore.SIGNAL("itemSelectionChanged()"), MainW.viewClustersChanged)
        QtCore.QObject.connect(self.deleteButton, QtCore.SIGNAL("clicked()"), MainW.deleteCluster)
        QtCore.QObject.connect(self.copyButton, QtCore.SIGNAL("clicked()"), MainW.copyCluster)
        QtCore.QObject.connect(self.reportClusterButton, QtCore.SIGNAL("clicked()"), MainW.showReport)
        QtCore.QObject.connect(self.prevWavesButton, QtCore.SIGNAL("clicked()"), MainW.drawPrevWaves)
        QtCore.QObject.connect(self.nextWavesButton, QtCore.SIGNAL("clicked()"), MainW.drawNextWaves)
        QtCore.QObject.connect(self.clearWavePlotsButton, QtCore.SIGNAL("clicked()"), MainW.clearWavePlots)
        QtCore.QObject.connect(self.resetWaveNButton, QtCore.SIGNAL("clicked()"), MainW.resetWaveInd)
        QtCore.QObject.connect(self.timeSelButton, QtCore.SIGNAL("clicked()"), MainW.selectTimeWindow)
        QtCore.QObject.connect(self.saveFileButton, QtCore.SIGNAL("clicked()"), MainW.saveClusterData)
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
        self.refineButton.setText(QtGui.QApplication.translate("MainW", "reFine", None, QtGui.QApplication.UnicodeUTF8))
        self.copyButton.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>add a cluster from the currently selected work cluster with points in the boundary, but also keep the points in the parent cluster also</p><p>keyboard shortcut: C</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.copyButton.setText(QtGui.QApplication.translate("MainW", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>delete the selected working cluster, all the points will be returned to the parent cluster that the cluster was created from.</p><p>keyboard shortcut: D</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("MainW", "Delet", None, QtGui.QApplication.UnicodeUTF8))
        self.clearWavePlotsButton.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>clear the waveform view window</p><p>Keyboard shortcut: E</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.clearWavePlotsButton.setText(QtGui.QApplication.translate("MainW", "clEar", None, QtGui.QApplication.UnicodeUTF8))
        self.reportClusterButton.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>produce a report of cluster overlaps, click again to high window</p><p>Keyboard shortcut: X</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.reportClusterButton.setText(QtGui.QApplication.translate("MainW", "Reprt", None, QtGui.QApplication.UnicodeUTF8))
        self.nextWavesButton.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>View the next 100 waveforms of the working cluster</p><p>Keyboard shortcut: W</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.nextWavesButton.setText(QtGui.QApplication.translate("MainW", "nWav", None, QtGui.QApplication.UnicodeUTF8))
        self.undoButton.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>undo a step in the boundary selection</p><p>Keyboard shortcut: Z</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.undoButton.setText(QtGui.QApplication.translate("MainW", "Undo", None, QtGui.QApplication.UnicodeUTF8))
        self.prevWavesButton.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>View the previous 100 waveforms of the working cluster</p><p>Keyboard shortcut: Q</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.prevWavesButton.setText(QtGui.QApplication.translate("MainW", "pwav", None, QtGui.QApplication.UnicodeUTF8))
        self.resetWaveNButton.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>produce a report of cluster overlaps, click again to high window</p><p>Keyboard shortcut: X</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.resetWaveNButton.setText(QtGui.QApplication.translate("MainW", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.numWavesIncBox.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>set the number of waves to display each time pwav and nWav buttons are clicked.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.timeSelButton.setText(QtGui.QApplication.translate("MainW", "select", None, QtGui.QApplication.UnicodeUTF8))
        self.timeSelLabel.setToolTip(QtGui.QApplication.translate("MainW", "<html><head/><body><p>select the time window for the samples to be worked on. Press select to set. Once set, cannot be changed.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.timeSelLabel.setText(QtGui.QApplication.translate("MainW", "Time selection", None, QtGui.QApplication.UnicodeUTF8))
        self.timeSelStartLabel.setText(QtGui.QApplication.translate("MainW", "<html><head/><body><p align=\"right\">start</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.timeSelEndLabel.setText(QtGui.QApplication.translate("MainW", "<html><head/><body><p align=\"right\">end</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainW", "num waves", None, QtGui.QApplication.UnicodeUTF8))

