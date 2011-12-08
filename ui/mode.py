# -*- coding: utf-8 -*-

import logging

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMenu, QActionGroup

logger = logging.getLogger(__name__)

class ModeTab(object):

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

    def enterTab(self):
        logger.debug("Entering mode tab")

    def exitTab(self):
        logger.debug("Exiting mode tab")

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
