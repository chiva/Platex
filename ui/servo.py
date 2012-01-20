# -*- coding: utf-8 -*-

import logging

from PyQt4.QtCore import pyqtSlot
from functools import partial

logger = logging.getLogger(__name__)

class ServoTab(object):

    def __init__(self, mwHandle):
        self.mw = mwHandle
        self.sliders = list()
        self.selected = [0 for x in range(0, 6)]
        
        for x in xrange(1, 7):
            slider = eval("self.mw.servoBar%d" % x)
            spinBox = eval("self.mw.servoBox%d" % x)
            slider.setRange(0, 180, 1)
            self.sliders.append(slider)
            self._groupEnabled(x, False)
            self._disableCheckBox(x)
            
            slider.valueChanged.connect(spinBox.setValue)
            spinBox.valueChanged[int].connect(slider.setValue)
            spinBox.valueChanged[int].connect(partial(self._updateServo, x))
            eval("self.mw.servoCmb%d" % x).currentIndexChanged[str].connect(partial(self._pinSelected, x))
            eval("self.mw.servoCb%d" % x).stateChanged[int].connect(partial(self._activated, x))
            eval("self.mw.servoBut%d" % x).clicked.connect(partial(self._zero, x-1))
        self.mw.servoBut0.clicked.connect(self._allZero)

    def enterTab(self):
        logger.debug("Entering servo tab")
        self._updateAvailable()

    def exitTab(self):
        logger.debug("Exiting servo tab")

    @pyqtSlot(int)
    def _zero(self, slider):
        if self.sliders[slider].isValid():
            self.sliders[slider].setValue(0)

    @pyqtSlot()
    def _allZero(self):
        for x in xrange(0, len(self.sliders)):
            self._zero(x)

    @pyqtSlot(int, int)
    def _activated(self, group, status):
        if status:
            self._groupEnabled(group, True)
            pin = int(eval("self.mw.servoCmb%d" % group).currentText())
            logger.debug("Pin "+str(pin)+" set to Servo mode")
            self.selected[group-1] = pin
            self.mw.board.pins[pin].mode = 4
        else:
            self._groupEnabled(group, False)
            pin = self.selected[group-1]
            logger.debug("Pin "+str(pin)+" restored to Output mode")
            self.selected[group-1] = 0
            self.mw.board.pins[pin].mode = 1
            self.mw.board.pins[pin].write(0)

    def _groupEnabled(self, group, state):
        eval("self.mw.servoBar%d" % group).setEnabled(state)
        eval("self.mw.servoBar%d" % group).setValid(state)
        eval("self.mw.servoBox%d" % group).setEnabled(state)
        eval("self.mw.servoBut%d" % group).setEnabled(state)

    def _disableCheckBox(self, group):
        eval("self.mw.servoCb%d" % group).setChecked(False)
        eval("self.mw.servoCb%d" % group).setEnabled(False)

    @pyqtSlot(str)
    def _pinSelected(self, group, pin):
        if pin:
            try:
                self.suitables.remove(int(pin))
                eval("self.mw.servoCb%d" % group).setEnabled(True)
            except ValueError:
                pass
        else:
            eval("self.mw.servoBox%d" % group).blockSignals(True)
            eval("self.mw.servoBar%d" % group).setValue(0)
            eval("self.mw.servoBox%d" % group).blockSignals(False)
            self._groupEnabled(group, False)
            self._disableCheckBox(group)
        self._updateAvailable()

    def _updateAvailable(self):
        self.suitables = list()
        
        # Search for pins set as output or servo modes
        for x in self.mw.board.pins:
            if x.mode in (1, 4):
                self.suitables.append(x.pin_number)
        
        # Search for non used pins
        for x in xrange(1, 7):
            combo = eval("self.mw.servoCmb%d" % x)
            try:
                number = int(combo.currentText())
                if number in self.suitables:
                    # If pin is on available list, remove it, we are already using it
                    self.suitables.remove(number)
                    continue
            except ValueError:
                # If combobox content is not a number, is empty, ignore
                pass
        
        # Create custom list for each combobox
        # Made from available pin list plus the selected pin in the combobox
        for x in xrange(1, 7):
            combo = eval("self.mw.servoCmb%d" % x)
            items = self.suitables[:]               # copy list
            number = 0                              # no pin selected
            try:
                number = int(combo.currentText())
                items.append(number)                # add pin selected in combobox
                items.sort()
            except ValueError:
                pass
            combo.blockSignals(True)
            combo.clear()
            combo.addItem("")
            if len(items):
                for pin in items:
                    combo.addItem(str(pin))
            if number:
                combo.setCurrentIndex(items.index(number)+1)
                #eval("self.mw.servoCb%d" % x).setChecked(True)
            combo.blockSignals(False)

    @pyqtSlot(int, int)
    def _updateServo(self, group, angle):
        pin = int(eval("self.mw.servoCmb%d" % group).currentText())
        logger.debug("Moved servo on pin "+str(pin)+" to "+str(angle)+"º")
        self.mw.board.pins[pin].write(angle)
