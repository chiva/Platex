# -*- coding: utf-8 -*-

import logging

from PyQt4.QtCore import pyqtSlot

logger = logging.getLogger(__name__)

class DigitalTab(object):
    def __init__(self, mwHandle):
        self.mw = mwHandle
        
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
    def digPinClicked(self):
        pin = self.mw.sender()
        number = int(pin.property("objectName").toString()[-2:])
        if pin.isChecked():
            self.mw.board.pins[number].write(1)
            logger.debug("Changed output pin "+str(number)+" state to True")
        else:
            self.mw.board.pins[number].write(0)
            logger.debug("Changed output pin "+str(number)+" state to False")
