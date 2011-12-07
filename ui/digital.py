# -*- coding: utf-8 -*-

import logging

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMenu, QActionGroup

logger = logging.getLogger(__name__)

class DigitalTab(object):

    def __init__(self, mwHandle):
        self.mw = mwHandle
        
        for x in xrange(2, 20):
            pin = eval("self.mw.pin%02d" % (x))
            menu = QMenu(pin)
            modeGroup = QActionGroup(self.mw)
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
            if self.mw.board.pins[x].PWM_CAPABLE:
                pwm = menu.addAction("&PWM")
                modeGroup.addAction(pwm)
                pwm.triggered.connect(self.clickPWM)
                pwm.setCheckable(True)
            if self.mw.board.pins[x].type == 2:
                analogic = menu.addAction(u"&Analógico")
                modeGroup.addAction(analogic)
                analogic.triggered.connect(self.clickAnalog)
                analogic.setCheckable(True)
            pin.setMenu(menu)
            pin.setStyleSheet("/* */") # force stylesheet update
        
        for x in self.mw.board.ports:
            x.pinChanged.connect(self.updatePin)

    @pyqtSlot(int, bool)
    def updatePin(self, number, state):
        logger.debug("Input pin "+str(number)+" changed its state to "+str(state))
        eval("self.mw.di%02d" % (number)).setChecked(state)

    def enterTab(self):
        logger.debug("Entering digital tab")
        for x in xrange(2, 20):
            digPin = eval("self.mw.d%02d" % (x))
            digInPin = eval("self.mw.di%02d" % (x))
            digPin.setVisible(False)
            digInPin.setVisible(False)
            mode = self.mw.board.pins[x].mode
            if mode == 1:
                digPin.clicked.connect(self.digPinClicked)
                digPin.setVisible(True)
                digPin.setChecked(self.mw.board.pins[x].read())
            elif mode == 0:
                digInPin.setVisible(True)
                digInPin.setChecked(self.mw.board.pins[x].read())
                self.mw.board.pins[x].enable_reporting()

    def exitTab(self):
        logger.debug("Exiting digital tab")
        for x in xrange(2, 20):
            self.mw.board.pins[x].disable_reporting()

    @pyqtSlot()
    def clickNone(self):
        self._changeMode(self.mw.sender(), 7)

    @pyqtSlot()
    def clickInput(self):
        self._changeMode(self.mw.sender(), 0)

    @pyqtSlot()
    def clickOutput(self):
        self._changeMode(self.mw.sender(), 1)

    @pyqtSlot()
    def clickPWM(self):
        self._changeMode(self.mw.sender(), 3)

    @pyqtSlot()
    def clickAnalog(self):
        self._changeMode(self.mw.sender(), 2)

    def _changeMode(self, action, mode):
        pin = action.parentWidget().parentWidget()
        text = ['I', 'O', 'A', 'P', '', '', '', 'N']
        pin.setText(text[mode])
        pin.setStyleSheet("/* */") # force stylesheet update
        number = int(pin.property("objectName").toString()[-2:])
        self.mw.board.pins[number].mode = mode
        if mode == 2:
            self.mw.board.pins[number].disable_reporting()
        logger.debug("Changed pin %d mode to '%s'", number, pin.text())

    @pyqtSlot()
    def digPinClicked(self):
        pin = self.mw.sender()
        number = int(pin.property("objectName").toString()[-2:])
        if pin.isChecked():
            self.mw.board.pins[number].write(1)
            logger.debug("Changed output pin "+str(number)+" state to True")
        else:
            self.mw.board.pins[number].write(0)
            logger.debug("Changed output pin "+str(number)+" state to False")
