# -*- coding: utf-8 -*-

import logging
from functools import partial

from PyQt4.Qwt5 import QwtPlotGrid, QwtPlotCurve, QwtPlot, QwtPlotItem
from PyQt4.Qt import Qt, QPen
from PyQt4.QtCore import pyqtSlot

logger = logging.getLogger(__name__)
HISTORY = 60

class AnalogTab(object):

    def __init__(self, mwHandle):
        self.mw = mwHandle
        self.curves = list()
        self.data = list()
        self.bars = list()
        for i in xrange(0, 6):
            self.bars.append({ 'group' : eval("self.mw.gbAnalog%d" % (i)),
                               'bar' : eval("self.mw.analogBar%d" % (i)),
                               'label' : eval("self.mw.lbAnalog%d" % (i)), 
                               'active' : eval("self.mw.analogShow%d" % (i)) })
            eval("self.mw.analogShow%d" % (i)).stateChanged.connect(partial(self._channelVisible, i))
        
        self.mw.analogPlot.setAutoReplot(False)
        self.mw.analogPlot.plotLayout().setAlignCanvasToScales(True)
        grid = QwtPlotGrid()
        grid.enableXMin(True)
        grid.enableYMin(True)
        grid.attach(self.mw.analogPlot)
        grid.setPen(QPen(Qt.black, 0, Qt.DotLine))
        grid.setMinPen(QPen(Qt.lightGray, 0, Qt.DotLine))
        self.mw.analogPlot.setAxisScale(QwtPlot.xBottom, 0, HISTORY)
        self.mw.analogPlot.setAxisScale(QwtPlot.yLeft, 0, 5)
        
        self.mw.analogUnits.insertItems(0, ("Voltios", "Cuentas"))
        self.mw.board.updateAnalog.connect(self._newSample)
        self.mw.analogUnits.currentIndexChanged.connect(self._changedUnits)
        self.mw.analogUnitsTime.currentIndexChanged.connect(self._changedUnitsTime)
        self.mw.analogTime.valueChanged[int].connect(self._changedTime)
        
        colors = (Qt.blue, Qt.red, Qt.black, Qt.darkGreen, Qt.darkCyan, Qt.magenta)
        for i in xrange(0, 6):
            curve = QwtPlotCurve()
            curve.setPen(QPen(colors[i], 2))
            curve.attach(self.mw.analogPlot)
            self.curves.append(curve)
            self.data.append(self._zeros(HISTORY+1))
            self.bars[i]['bar'].setFillBrush(colors[i])
        
        self.mw.analogPlot.replot()

    @pyqtSlot(int, int)
    def _newSample(self, channel, value):
        if self.mw.analogUnits.currentIndex() is 0:
            value = round(float(value*5) / 1023, 2)
        self.data[channel] = self.data[channel][1:]
        self.data[channel].append(value)
        self.curves[channel].setData(range(0, HISTORY+1), self.data[channel])
        self._updatePlot(channel)

    def _updatePlot(self, channel):
        if self.mw.analogUnits.currentIndex() is 0:
            self.bars[channel]['bar'].setValue(round(self.data[channel][HISTORY], 2))
            self.bars[channel]['label'].setText(str(round(self.data[channel][HISTORY], 2)))
        else:
            self.bars[channel]['bar'].setValue(int(self.data[channel][HISTORY]))
            self.bars[channel]['label'].setText(str(int(self.data[channel][HISTORY])))
        self.mw.analogPlot.replot()

    def enterTab(self):
        logger.debug("Entering analog tab")
        self._changedTime(self.mw.analogTime.value())
        for pin in self.mw.board.pins:
            if pin.type is 2:
                channel = pin.pin_number-14
                if pin.mode is 2:
                    pin.enable_reporting()
                    logger.debug("Enabled analog reporting of analog pin "+str(channel))
                    self.curves[channel].setVisible(self.bars[channel]['active'].isChecked())
                    self.bars[channel]['group'].setEnabled(True)
                else:
                    self.curves[channel].setVisible(False)
                    self.bars[channel]['group'].setEnabled(False)
                    self.bars[channel]['bar'].setValue(0)
                    self.bars[channel]['label'].setText(str(0))
                self.data[channel] = self._zeros(HISTORY+1)
                self.curves[channel].setData(range(0, HISTORY+1), self.data[channel])
                self._updatePlot(channel)

    def exitTab(self):
        logger.debug("Exiting analog tab")
        for pin in self.mw.board.pins:
            if pin.type is 2 and pin.mode is 2:
                channel = pin.pin_number-14
                logger.debug("Disabled analog reporting of analog pin "+str(channel))
                pin.disable_reporting()
                self.data[channel] = self._zeros(HISTORY+1)
        self.mw.board.sampling_interval()

    def _zeros(self, length):
                x = list()
                for i in xrange(0, length):
                    x.append(0)
                return x

    def _resizeHistory(self, factor):
        for channel in xrange(0, len(self.data)):
            for sample in xrange(0, len(self.data[channel])):
                self.data[channel][sample] *= factor
            self.curves[channel].setData(range(0, HISTORY+1), self.data[channel])
            self._updatePlot(channel)

    @pyqtSlot(int)
    def _changedUnits(self, index):
        if index is 0:
            logger.debug("Changed analog units to volts")
            self._resizeHistory(5.0/1024)
            self.mw.analogPlot.setAxisScale(QwtPlot.yLeft, 0, 5)
            self.mw.analogPlot.replot()
            for bar in self.bars:
                bar['bar'].setRange(0, 5)
        else:
            logger.debug("Changed analog units to counts")
            self._resizeHistory(1024.0/5)
            self.mw.analogPlot.setAxisScale(QwtPlot.yLeft, 0, 1024)
            self.mw.analogPlot.replot()
            for bar in self.bars:
                bar['bar'].setRange(0, 1024)
        self.mw.analogPlot.replot()

    @pyqtSlot(int, int)
    def _channelVisible(self, channel, state):
        self.curves[channel].setVisible(state)
        self._updatePlot(channel)

    @pyqtSlot(int)
    def _changedUnitsTime(self, index):
        value = self.mw.analogTime.value()
        self.mw.analogTime.blockSignals(True)
        if index is 0:
            self.mw.analogTime.setRange(19, 16383)
            self.mw.analogTime.setValue(value*1000)
        else:
            self.mw.analogTime.setRange(0, 16)
            self.mw.analogTime.setValue(value/1000)
        self.mw.analogTime.blockSignals(False)

    @pyqtSlot(int)
    def _changedTime(self, time):
        if self.mw.analogUnitsTime.currentIndex() is 0:
            self.mw.board.sampling_interval(time)
        else:
            self.mw.board.sampling_interval(time*1000)
