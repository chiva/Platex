# -*- coding: utf-8 -*-

"""
This module contains the class MainWindow.
"""

import logging, inspect, time
from PyQt4.QtGui import QMainWindow, QPushButton, QMenu, QActionGroup
from PyQt4.QtCore import QTimer, pyqtSlot
from pyfirmata import Arduino, util

from Ui_mainwindow import Ui_mainWindow
from selectportdlg import SelectPortDlg
from analog import AnalogTab

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
        
        for x in xrange(2, 20):
                eval("self.pin%02d" % (x)).setStyleSheet("* {padding:0px}")
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
            self.analog = AnalogTab(self, self.analogPlot)
            self.board.updateAnalog.connect(self.analog.update)
            self.cbUnit.currentIndexChanged.connect(self.analog.changedUnits)
            for x in xrange(2, 20):
                pin = eval("self.pin%02d" % (x))
                menu = QMenu(pin)
                modeGroup = QActionGroup(self)
                modeGroup.setExclusive(True)
                none = menu.addAction("&None")
                modeGroup.addAction(none)
                none.triggered.connect(self.clickNone)
                none.setCheckable(True)
                none.setChecked(True)
                input = menu.addAction("&Input")
                modeGroup.addAction(input)
                input.triggered.connect(self.clickInput)
                input.setCheckable(True)
                output = menu.addAction("&Output")
                modeGroup.addAction(output)
                output.triggered.connect(self.clickOutput)
                output.setCheckable(True)
                if self.board.pins[x].PWM_CAPABLE:
                    pwm = menu.addAction("&PWM")
                    modeGroup.addAction(pwm)
                    pwm.triggered.connect(self.clickPWM)
                    pwm.setCheckable(True)
                if self.board.pins[x].type == 2:
                    analogic = menu.addAction(u"&Analógico")
                    modeGroup.addAction(analogic)
                    analogic.triggered.connect(self.clickAnalog)
                    analogic.setCheckable(True)
                pin.setMenu(menu)
                pin.setStyleSheet("/* */") # force stylesheet update
            
            self.it = util.Iterator(self.board)
            self.it.start()

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
        if self.lastIndex == 1:
            for x in self.board.ports:
                x.pinChanged.disconnect()
            for x in xrange(2, 20):
                try:
                    # TODO: disable reporting instead of disconnecting signals
                    eval("self.d%02d" % (x)).clicked.disconnect()
                except TypeError:
                    pass
        if self.lastIndex == 2:
            self.analog.exitTab()
        
        self.lastIndex = index
        
        if index == 1:
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
        elif index == 2:
            self.analog.enterTab()

    @pyqtSlot()
    def clickNone(self):
        self._changeMode(self.sender(), 7)

    @pyqtSlot()
    def clickInput(self):
        self._changeMode(self.sender(), 0)

    @pyqtSlot()
    def clickOutput(self):
        self._changeMode(self.sender(), 1)

    @pyqtSlot()
    def clickPWM(self):
        self._changeMode(self.sender(), 3)

    @pyqtSlot()
    def clickAnalog(self):
        self._changeMode(self.sender(), 2)

    def _changeMode(self, action, mode):
        pin = action.parentWidget().parentWidget()
        text = ['I', 'O', 'A', 'P', '', '', '', 'N']
        if not isinstance(pin, QPushButton):
            logger.warning(inspect.stack()[0][3] + "(): Not a QPushButton")
            return
        pin.setText(text[mode])
        pin.setStyleSheet("/* */") # force stylesheet update
        number = int(pin.property("objectName").toString()[-2:])
        self.board.pins[number].mode = mode
        if mode == 2:
            self.board.pins[number].disable_reporting()
        logger.debug("Changed pin %d mode to '%s'", number, pin.text())
