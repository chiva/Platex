import sip
sip.setapi('QString', 2)

from PyQt4 import QtCore, QtGui
import sys, logging

from ui.mainwindow import MainWindow
import resources_rc

if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)-10s %(asctime)s %(message)s", level=logging.DEBUG)

    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("Universidad de La Rioja")
    app.setOrganizationDomain("unirioja.es")
    app.setApplicationName("Platex")
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
