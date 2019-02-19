# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainw.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainW(object):
    def setupUi(self, MainW):
        MainW.setObjectName("MainW")
        MainW.resize(280, 824)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainW.sizePolicy().hasHeightForWidth())
        MainW.setSizePolicy(sizePolicy)
        MainW.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.openFileButton = QtWidgets.QPushButton(MainW)
        self.openFileButton.setGeometry(QtCore.QRect(10, 0, 84, 21))
        self.openFileButton.setObjectName("openFileButton")
        self.saveFileButton = QtWidgets.QPushButton(MainW)
        self.saveFileButton.setGeometry(QtCore.QRect(150, 0, 101, 21))
        self.saveFileButton.setObjectName("saveFileButton")
        self.hParamSelect = QtWidgets.QListWidget(MainW)
        self.hParamSelect.setGeometry(QtCore.QRect(120, 80, 141, 111))
        self.hParamSelect.setObjectName("hParamSelect")
        self.hChannelSelect = QtWidgets.QListWidget(MainW)
        self.hChannelSelect.setGeometry(QtCore.QRect(40, 80, 51, 111))
        self.hChannelSelect.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.hChannelSelect.setObjectName("hChannelSelect")
        self.vChannelSelect = QtWidgets.QListWidget(MainW)
        self.vChannelSelect.setGeometry(QtCore.QRect(40, 195, 51, 111))
        self.vChannelSelect.setObjectName("vChannelSelect")
        self.vParamSelect = QtWidgets.QListWidget(MainW)
        self.vParamSelect.setGeometry(QtCore.QRect(120, 195, 141, 111))
        self.vParamSelect.setObjectName("vParamSelect")
        self.workClusterSelect = QtWidgets.QListWidget(MainW)
        self.workClusterSelect.setGeometry(QtCore.QRect(20, 360, 71, 151))
        self.workClusterSelect.setObjectName("workClusterSelect")
        self.viewClustersSelect = QtWidgets.QListWidget(MainW)
        self.viewClustersSelect.setGeometry(QtCore.QRect(120, 360, 71, 151))
        self.viewClustersSelect.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.viewClustersSelect.setObjectName("viewClustersSelect")
        self.chLabel = QtWidgets.QLabel(MainW)
        self.chLabel.setGeometry(QtCore.QRect(30, 60, 61, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.chLabel.setFont(font)
        self.chLabel.setObjectName("chLabel")
        self.hLabel = QtWidgets.QLabel(MainW)
        self.hLabel.setGeometry(QtCore.QRect(9, 80, 21, 111))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.hLabel.setFont(font)
        self.hLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.hLabel.setObjectName("hLabel")
        self.vLabel = QtWidgets.QLabel(MainW)
        self.vLabel.setGeometry(QtCore.QRect(9, 200, 21, 101))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.vLabel.setFont(font)
        self.vLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.vLabel.setObjectName("vLabel")
        self.paramLabel = QtWidgets.QLabel(MainW)
        self.paramLabel.setGeometry(QtCore.QRect(130, 60, 121, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.paramLabel.setFont(font)
        self.paramLabel.setObjectName("paramLabel")
        self.viewingClusterLabel = QtWidgets.QLabel(MainW)
        self.viewingClusterLabel.setGeometry(QtCore.QRect(120, 320, 61, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.viewingClusterLabel.setFont(font)
        self.viewingClusterLabel.setWordWrap(True)
        self.viewingClusterLabel.setObjectName("viewingClusterLabel")
        self.workingClusterLabel = QtWidgets.QLabel(MainW)
        self.workingClusterLabel.setGeometry(QtCore.QRect(30, 320, 61, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.workingClusterLabel.setFont(font)
        self.workingClusterLabel.setWordWrap(True)
        self.workingClusterLabel.setObjectName("workingClusterLabel")
        self.viewButton = QtWidgets.QPushButton(MainW)
        self.viewButton.setGeometry(QtCore.QRect(180, 610, 41, 25))
        self.viewButton.setStyleSheet("font: 9pt \"Noto Sans\";")
        self.viewButton.setObjectName("viewButton")
        self.quitButton = QtWidgets.QPushButton(MainW)
        self.quitButton.setGeometry(QtCore.QRect(0, 800, 63, 21))
        self.quitButton.setObjectName("quitButton")
        self.addButton = QtWidgets.QPushButton(MainW)
        self.addButton.setGeometry(QtCore.QRect(20, 580, 41, 25))
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.addButton.setFont(font)
        self.addButton.setStyleSheet("font: 9pt \"Noto Sans\";")
        self.addButton.setObjectName("addButton")
        self.refineButton = QtWidgets.QPushButton(MainW)
        self.refineButton.setGeometry(QtCore.QRect(170, 580, 41, 25))
        self.refineButton.setStyleSheet("font: 9pt \"Noto Sans\";")
        self.refineButton.setObjectName("refineButton")
        self.copyButton = QtWidgets.QPushButton(MainW)
        self.copyButton.setGeometry(QtCore.QRect(70, 580, 41, 25))
        self.copyButton.setStyleSheet("font: 9pt \"Noto Sans\";")
        self.copyButton.setObjectName("copyButton")
        self.deleteButton = QtWidgets.QPushButton(MainW)
        self.deleteButton.setGeometry(QtCore.QRect(120, 580, 41, 25))
        self.deleteButton.setStyleSheet("font: 9pt \"Noto Sans\";")
        self.deleteButton.setObjectName("deleteButton")
        self.clearWavePlotsButton = QtWidgets.QPushButton(MainW)
        self.clearWavePlotsButton.setGeometry(QtCore.QRect(110, 550, 41, 25))
        self.clearWavePlotsButton.setStyleSheet("font: 9pt \"Noto Sans\";")
        self.clearWavePlotsButton.setObjectName("clearWavePlotsButton")
        self.reportClusterButton = QtWidgets.QPushButton(MainW)
        self.reportClusterButton.setGeometry(QtCore.QRect(80, 610, 41, 25))
        self.reportClusterButton.setStyleSheet("font: 9pt \"Noto Sans\";")
        self.reportClusterButton.setObjectName("reportClusterButton")
        self.nextWavesButton = QtWidgets.QPushButton(MainW)
        self.nextWavesButton.setGeometry(QtCore.QRect(60, 550, 41, 25))
        self.nextWavesButton.setStyleSheet("font: 9pt \"Noto Sans\";")
        self.nextWavesButton.setObjectName("nextWavesButton")
        self.stepBackBoundButton = QtWidgets.QPushButton(MainW)
        self.stepBackBoundButton.setGeometry(QtCore.QRect(30, 610, 41, 25))
        self.stepBackBoundButton.setStyleSheet("font: 9pt \"Noto Sans\";")
        self.stepBackBoundButton.setObjectName("stepBackBoundButton")
        self.prevWavesButton = QtWidgets.QPushButton(MainW)
        self.prevWavesButton.setGeometry(QtCore.QRect(10, 550, 41, 25))
        self.prevWavesButton.setStyleSheet("font: 9pt \"Noto Sans\";")
        self.prevWavesButton.setObjectName("prevWavesButton")
        self.resetWaveNButton = QtWidgets.QPushButton(MainW)
        self.resetWaveNButton.setGeometry(QtCore.QRect(160, 550, 41, 25))
        self.resetWaveNButton.setStyleSheet("font: 9pt \"Noto Sans\";")
        self.resetWaveNButton.setObjectName("resetWaveNButton")
        self.numWavesIncBox = QtWidgets.QSpinBox(MainW)
        self.numWavesIncBox.setGeometry(QtCore.QRect(80, 520, 71, 22))
        self.numWavesIncBox.setMinimum(1)
        self.numWavesIncBox.setMaximum(100000)
        self.numWavesIncBox.setProperty("value", 100)
        self.numWavesIncBox.setObjectName("numWavesIncBox")
        self.timeSelEndBox = QtWidgets.QSpinBox(MainW)
        self.timeSelEndBox.setGeometry(QtCore.QRect(60, 690, 131, 22))
        self.timeSelEndBox.setMinimum(-1)
        self.timeSelEndBox.setProperty("value", -1)
        self.timeSelEndBox.setObjectName("timeSelEndBox")
        self.timeSelStartBox = QtWidgets.QSpinBox(MainW)
        self.timeSelStartBox.setGeometry(QtCore.QRect(60, 660, 131, 22))
        self.timeSelStartBox.setMinimum(-1)
        self.timeSelStartBox.setProperty("value", -1)
        self.timeSelStartBox.setObjectName("timeSelStartBox")
        self.timeSelButton = QtWidgets.QPushButton(MainW)
        self.timeSelButton.setGeometry(QtCore.QRect(200, 680, 61, 41))
        self.timeSelButton.setObjectName("timeSelButton")
        self.timeSelLabel = QtWidgets.QLabel(MainW)
        self.timeSelLabel.setGeometry(QtCore.QRect(60, 640, 121, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.timeSelLabel.setFont(font)
        self.timeSelLabel.setObjectName("timeSelLabel")
        self.timeSelStartLabel = QtWidgets.QLabel(MainW)
        self.timeSelStartLabel.setGeometry(QtCore.QRect(20, 660, 31, 21))
        self.timeSelStartLabel.setObjectName("timeSelStartLabel")
        self.timeSelEndLabel = QtWidgets.QLabel(MainW)
        self.timeSelEndLabel.setGeometry(QtCore.QRect(20, 690, 31, 21))
        self.timeSelEndLabel.setObjectName("timeSelEndLabel")
        self.numWavesIncLabel = QtWidgets.QLabel(MainW)
        self.numWavesIncLabel.setGeometry(QtCore.QRect(0, 520, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.numWavesIncLabel.setFont(font)
        self.numWavesIncLabel.setObjectName("numWavesIncLabel")
        self.exportDataButton = QtWidgets.QPushButton(MainW)
        self.exportDataButton.setGeometry(QtCore.QRect(150, 30, 101, 21))
        self.exportDataButton.setObjectName("exportDataButton")
        self.exportWavesButton = QtWidgets.QPushButton(MainW)
        self.exportWavesButton.setGeometry(QtCore.QRect(10, 30, 101, 21))
        self.exportWavesButton.setObjectName("exportWavesButton")
        self.viewLargeButton = QtWidgets.QPushButton(MainW)
        self.viewLargeButton.setGeometry(QtCore.QRect(130, 610, 41, 25))
        self.viewLargeButton.setStyleSheet("font: 9pt \"Noto Sans\";")
        self.viewLargeButton.setObjectName("viewLargeButton")
        self.timeResetButton = QtWidgets.QPushButton(MainW)
        self.timeResetButton.setGeometry(QtCore.QRect(210, 650, 41, 21))
        self.timeResetButton.setObjectName("timeResetButton")
        self.clustRateBox = QtWidgets.QSpinBox(MainW)
        self.clustRateBox.setGeometry(QtCore.QRect(200, 410, 51, 31))
        self.clustRateBox.setMinimum(-1)
        self.clustRateBox.setMaximum(5)
        self.clustRateBox.setProperty("value", -1)
        self.clustRateBox.setObjectName("clustRateBox")
        self.clustRatelabel = QtWidgets.QLabel(MainW)
        self.clustRatelabel.setGeometry(QtCore.QRect(200, 360, 61, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.clustRatelabel.setFont(font)
        self.clustRatelabel.setObjectName("clustRatelabel")
        self.undoClustButton = QtWidgets.QPushButton(MainW)
        self.undoClustButton.setGeometry(QtCore.QRect(220, 580, 41, 25))
        self.undoClustButton.setStyleSheet("font: 9pt \"Noto Sans\";")
        self.undoClustButton.setObjectName("undoClustButton")
        self.refWaveChsOnlyBox = QtWidgets.QCheckBox(MainW)
        self.refWaveChsOnlyBox.setGeometry(QtCore.QRect(160, 520, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.refWaveChsOnlyBox.setFont(font)
        self.refWaveChsOnlyBox.setObjectName("refWaveChsOnlyBox")
        self.toggleRefWaveChsButton = QtWidgets.QPushButton(MainW)
        self.toggleRefWaveChsButton.setGeometry(QtCore.QRect(210, 550, 41, 25))
        self.toggleRefWaveChsButton.setStyleSheet("font: 9pt \"Noto Sans\";")
        self.toggleRefWaveChsButton.setObjectName("toggleRefWaveChsButton")
        self.elimOutlierButton = QtWidgets.QPushButton(MainW)
        self.elimOutlierButton.setGeometry(QtCore.QRect(182, 740, 81, 21))
        self.elimOutlierButton.setStyleSheet("font: 9pt \"Noto Sans\";")
        self.elimOutlierButton.setObjectName("elimOutlierButton")
        self.outlierPosThreshBox = QtWidgets.QSpinBox(MainW)
        self.outlierPosThreshBox.setGeometry(QtCore.QRect(60, 770, 111, 22))
        self.outlierPosThreshBox.setMaximum(10000000)
        self.outlierPosThreshBox.setProperty("value", 500)
        self.outlierPosThreshBox.setObjectName("outlierPosThreshBox")
        self.outlierThreshLabel = QtWidgets.QLabel(MainW)
        self.outlierThreshLabel.setGeometry(QtCore.QRect(60, 720, 111, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.outlierThreshLabel.setFont(font)
        self.outlierThreshLabel.setObjectName("outlierThreshLabel")
        self.outlierNegThreshBox = QtWidgets.QSpinBox(MainW)
        self.outlierNegThreshBox.setGeometry(QtCore.QRect(60, 740, 111, 22))
        self.outlierNegThreshBox.setMinimum(-10000000)
        self.outlierNegThreshBox.setMaximum(0)
        self.outlierNegThreshBox.setProperty("value", -200)
        self.outlierNegThreshBox.setObjectName("outlierNegThreshBox")
        self.posThreshLabel = QtWidgets.QLabel(MainW)
        self.posThreshLabel.setGeometry(QtCore.QRect(30, 770, 21, 20))
        self.posThreshLabel.setObjectName("posThreshLabel")
        self.negThreshLabel = QtWidgets.QLabel(MainW)
        self.negThreshLabel.setGeometry(QtCore.QRect(30, 740, 20, 21))
        self.negThreshLabel.setObjectName("negThreshLabel")
        self.finalizeElimOutlierBox = QtWidgets.QPushButton(MainW)
        self.finalizeElimOutlierBox.setGeometry(QtCore.QRect(182, 780, 81, 21))
        self.finalizeElimOutlierBox.setObjectName("finalizeElimOutlierBox")

        self.retranslateUi(MainW)
        self.openFileButton.clicked.connect(MainW.loadFile)
        self.quitButton.clicked.connect(MainW.quit)
        self.addButton.clicked.connect(MainW.addCluster)
        self.refineButton.clicked.connect(MainW.refineCluster)
        self.workClusterSelect.itemSelectionChanged.connect(MainW.changeWorkCluster)
        self.hChannelSelect.itemSelectionChanged.connect(MainW.invalidateView)
        self.vChannelSelect.itemSelectionChanged.connect(MainW.invalidateView)
        self.hParamSelect.itemSelectionChanged.connect(MainW.invalidateView)
        self.vParamSelect.itemSelectionChanged.connect(MainW.invalidateView)
        self.viewClustersSelect.itemSelectionChanged.connect(MainW.viewClustersChanged)
        self.deleteButton.clicked.connect(MainW.deleteCluster)
        self.copyButton.clicked.connect(MainW.copyCluster)
        self.reportClusterButton.clicked.connect(MainW.toggleReport)
        self.prevWavesButton.clicked.connect(MainW.drawPrevWaves)
        self.nextWavesButton.clicked.connect(MainW.drawNextWaves)
        self.clearWavePlotsButton.clicked.connect(MainW.clearWavePlots)
        self.resetWaveNButton.clicked.connect(MainW.resetWaveInd)
        self.timeSelButton.clicked.connect(MainW.selectTimeWindow)
        self.saveFileButton.clicked.connect(MainW.saveClusterData)
        self.exportDataButton.clicked.connect(MainW.exportData)
        self.exportWavesButton.clicked.connect(MainW.exportWaveforms)
        self.viewButton.clicked.connect(MainW.plotPoints)
        self.viewLargeButton.clicked.connect(MainW.plotLargePoints)
        self.timeResetButton.clicked.connect(MainW.resetTimeWindow)
        self.clustRateBox.valueChanged['int'].connect(MainW.updateClustRating)
        self.undoClustButton.clicked.connect(MainW.undoCluster)
        self.stepBackBoundButton.clicked.connect(MainW.stepBackBoundary)
        self.toggleRefWaveChsButton.clicked.connect(MainW.toggleRefWaveChs)
        self.elimOutlierButton.clicked.connect(MainW.eliminateOutliers)
        self.finalizeElimOutlierBox.clicked.connect(MainW.disableElimOutlierUI)
        QtCore.QMetaObject.connectSlotsByName(MainW)

    def retranslateUi(self, MainW):
        _translate = QtCore.QCoreApplication.translate
        MainW.setWindowTitle(_translate("MainW", "control"))
        self.openFileButton.setToolTip(_translate("MainW", "<html><head/><body><p>load a data file. The data file can be an open-ephys .spikes file (version 0.2 and 0.4 compatible), or a .clusterdataset file which is the saved work from this program.</p></body></html>"))
        self.openFileButton.setText(_translate("MainW", "load file"))
        self.saveFileButton.setToolTip(_translate("MainW", "<html><head/><body><p>save the work progress. The file is saved with the extension .clusterdataset, and is saved in the same directory that the data was originally loaded from.</p></body></html>"))
        self.saveFileButton.setText(_translate("MainW", "save file"))
        self.hParamSelect.setToolTip(_translate("MainW", "<html><head/><body><p>select the parameter to display on the horizontal axis. A change in selection here requires pressing the view button to update the view in the plot.</p></body></html>"))
        self.hChannelSelect.setToolTip(_translate("MainW", "<html><head/><body><p>select the channel to display on the horizontal axis. A change in selection here requires pressing the view button to update the view in the plot.</p></body></html>"))
        self.vChannelSelect.setToolTip(_translate("MainW", "<html><head/><body><p>select the channel to display on the vertical axis. A change in selection here requires pressing the view button to update the view in the plot.</p></body></html>"))
        self.vParamSelect.setToolTip(_translate("MainW", "<html><head/><body><p>select the parameter to display on the vertical axis. A change in selection here requires pressing the view button to update the view in the plot.</p></body></html>"))
        self.workClusterSelect.setToolTip(_translate("MainW", "<html><head/><body><p>select the working cluster</p></body></html>"))
        self.viewClustersSelect.setToolTip(_translate("MainW", "<html><head/><body><p>select the clusters to view. A change in the selections here requires pressing the view button to update the view on the plot.</p></body></html>"))
        self.chLabel.setToolTip(_translate("MainW", "<html><head/><body><p>electrode channel number</p></body></html>"))
        self.chLabel.setText(_translate("MainW", "<html><head/><body><p align=\"center\">channel</p></body></html>"))
        self.hLabel.setToolTip(_translate("MainW", "<html><head/><body><p>horizontal axis of the plot</p></body></html>"))
        self.hLabel.setText(_translate("MainW", "H"))
        self.vLabel.setToolTip(_translate("MainW", "<html><head/><body><p>vertical axis of the plot</p></body></html>"))
        self.vLabel.setText(_translate("MainW", "V"))
        self.paramLabel.setToolTip(_translate("MainW", "<html><head/><body><p>parameters for the waveforms</p></body></html>"))
        self.paramLabel.setText(_translate("MainW", "<html><head/><body><p align=\"center\">parameter</p></body></html>"))
        self.viewingClusterLabel.setToolTip(_translate("MainW", "<html><head/><body><p>the clusters that are displayed</p></body></html>"))
        self.viewingClusterLabel.setText(_translate("MainW", "<html><head/><body><p align=\"center\">viewing clusters</p></body></html>"))
        self.workingClusterLabel.setToolTip(_translate("MainW", "<html><head/><body><p>the cluster that the cluster operations (add, delete, refine, copy) apply to</p></body></html>"))
        self.workingClusterLabel.setText(_translate("MainW", "<html><head/><body><p align=\"center\">working cluster</p></body></html>"))
        self.viewButton.setToolTip(_translate("MainW", "<html><head/><body><p>update the data viewed in the plot window</p><p>keyboard shortcut: V</p></body></html>"))
        self.viewButton.setText(_translate("MainW", "View"))
        self.quitButton.setToolTip(_translate("MainW", "<html><head/><body><p>exit the application</p></body></html>"))
        self.quitButton.setText(_translate("MainW", "quit"))
        self.addButton.setToolTip(_translate("MainW", "<html><head/><body><p>add a cluster from the selected working cluster with the points in the boundary.</p><p>Keyboard shortcut: A</p></body></html>"))
        self.addButton.setText(_translate("MainW", "Add"))
        self.refineButton.setToolTip(_translate("MainW", "<html><head/><body><p>refine the selected working cluster with points in the boundaries, All the points outside of the boundary is returned to the 0 (initial) cluster</p><p>keyboard shortcut: F</p></body></html>"))
        self.refineButton.setText(_translate("MainW", "reFine"))
        self.copyButton.setToolTip(_translate("MainW", "<html><head/><body><p>add a cluster from the currently selected work cluster with points in the boundary, but also keep the points in the parent cluster</p><p>keyboard shortcut: S</p></body></html>"))
        self.copyButton.setText(_translate("MainW", "copy"))
        self.deleteButton.setToolTip(_translate("MainW", "<html><head/><body><p>delete the selected working cluster, all the points will be returned to the 0 (initial) cluster.</p><p>keyboard shortcut: shift+D</p></body></html>"))
        self.deleteButton.setText(_translate("MainW", "Delete"))
        self.clearWavePlotsButton.setToolTip(_translate("MainW", "<html><head/><body><p>clear the waveform view window</p><p>Keyboard shortcut: E</p></body></html>"))
        self.clearWavePlotsButton.setText(_translate("MainW", "clEar"))
        self.reportClusterButton.setToolTip(_translate("MainW", "<html><head/><body><p>produce a report of cluster overlaps, click again to high window</p><p>Keyboard shortcut: X</p></body></html>"))
        self.reportClusterButton.setText(_translate("MainW", "report"))
        self.nextWavesButton.setToolTip(_translate("MainW", "<html><head/><body><p>View the next 100 waveforms of the working cluster</p><p>Keyboard shortcut: W</p></body></html>"))
        self.nextWavesButton.setText(_translate("MainW", "nWav"))
        self.stepBackBoundButton.setToolTip(_translate("MainW", "<html><head/><body><p>step back one point in the boundary selection</p><p>Keyboard shortcut: Z</p></body></html>"))
        self.stepBackBoundButton.setText(_translate("MainW", "back"))
        self.prevWavesButton.setToolTip(_translate("MainW", "<html><head/><body><p>View the previous 100 waveforms of the working cluster</p><p>Keyboard shortcut: Q</p></body></html>"))
        self.prevWavesButton.setText(_translate("MainW", "pwav"))
        self.resetWaveNButton.setToolTip(_translate("MainW", "<html><head/><body><p>Reset the display wave index of the working cluster back to 0 (beginning)</p><p>Keyboard shortcut: R</p></body></html>"))
        self.resetWaveNButton.setText(_translate("MainW", "Reset"))
        self.numWavesIncBox.setToolTip(_translate("MainW", "<html><head/><body><p>set the number of waves to display each time pwav and nWav buttons are clicked.</p></body></html>"))
        self.timeSelEndBox.setToolTip(_translate("MainW", "<html><head/><body><p>The end time point (as raw timestamp) for the time window selection. defaults to the last timestamp in the data, which is also the maximum that can be set.</p></body></html>"))
        self.timeSelStartBox.setToolTip(_translate("MainW", "<html><head/><body><p>set the starting time point (in raw timestamp) of the time window selection. Defaults to the first time stamp in the data, which is also the minimum that can be set.</p></body></html>"))
        self.timeSelButton.setToolTip(_translate("MainW", "<html><head/><body><p>set the time window selection. This action is final.</p></body></html>"))
        self.timeSelButton.setText(_translate("MainW", "select"))
        self.timeSelLabel.setToolTip(_translate("MainW", "<html><head/><body><p>select the time window for the samples to be worked on. Press select to set. Once set, cannot be changed.</p></body></html>"))
        self.timeSelLabel.setText(_translate("MainW", "<html><head/><body><p align=\"center\">Time selection</p></body></html>"))
        self.timeSelStartLabel.setToolTip(_translate("MainW", "<html><head/><body><p>start of the time window selection</p></body></html>"))
        self.timeSelStartLabel.setText(_translate("MainW", "<html><head/><body><p align=\"right\">start</p></body></html>"))
        self.timeSelEndLabel.setToolTip(_translate("MainW", "<html><head/><body><p>end of the time window selection</p></body></html>"))
        self.timeSelEndLabel.setText(_translate("MainW", "<html><head/><body><p align=\"right\">end</p></body></html>"))
        self.numWavesIncLabel.setToolTip(_translate("MainW", "<html><head/><body><p>number of waves to be displayed</p></body></html>"))
        self.numWavesIncLabel.setText(_translate("MainW", "<html><head/><body><p align=\"center\">num waves</p></body></html>"))
        self.exportDataButton.setToolTip(_translate("MainW", "<html><head/><body><p>export cluster parameters to hdf5 format for import into other programs. Each cut cluster is a single file, in the directory that the data file was originally loaded from. The waveforms are not exported.</p></body></html>"))
        self.exportDataButton.setText(_translate("MainW", "export data"))
        self.exportWavesButton.setToolTip(_translate("MainW", "<html><head/><body><p>export the waveforms that are drawn on the plot currently to HDF5 format for analysis and display in other programs. The exported waveforms are organized into the clusters that they came from.</p></body></html>"))
        self.exportWavesButton.setText(_translate("MainW", "export waves"))
        self.viewLargeButton.setToolTip(_translate("MainW", "<html><head/><body><p>update the data viewed in the plot window, draw in large points for visualizing stray isolated points.</p><p>Warning: this can be pretty slow, and the plot might take some time to update.</p><p>keyboard shortcut: C</p></body></html>"))
        self.viewLargeButton.setText(_translate("MainW", "viewb"))
        self.timeResetButton.setToolTip(_translate("MainW", "<html><head/><body><p>reset the time window selection to the max and minimum value.</p></body></html>"))
        self.timeResetButton.setText(_translate("MainW", "reset"))
        self.clustRatelabel.setText(_translate("MainW", "<html><head/><body><p align=\"center\">cluster<br/>rating</p></body></html>"))
        self.undoClustButton.setToolTip(_translate("MainW", "<html><head/><body><p>undo the operations on the working cluster, one step per click.</p><p>keyboard shortcut: Shift-G</p></body></html>"))
        self.undoClustButton.setText(_translate("MainW", "undo"))
        self.refWaveChsOnlyBox.setToolTip(_translate("MainW", "<html><head/><body><p>when checked, pressing pwav and nWav buttons will only display the reference waveform channels.</p></body></html>"))
        self.refWaveChsOnlyBox.setText(_translate("MainW", "RefWaves only"))
        self.toggleRefWaveChsButton.setToolTip(_translate("MainW", "<html><head/><body><p>toggle displaying only reference waveform channels, which also sets the checkbox.</p><p>Keyboard shortcut: T</p></body></html>"))
        self.toggleRefWaveChsButton.setText(_translate("MainW", "Toggle"))
        self.elimOutlierButton.setText(_translate("MainW", "elim outliers"))
        self.outlierThreshLabel.setText(_translate("MainW", "<html><head/><body><p align=\"center\">thresh</p></body></html>"))
        self.posThreshLabel.setText(_translate("MainW", "<html><head/><body><p align=\"right\">+</p></body></html>"))
        self.negThreshLabel.setText(_translate("MainW", "<html><head/><body><p align=\"right\"><span style=\" font-weight:600;\">-</span></p></body></html>"))
        self.finalizeElimOutlierBox.setText(_translate("MainW", "finalize"))

