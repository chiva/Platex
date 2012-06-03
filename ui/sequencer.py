# -*- coding: utf-8 -*-

import logging

from PyQt4.QtCore import pyqtSlot, QCoreApplication
from functools import partial
from time import sleep

logger = logging.getLogger(__name__)

class Step(object):
    
    def __init__(self):
        self.digital = [False for x in range(0, 6)]
        self.servo = [0 for x in range(0, 3)]
        self.pwm = [0 for x in range(0, 3)]
        self.time = 1000

class SequencerTab(object):

    def __init__(self, mwHandle):
        self.mw = mwHandle
        self.sliders = list()
        self.digital = dict()
        self.servo = list()
        self.pwm = list()
        self.steps = [Step()]
        self.index = eval("self.mw.seqStep")
        
        for x in xrange(1, 4):
            # Servos
            slider = eval("self.mw.seqBar%d" % x)
            spinBox = eval("self.mw.seqBox%d" % x)
            slider.setRange(0, 180, 1)
            self.sliders.append(slider)
            self._groupEnabled(x, False)
            
            slider.valueChanged.connect(spinBox.setValue)
            spinBox.valueChanged[int].connect(slider.setValue)
            spinBox.valueChanged[int].connect(partial(self._updateServo, x))
            eval("self.mw.seqZero%d" % x).clicked.connect(partial(self._zero, x-1))
            self.servo.append(int(eval("self.mw.seqGb%d" % x).property("title").toString().split()[1]))

        for x in xrange(1, 4):
            #PWM
            eval("self.mw.seqBarP%d" % x).valueChanged.connect(partial(self._updatePWM, x))
            self.pwm.append(int(eval("self.mw.seqGbP%d" % x).property("title").toString().split()[1]))
        
        for x in xrange(1, 7):
            #Digitales
            button = eval("self.mw.seqDig%d" % x)
            button.toggled.connect(partial(self._clickDigital, x))
            button.setEnabled(False)
            self.digital[int(eval("self.mw.seqDigL%d" % x).property("text").toString())] = button
        
        self.mw.servoBut0.clicked.connect(self._allZero)
        eval("self.mw.seqAddStep").clicked.connect(self._addStep)
        eval("self.mw.seqDelStep").clicked.connect(self._delStep)
        eval("self.mw.seqTime").valueChanged[int].connect(self._changedTime)
        self.index.valueChanged[int].connect(self._loadStep)
        eval("self.mw.seqControl").clicked.connect(self._sequencerControl)

    def enterTab(self):
        logger.debug("Entering sequencer tab")
        self._updateAvailable()
        self._loadStep(self.index.value())

    def exitTab(self):
        logger.debug("Exiting sequencer tab")
        for x in self.mw.board.pins:
            if x.mode is 4:
                self._groupEnabled(self.servo.index(pin)+1, False)

    @pyqtSlot()
    def _sequencerControl(self):
        button = eval("self.mw.seqControl")
        button.setEnabled(False)
        QCoreApplication.processEvents()
        for x in xrange(1, len(self.steps)+1):
            self._loadStep(x)
            sleep(float(self.steps[x-1].time)/1000)
        button.setEnabled(True)

    @pyqtSlot(int)
    def _changedTime(self, time):
        curStep = self.steps[self.index.value()-1]
        curStep.time = time

    def _addStep(self):
        curStep = self.steps[self.index.value()-1]
        newStep = Step()
        newStep.digital = curStep.digital[:]
        newStep.servo = curStep.servo[:]
        newStep.pwm = curStep.pwm[:]
        newStep.time = curStep.time
        self.steps.append(newStep)
        logger.debug("Created step "+str(len(self.steps)))
        self.index.setMaximum(len(self.steps))
        self._loadStep(len(self.steps))

    def _delStep(self):
        index = self.index.value()
        if index is not 1:
            logger.debug("Deleted step "+str(index))
            self.steps.pop(index-1)
            self._loadStep(index-1)
            self.index.setMaximum(len(self.steps))

    @pyqtSlot(int)
    def _loadStep(self, index):
        step = self.steps[index-1]
        logger.debug("Loaded step "+str(index))
        self.index.blockSignals(True)
        self.index.setValue(index)
        self.index.blockSignals(False)
        for x in xrange(1, len(step.digital)+1):
            eval("self.mw.seqDig%d" % x).setChecked(step.digital[x-1])
        for x in xrange(1, len(step.servo)+1):
            eval("self.mw.seqBox%d" % x).setValue(step.servo[x-1])
        for x in xrange(1, len(step.pwm)+1):
            eval("self.mw.seqBarP%d" % x).setValue(step.pwm[x-1])
        eval("self.mw.seqTime").setValue(step.time)

    @pyqtSlot(int)
    def _clickDigital(self, group):
        pin = self.mw.sender()
        number = int(eval("self.mw.seqDigL%d" % group).property("text").toString())
        if not pin.isEnabled():
            return
        if pin.isChecked():
            self.mw.board.pins[number].write(1)
            logger.debug("Changed output pin "+str(number)+" state to True")
        else:
            self.mw.board.pins[number].write(0)
            logger.debug("Changed output pin "+str(number)+" state to False")
        curStep = self.steps[self.index.value()-1]
        curStep.digital[group-1] = pin.isChecked()

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
        pin = int(eval("self.mw.seqGb%d" % group).property("title").toString().split()[1])
        if self.mw.board.pins[pin].mode in (1, 4):
            if status:
                logger.debug("Pin "+str(pin)+" set to Servo mode")
                self.mw.board.pins[pin].mode = 4
            else:
                logger.debug("Pin "+str(pin)+" restored to Output mode")
                self.mw.board.pins[pin].mode = 1
                self.mw.board.pins[pin].write(0)

    def _groupEnabled(self, group, state):
        eval("self.mw.seqBar%d" % group).setEnabled(state)
        eval("self.mw.seqBar%d" % group).setValid(state)
        eval("self.mw.seqZero%d" % group).setEnabled(state)
        eval("self.mw.seqBox%d" % group).setEnabled(state)
        self._activated(group, state)
    
    def _groupEnabledP(self, group, state):
        eval("self.mw.seqBarP%d" % group).setEnabled(state)
        eval("self.mw.seqBarP%d" % group).setValid(state)
        eval("self.mw.seqLblP%d" % group).setEnabled(state)

    def _updateAvailable(self):
        self.suitableDig = list()
        self.suitableServo = list()
        self.suitablePWM = list()
        
        # Search for pins set as output or servo modes
        for x in self.mw.board.pins:
            if x.mode is 1:
                self.suitableDig.append(x.pin_number)
                self.suitableServo.append(x.pin_number)
            if x.mode is 3:
                self.suitablePWM.append(x.pin_number)
        
        for pin in self.digital.keys():
            self.digital[pin].setEnabled(True if pin in self.suitableDig else False)
        for pin in self.servo:
            if pin in self.suitableServo:
                if self.mw.board.pins[pin].mode is not 4:
                    self._groupEnabled(self.servo.index(pin)+1, True)
            else:
                self._groupEnabled(self.servo.index(pin)+1, False)
        for pin in self.pwm:
            if pin in self.suitablePWM:
                self._groupEnabledP(self.pwm.index(pin)+1, True)
            else:
                self._groupEnabledP(self.pwm.index(pin)+1, False)

    @pyqtSlot(int, int)
    def _updateServo(self, group, angle):
        if not self.sliders[group-1].isValid():
            return
        curStep = self.steps[self.index.value()-1]
        curStep.servo[group-1] = angle
        pin = int(eval("self.mw.seqGb%d" % group).property("title").toString().split()[1])
        logger.debug("Moved servo on pin "+str(pin)+" to "+str(angle)+"º")
        self.mw.board.pins[pin].write(angle)

    @pyqtSlot(int, int)
    def _updatePWM(self, group, value):
        curStep = self.steps[self.index.value()-1]
        curStep.pwm[group-1] = value
        pin = int(eval("self.mw.seqGbP%d" % group).property("title").toString().split()[1])
        logger.debug("Changed PWM on pin "+str(pin)+" to "+str(value))
        self.mw.board.pins[pin].write(value/100)
