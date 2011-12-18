# -*- coding: utf-8 -*-

import logging

from PyQt4.QtCore import pyqtSlot
from functools import partial

logger = logging.getLogger(__name__)

class MotorTab(object):

    def __init__(self, mwHandle):
        self.mw = mwHandle
        
        for page in xrange(0, 3):
            eval("self.mw.motorBut%d" % page).clicked.connect(partial(self.mw.motorSw.setCurrentIndex, page))
            eval("self.mw.motorSAll%d" % page).clicked.connect(partial(self._allZero, page))
            eval("self.mw.motorBut%d" % page).clicked.connect(partial(self._changedPage, page))
            for section in ("A", "B"):
                eval("self.mw.motorStop%s%d" % (section, page)).clicked.connect(partial(self._zero, section, page))
                eval("self.mw.motorPer%s%d" % (section, page)).valueChanged[int].connect(partial(self._updateMotor, section, page))
                eval("self.mw.motorAct%s%d" % (section, page)).clicked.connect(partial(self._activated, section, page))
                self._groupEnabled(section, page, False)
                if page is 3:
                    eval("self.mw.motorPwm%s%d" % (section, page)).currentIndexChanged[str].connect(partial(self._pinSelected, section))
                    eval("self.mw.motorDir%s%d" % (section, page))

    def enterTab(self):
        logger.debug("Entering motor tab")
        self._updateAvailable()
        for page in xrange(0, 3):
            for section in ("A", "B"):
                try:
                    pin1 = int(eval("self.mw.motorPwm%s%d" % (section, page)).currentText())
                    pin2 = int(eval("self.mw.motorDir%s%d" % (section, page)).currentText())
                    state = self.mw.board.pins[pin1].mode is 3 and self.mw.board.pins[pin2].mode is 1
                except ValueError:
                    state = False
                eval("self.mw.motorAct%s%d" % (section, page)).setEnabled(state)

    def exitTab(self):
        logger.debug("Exiting motor tab")

    @pyqtSlot(int)
    def _zero(self, section, page):
        if eval("self.mw.motorAct"+section+str(page)).isChecked():
            eval("self.mw.motorPer"+section+str(page)).setValue(0)

    @pyqtSlot()
    def _allZero(self, page):
        for section in ("A", "B"):
            self._zero(section, page)

    @pyqtSlot(str, int, bool)
    def _activated(self, section, page, status):
        pin = int(eval("self.mw.motorPwm%s%d" % (section, page)).currentText())
        self._groupEnabled(section, page, status)
        if status:
            logger.debug("Activating motor "+section+" in pin "+str(pin))
        else:
            logger.debug("Deactivating motor "+section+" in pin "+str(pin))
        eval("self.mw.motorPer%s%d" % (section, page)).setValue(0)
        self._updateAvailable()

    def _groupEnabled(self, section, page, state):
        eval("self.mw.motorSli%s%d" % (section, page)).setEnabled(state)
        eval("self.mw.motorPer%s%d" % (section, page)).setEnabled(state)
        eval("self.mw.motorStop%s%d" % (section, page)).setEnabled(state)

    @pyqtSlot(str, str)
    def _pinSelected(self, section, pin):
        try:
            pwm = eval("self.mw.motorPwm%s2" % section).currentText()
            dir = eval("self.mw.motorDir%s2" % section).currentText()
            eval("self.mw.servoCb%d" % group).setEnabled(True)
        except ValueError:
            pass
        self._updateAvailable()

    def _updateAvailable(self):
        self.suitableDir = list()
        self.suitablePwm = list()
        
        # Search for pins set as output or servo modes
        for x in self.mw.board.pins:
            if x.mode is 1:
                self.suitableDir.append(x.pin_number)
            elif x.mode is 3:
                self.suitablePwm.append(x.pin_number)
        
        # Remove used pins in active configurations of page 2
        for section in ("A", "B"):
            try:
                pwm = int(eval("self.mw.motorPwm%s2" % section).currentText())
                dir = int(eval("self.mw.motorDir%s2" % section).currentText())
                if eval("self.mw.motorAct%s2" % section).isChecked():
                    if pwm in self.suitablePwm:
                        self.suitablePwm.remove(pwm)
                    if dir in self.suitableDir:
                        self.suitableDir.remove(dir)
            except ValueError:
                pass
        
        # Create custom list for each combobox
        for section in ("A", "B"):
            for type in ("Pwm", "Dir"):
                combo = eval("self.mw.motor%s%s2" % (type, section))
                if not eval("self.mw.motorAct%s2" % section).isChecked():
                    items = eval("self.suitable%s" % type)[:]
                else:
                    items = [int(eval("self.mw.motor%s%s2" % (type, section)).currentText())]
                combo.blockSignals(True)
                combo.clear()
                if len(items):
                    for pin in items:
                        combo.addItem(str(pin))
                combo.blockSignals(False)

    @pyqtSlot(str, int, int)
    def _updateMotor(self, section, page, speed):
        pin = int(eval("self.mw.motorDir%s%d" % (section, page)).currentText())
        pwm = int(eval("self.mw.motorPwm%s%d" % (section, page)).currentText())
        logger.debug("Changed motor "+section+" speed to "+str(speed)+"%")
        self.mw.board.pins[pin].write(1 if speed > 0 else 0)
        self.mw.board.pins[pwm].write(abs(speed)/100.0)

    @pyqtSlot(int)
    def _changedPage(self, page):
        eval("self.mw.motorBut%d" % page).setChecked(True)
        for x in [y for y in range(0,3) if y is not page]:
            eval("self.mw.motorBut%d" % x).setChecked(False)
            for section in ("A", "B"):
                if eval("self.mw.motorAct%s%d" % (section, x)).isChecked():
                    eval("self.mw.motorAct%s%d" % (section, x)).setChecked(False)
                    self._activated(section, page, False)
        self._updateAvailable()
