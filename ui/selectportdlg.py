# -*- coding: utf-8 -*-

import logging
from PyQt4.QtGui import QDialog, QPushButton, QComboBox, QLabel, QStackedWidget, QHBoxLayout, QVBoxLayout, QWidget
from PyQt4.QtCore import pyqtSignature, SIGNAL, SLOT, QTimer, QReadWriteLock

from pyfirmata import util

logger = logging.getLogger(__name__)

class SelectPortDlg(QDialog):
    def __init__(self, parent=None):
        logging.debug("Port selection dialog created")
        super(SelectPortDlg, self).__init__(parent)
        self.statusLb = QLabel()
        self.updateBtn = QPushButton("Actualizar")
        self.updateBtn.setEnabled(False)
        programBtn = QPushButton("&Programar")
        self.exitBtn = QPushButton("Salir")
        multiLbl = QLabel("Selecciona la placa:")
        self.portsCmb = QComboBox()
        
        self.stackedWidget = QStackedWidget()
        mainWidget = QWidget()
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.statusLb)
        mainWidget.setLayout(mainLayout)
        self.stackedWidget.addWidget(mainWidget)
        multiWidget = QWidget()
        multiLayout = QHBoxLayout()
        multiLayout.addWidget(multiLbl)
        multiLayout.addWidget(self.portsCmb)
        multiWidget.setLayout(multiLayout)
        self.stackedWidget.addWidget(multiWidget)
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.updateBtn)
        buttonLayout.addWidget(programBtn)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.exitBtn)
        self.exitBtn.setFocus()
        
        layout = QVBoxLayout()
        layout.addWidget(self.stackedWidget)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)
        
        self.lock = QReadWriteLock()
        self.boards = list()
        self.searcher = util.SearchBoard(self.lock, self)
        self.connect(self.searcher, SIGNAL("finished(bool)"), self.finishedSearching)
        #self.connect(self.programBtn, SIGNAL("clicked()"), self.setPath)
        self.connect(self.updateBtn, SIGNAL("clicked()"), self.startSearch)
        self.connect(self.exitBtn, SIGNAL("clicked()"), self, SLOT("reject()"))
        self.setWindowTitle(u"Iniciando comunicación")
        self.startSearch()

    def startSearch(self):
        self.stackedWidget.setCurrentIndex(0)
        self.portsCmb.clear()
        self.statusLb.setText("Buscando placa Arduino...")
        # Close all serial ports and delete all objects from past executions
        while self.boards:
            board = self.boards.pop()
            board.exit()
            del board
        self.updateBtn.setEnabled(False)
        self.searcher.initialize(self.boards)
        self.searcher.start()

    def finishedSearching(self):
        self.searcher.wait()
        self.updateBtn.setEnabled(True)
        if not self.boards:
            self.statusLb.setText(u"No se ha detectado ningún Arduino")
        else:
            self.statusLb.setText(u"Se ha detectado %d Arduino")
            if len(self.boards) == 1:
                self.board = self.boards[0]
                QDialog.accept(self)
            else:
                self.stackedWidget.setCurrentIndex(1)
                self.portsCmb.addItems([x.sp.port for x in self.boards])
                #Connect combobox selection to 

    def reject(self):
        logging.debug("Called reject")
        if self.searcher.isRunning():
            self.searcher.stop()
            self.finishedSearching()
        else:
            self.accept()

    def closeEvent(self, event=None):
        logging.debug("Close event")
        self.searcher.stop()
        self.searcher.wait()

    def getBoard(self):
        return self.board
