# -*- coding: utf-8 -*-

"""
This module contains the class MainWindow.
"""

import logging, inspect, time
from PyQt4.QtGui import QMainWindow, QPushButton
from PyQt4.QtCore import pyqtSignature, SIGNAL, SLOT, QTimer
from pyfirmata import Arduino, util

from Ui_mainwindow import Ui_mainWindow
from selectportdlg import SelectPortDlg

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow, Ui_mainWindow):
    """
    MainWindow: this is the class that manages all the funcionality of receiving input from the user.
    """

    def __init__(self, parent=None):
        """
        Default Constructor. It can receive a top window as parent. 
        """
        logging.debug("Creating MainWindow")
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # Build object name, evaluate the string to obtain it and bind the clicked() signal
        for x in xrange(2, 20):
            self.connect(eval("self.pin"+str(x)), SIGNAL("clicked()"), self.pinClicked)
        QTimer.singleShot(0, self.selectPort)
        
        self.board = None

    def selectPort(self):
        # Devolver objeto pyfirmata, mirar ejemplo libro paint
        dialog = SelectPortDlg(self)
        dialog.exec_()
        # If empty list of boards is returned, we exit
        self.board = dialog.getBoard()
        print self.board
        if not self.board:
            self.close()

    def pinClicked(self):
        pin = self.sender()
        if not isinstance(pin, QPushButton):
            logger.warning(inspect.stack()[0][3] + "(): Not a QPushButton")
            return
        if not pin.property("analog").isValid():
            logger.warning("%s(): '%s' shouldn't be connected to this method. Missing 'analog' property", inspect.stack()[0][3], unicode(pin.property("objectName").toString()))
            return 
        current = unicode(pin.text())
        if current == 'N':
            pin.setText('I')
        elif current == 'I':
            pin.setText('O')
            self.board.digital[13].write(1)
        elif current == 'O' and pin.property("analog").toBool():
            pin.setText('A')
        else:
            pin.setText('N')
        pin.setStyleSheet("/* */") #Empty stylesheet to force redraw with the stylesheet set in Qt-Designer
        logger.debug("%s(): '%s' change its mode to '%s'", inspect.stack()[0][3], unicode(pin.property("objectName").toString()), unicode(pin.text()))
