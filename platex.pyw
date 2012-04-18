#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sip
sip.setapi('QString', 2)

from PyQt4 import QtCore, QtGui
import sys, logging, os

from ui.mainwindow import MainWindow
import resources_rc

if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)-8s %(asctime)s %(module)-12s %(message)s", level=logging.DEBUG)

    logger = logging.getLogger(__name__)
    logger.debug("Working dir: "+os.getcwd())
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("Universidad de La Rioja")
    app.setOrganizationDomain("unirioja.es")
    app.setApplicationName("Platex")
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
