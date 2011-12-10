# -*- coding: utf-8 -*-

import logging

from PyQt4.QtCore import pyqtSlot

logger = logging.getLogger(__name__)

class PWMTab(object):

    def __init__(self, mwHandle):
        self.mw = mwHandle
        self.sliders = list()
        
        for x in self.mw.board.pins:
            if x.PWM_CAPABLE:
                slider = eval("self.mw.pwmBar%02d" % x.pin_number)
                slider.valueChanged.connect(self.updatePwm)
                self.sliders.append(slider)
                
        self.mw.cbPwmUnit.insertItems(0, ("Porcentaje", "Cuentas"))
        self.mw.cbPwmUnit.currentIndexChanged.connect(self.changedUnits)

    @pyqtSlot(int)
    def updatePwm(self, value):
        if self.mw.cbPwmUnit.currentIndex() is 0:
            number = int(self.mw.sender().property("objectName").toString()[-2:])
            logger.debug("PWM value pin "+str(number)+" set to "+str(int(value))+"%")
            self.mw.board.pins[number].write(value/100)
        else:
            number = int(self.mw.sender().property("objectName").toString()[-2:])
            logger.debug("PWM value pin "+str(number)+" set to "+str(int(value)))
            self.mw.board.pins[number].write(round(value/1023, 2))

    def enterTab(self):
        logger.debug("Entering PWM tab")
        for x in self.mw.board.pins:
            if x.PWM_CAPABLE:
                eval("self.mw.gbPwm%02d" % x.pin_number).setEnabled(x.mode is 3)
                eval("self.mw.pwmBar%02d" % x.pin_number).setValid(x.mode is 3)

    def exitTab(self):
        logger.debug("Exiting PWM tab")

    @pyqtSlot(int)
    def changedUnits(self, index):
        if index is 0:
            logger.debug("Changed PWM units to percentage")
            for slider in self.sliders:
                value = slider.value()
                slider.blockSignals(True)
                slider.setRange(0, 100, 1)
                slider.blockSignals(False)
                slider.setValue(round(value*100/1023))
        else:
            logger.debug("Changed PWM units to counts")
            for slider in self.sliders:
                value = slider.value()
                slider.blockSignals(True)
                slider.setRange(0, 1023, 1)
                slider.blockSignals(False)
                slider.setValue(round(value*1023/100))
