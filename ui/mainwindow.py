# -*- coding: utf-8 -*-

"""
This module contains the class MainWindow.
"""

import logging, inspect, time
from PyQt4.QtGui import QMainWindow, QPushButton
from PyQt4.QtCore import QTimer, pyqtSlot
from pyfirmata import Arduino, util

from Ui_mainwindow import Ui_mainWindow
from selectportdlg import SelectPortDlg

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow, Ui_mainWindow):
    """
    MainWindow: this is the class that manages all the funcionality of receiving input from the user.
    """

    def __init__(self, parent=None):
        """
        Default Constructor. It can receive a top window as parent. 
        """
        logging.debug("Creating MainWindow")
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # Build object name, evaluate the string to obtain it and bind the clicked() signal
        for x in xrange(2, 20):
            eval("self.pin%02d" % (x)).clicked.connect(self.pinClicked)
        QTimer.singleShot(0, self.selectPort)
        
        self.board = None
        self.lastIndex = 0

    def selectPort(self):
        dialog = SelectPortDlg(self)
        dialog.exec_()
        # If empty object is returned, we exit
        self.board = dialog.getBoard()
        if not self.board:
            self.close()
        else:
            self.it = util.Iterator(self.board)
            self.it.start()

    @pyqtSlot()
    def pinClicked(self):
        pin = self.sender()
        if not isinstance(pin, QPushButton):
            logger.warning(inspect.stack()[0][3] + "(): Not a QPushButton")
            return
        if not pin.property("analog").isValid():
            logger.warning("%s(): '%s' shouldn't be connected to this method. Missing 'analog' property", inspect.stack()[0][3], pin.property("objectName").toString())
            return
        current = pin.text()
        if current == 'N':
            pin.setText('I')
            mode = 0
        elif current == 'I':
            pin.setText('O')
            mode = 1
        elif current == 'O' and pin.property("analog").toBool():
            pin.setText('A')
            mode = 2
        else:
            pin.setText('N')
            mode = 0
        number = int(pin.property("objectName").toString()[-2:])
        if number <= 13:
            self.board.digital[number].mode = mode
        else:
            self.board.analog[number-14].mode = mode
        pin.setStyleSheet("/* */") #Empty stylesheet to force redraw with the stylesheet set in Qt-Designer
        logger.debug("Changed pin %d mode to '%s'", number, pin.text())

    @pyqtSlot()
    def digPinClicked(self):
        pin = self.sender()
        number = int(pin.property("objectName").toString()[-2:])
        if pin.isChecked():
            self.board.digital[number].write(1)
            logger.debug("Changed output pin "+str(number)+" state to True")
        else:
            self.board.digital[number].write(0)
            logger.debug("Changed output pin "+str(number)+" state to False")

    @pyqtSlot(int, bool)
    def updatePin(self, number, state):
        logger.debug("Input pin "+str(number)+" changed its state to "+str(state))
        eval("self.di%02d" % (number)).setChecked(state)
    
    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, index):
        """
        Slot documentation goes here.
        """
        self.lastIndex = index
        if index == 1:
            for x in self.board.digital_ports:
                x.pinChanged.connect(self.updatePin)
            for x in xrange(2, 20):
                digPin = eval("self.d%02d" % (x))
                digInPin = eval("self.di%02d" % (x))
                pin = eval("self.pin%02d" % (x))
                digPin.setVisible(False)
                digInPin.setVisible(False)
                if x <= 13:
                    mode = self.board.digital[x].mode
                else:
                    mode = self.board.analog[x-14].mode
                if mode == 1:
                    digPin.clicked.connect(self.digPinClicked)
                    digPin.setVisible(True)
                elif mode == 0 and pin.text() == 'I':
                    digInPin.setVisible(True)
