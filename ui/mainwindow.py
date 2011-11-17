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
        QMainWindow.__init__(self, parent)
        logging.debug("Created MainWindow")
        self.setupUi(self)

        # Build object name, evaluate the string to obtain it and bind the clicked() signal
        for x in xrange(2, 20):
            eval("self.pin%02d" % (x)).clicked.connect(self.pinClicked)
        
        self.board = None
        self.lastIndex = 0
        QTimer.singleShot(0, self.selectPort)

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
            mode = 7
        number = int(pin.property("objectName").toString()[-2:])
        self.board.pins[number].mode = mode
        pin.setStyleSheet("/* */") #Empty stylesheet to force redraw with the stylesheet set in Qt-Designer
        logger.debug("Changed pin %d mode to '%s'", number, pin.text())

    @pyqtSlot()
    def digPinClicked(self):
        pin = self.sender()
        number = int(pin.property("objectName").toString()[-2:])
        if pin.isChecked():
            self.board.pins[number].write(1)
            logger.debug("Changed output pin "+str(number)+" state to True")
        else:
            self.board.pins[number].write(0)
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
        if self.lastIndex == 0:
            for x in xrange(2, 20):
                eval("self.pin%02d" % (x)).clicked.disconnect()
        elif self.lastIndex == 1:
            for x in self.board.ports:
                x.pinChanged.disconnect()
            for x in xrange(2, 20):
                try:
                    eval("self.d%02d" % (x)).clicked.disconnect()
                except TypeError:
                    pass
        
        self.lastIndex = index
        
        if index == 0:
            for x in xrange(2, 20):
                eval("self.pin%02d" % (x)).clicked.connect(self.pinClicked)
        elif index == 1:
            for x in self.board.ports:
                x.pinChanged.connect(self.updatePin)
            for x in xrange(2, 20):
                digPin = eval("self.d%02d" % (x))
                digInPin = eval("self.di%02d" % (x))
                digPin.setVisible(False)
                digInPin.setVisible(False)
                mode = self.board.pins[x].mode
                if mode == 1:
                    digPin.clicked.connect(self.digPinClicked)
                    digPin.setVisible(True)
                    digPin.setChecked(self.board.pins[x].read())
                elif mode == 0:
                    digInPin.setVisible(True)
                    digInPin.setChecked(self.board.pins[x].read())
