# -*- coding: utf-8 -*-

import logging

from PyQt4.QtCore import pyqtSlot

logger = logging.getLogger(__name__)

class PWMTab(object):

    def __init__(self, mwHandle):
        self.mw = mwHandle
        
        for x in self.mw.board.pins:
            if x.PWM_CAPABLE:
                eval("self.mw.pwmBar%02d" % x.pin_number).valueChanged.connect(self.updatePwm)

    @pyqtSlot(int)
    def updatePwm(self, value):
        number = int(self.mw.sender().property("objectName").toString()[-2:])
        logger.debug("Pwm value pin "+str(number)+" set to "+str(int(value))+"%")
        self.mw.board.pins[number].write(value/100)

    def enterTab(self):
        logger.debug("Entering PWM tab")
        for x in self.mw.board.pins:
            eval("self.mw.gbPwm%02d" % x.pin_number).setEnabled(x.mode is 3)

    def exitTab(self):
        logger.debug("Exiting digital tab")
