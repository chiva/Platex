# -*- coding: utf-8 -*-

import logging

from PyQt4.Qwt5 import QwtPlotGrid, QwtPlotCurve, QwtPlot, QwtPlotItem
from PyQt4.Qt import Qt, QPen
from PyQt4.QtCore import pyqtSlot

logger = logging.getLogger(__name__)
HISTORY = 60

class AnalogTab(object):

    def __init__(self, mwHandle):
        self.mw = mwHandle
        self.curves = {}
        self.data = {}
        self.bars = list()
        for i in xrange(0, 6):
            self.bars.append({ 'group' : eval("self.mw.gbAnalog%d" % (i)),
                               'bar' : eval("self.mw.analogBar%d" % (i)),
                               'label' : eval("self.mw.lbAnalog%d" % (i)) })
        
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
        
        self.mw.cbUnit.insertItems(0, ("Voltios", "Cuentas"))
        self.mw.board.updateAnalog.connect(self.update)
        self.mw.cbUnit.currentIndexChanged.connect(self.changedUnits)
        
        colors = (Qt.blue, Qt.red, Qt.black, Qt.darkGreen, Qt.darkCyan, Qt.magenta)
        for i in xrange(0, 6):
            curve = QwtPlotCurve()
            curve.setPen(QPen(colors[i], 2))
            curve.attach(self.mw.analogPlot)
            self.curves[i] = curve
            self.data[i] = self._zeros(HISTORY+1)
            self.bars[i]['bar'].setFillBrush(colors[i])
        
        self.mw.analogPlot.replot()

    @pyqtSlot(int, int)
    def update(self, channel, value):
        if self.mw.cbUnit.currentIndex() is 0:
            value = round(float(value*5) / 1023, 2)
        self.data[channel] = self.data[channel][1:]
        self.data[channel].append(value)
        self.curves[channel].setData(range(0, HISTORY+1), self.data[channel])
        self.bars[channel]['bar'].setValue(value)
        self.bars[channel]['label'].setText(str(value))
        self.mw.analogPlot.replot()

    def enterTab(self):
        logger.debug("Entering analog tab")
        for pin in self.mw.board.pins:
            if pin.type is 2:
                channel = pin.pin_number-14
                if pin.mode is 2:
                    pin.enable_reporting()
                    logger.debug("Enabled analog reporting of analog pin "+str(channel))
                    self.curves[channel].setVisible(True)
                    self.bars[channel]['group'].setEnabled(True)
                else:
                    self.curves[channel].setVisible(False)
                    self.bars[channel]['group'].setEnabled(False)
                    self.bars[channel]['bar'].setValue(0)
                    self.bars[channel]['label'].setText(str(0))
        self.mw.analogPlot.replot()

    def exitTab(self):
        logger.debug("Exiting analog tab")
        for pin in self.mw.board.pins:
            if pin.type is 2 and pin.mode is 2:
                channel = pin.pin_number-14
                logger.debug("Disabled analog reporting of analog pin "+str(channel))
                pin.disable_reporting()
                self.data[channel] = self._zeros(HISTORY+1)

    def _zeros(self, length):
                x = list()
                for i in xrange(0, length):
                    x.append(0)
                return x

    @pyqtSlot(int)
    def changedUnits(self, index):
        if index is 0:
            self.mw.analogPlot.setAxisScale(QwtPlot.yLeft, 0, 5)
            for bar in self.bars:
                bar['bar'].setRange(0, 5)
        elif index is 1:
            self.mw.analogPlot.setAxisScale(QwtPlot.yLeft, 0, 1024)
            for bar in self.bars:
                bar['bar'].setRange(0, 1024)
        self.mw.analogPlot.replot()
