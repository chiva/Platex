# -*- coding: utf-8 -*-

import logging, serial
from PyQt4.QtGui import QDialog, QPushButton, QComboBox, QLabel, QStackedWidget, QHBoxLayout, QVBoxLayout, QWidget
from PyQt4.QtCore import SIGNAL, SLOT, QTimer, QString, pyqtSlot

from pyfirmata import Board
from pyfirmata.boards import BOARDS

logger = logging.getLogger(__name__)

class SelectPortDlg(QDialog):
    def __init__(self, parent=None):
        logging.debug("Port selection dialog created")
        super(SelectPortDlg, self).__init__(parent)
        self.statusLb = QLabel()
        self.connectBtn = QPushButton("&Conectar")
        self.connectBtn.setEnabled(False)
        self.programBtn = QPushButton("&Programar")
        self.programBtn.setEnabled(False)
        exitBtn = QPushButton("Salir")
        multiLbl = QLabel("Selecciona la placa:")
        self.portsCmb = QComboBox()
        self.portsCmb.addItem("Actualizar")
        
        self.stackedWidget = QStackedWidget()
        mainWidget = QWidget()
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(multiLbl)
        mainLayout.addWidget(self.portsCmb)
        mainWidget.setLayout(mainLayout)
        self.stackedWidget.addWidget(mainWidget)
        progWidget = QWidget()
        progLayout = QHBoxLayout()
        progLayout.addWidget(self.statusLb)
        progLayout.addStretch()
        progWidget.setLayout(progLayout)
        self.stackedWidget.addWidget(progWidget)
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.connectBtn)
        buttonLayout.addWidget(self.programBtn)
        buttonLayout.addStretch()
        buttonLayout.addWidget(exitBtn)
        exitBtn.setFocus()
        
        layout = QVBoxLayout()
        layout.addWidget(self.stackedWidget)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)
        
        self.boards = list()
        self.board = None
        #self.connect(self.programBtn, SIGNAL("clicked()"), self.setPath)
        self.portsCmb.currentIndexChanged[int].connect(self.updatePorts)
        self.connectBtn.clicked[bool].connect(self.connectBoard)
        exitBtn.clicked.connect(self.reject)
        self.setWindowTitle(u"Iniciando comunicación")
        self.updatePorts()
    
    @pyqtSlot()
    def updatePorts(self):
        if self.portsCmb.currentText() != QString("Actualizar"):
            return
        logger.debug("Searching existing serial ports")
        self.connectBtn.setEnabled(False)
        self.programBtn.setEnabled(False)
        ports = []
        for i in xrange(256):
            try:
                s = serial.Serial(i)
                ports.append(s.portstr)
                s.close()
            except serial.SerialException:
                pass
        logger.debug("Found %d serial port(s): %s", len(ports), ports)
        if not len(ports): ports = [""]
        self.portsCmb.clear()
        self.portsCmb.addItems(ports)
        self.portsCmb.addItem("Actualizar")
        if self.portsCmb.currentText() != QString(""):
            self.connectBtn.setEnabled(True)
            self.programBtn.setEnabled(True)
    
    @pyqtSlot()
    def connectBoard(self):
        try:
            board = Board(unicode(self.portsCmb.currentText()), BOARDS['arduino'])
        except ValueError, e:
            logger.warning(str(e))
        except TypeError, e:
            logger.debug(str(e))
        else:
            self.board = board
            self.accept()

    def getBoard(self):
        return self.board
