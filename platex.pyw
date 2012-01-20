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
    os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
    logger.debug("Current working dir: %s", os.getcwd())
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("Universidad de La Rioja")
    app.setOrganizationDomain("unirioja.es")
    app.setApplicationName("Platex")
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
