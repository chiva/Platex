# -*- coding: utf-8 -*-

"""
This module contains the class MainWindow.
"""

import logging
from PyQt4.QtGui import QMainWindow, QPushButton, QMenu, QActionGroup
from PyQt4.QtCore import QTimer, pyqtSlot
from pyfirmata import Arduino, util

from Ui_mainwindow import Ui_mainWindow
from selectportdlg import SelectPortDlg
from mode import ModeTab
from analog import AnalogTab
from digital import DigitalTab
from pwm import PWMTab
from servo import ServoTab
from motor import MotorTab
from sequencer import SequencerTab

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow, Ui_mainWindow):
    """
    MainWindow: this is the class that manages all the funcionality of receiving input from the user.
    """

    def __init__(self, parent=None):
        """
        Default Constructor. It can receive a top window as parent. 
        """
        QMainWindow.__init__(self, parent)
        logger.debug("Created MainWindow")
        self.setupUi(self)
        
        for x in xrange(2, 20):
                eval("self.pin%02d" % (x)).setStyleSheet("* {padding:0px}")
        self.board = None
        self.lastIndex = 0
        
        QTimer.singleShot(0, self.selectPort)

    def selectPort(self):
        dialog = SelectPortDlg(self)
        
        dialog.exec_()
        # If empty object is returned, we exit
        self.board = dialog.getBoard()
        if not self.board:
            self.close()
        else:
            self.tabs = (ModeTab(self), DigitalTab(self), AnalogTab(self), PWMTab(self), ServoTab(self), MotorTab(self), SequencerTab(self))
            self.tabs[0].enterTab()
            
            self.it = util.Iterator(self.board)
            self.it.start()
    
    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, index):
        """
        Slot documentation goes here.
        """
        self.tabs[self.lastIndex].exitTab()
        self.tabs[index].enterTab()
        self.lastIndex = index
