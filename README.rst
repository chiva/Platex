Platex
======

Platex is an experimentation platform based on Arduino, Firmata and Python that will allow you to interface with chips, sensors and shields without writing a single line of code.

Installation
------------

NOTE: compiled version of the Arduino sketch to run Platex is not provided in the repository, please upload ``avrdude/PlatexFirmata/PlatexFirmata.ino`` with the `Arduino software`_.

**Windows**

#. Download and execute `Python(x,y)`_

#. Select at least required libraries:

   - Python 2.7.x
   - Python

     - PyQt
     - PyQwt
     - PySerial

#. Download `Platex source code`_

#. Build Qt files ::

   > mkpyqt.py -b -r

#. Execute ``platex.pyw``

**Linux** [#]_

#. Install all dependencies ::

   $ sudo apt-get install git avrdude python-qt4 pyqt4-dev-tools python-pip qt4-qmake g++ libqt4-dev python-sip-dev
   $ sudo pip install pyserial --upgrade

#. Install PyQwt

   First, download `PyQwt source code`_ ::

   $ tar -zxvf PyQwt-5.2.0.tar.gz
   $ cd PyQwt-5.2.0/configure
   $ python configure.py -Q ../qwt-5.2 --qt4 --disable-numarray --disable-numeric --disable-numpy
   $ make
   $ make install
   $ rm -r PyQwt*
    
#. Download source code ::

   $ git clone https://github.com/chiva/Platex.git

#. Build Qt files ::

   $ python mkpyqt.py -b -r

#. Run main script ::

   $ python platex.pyw

.. [#] For Linux 11.10 Oneiric Ocelot

**Mac** [#]_

**Note:** non working right now, instructions will be updated as soon as possible

#. Go to the *App Store* and download and install *Xcode*

#. Install macports_

#. Install dependencies ::

    $ sudo port install py27-pyqt4 avrdude && sudo port select --set python python27

#. Go for a very long walk

#. Get *pySerial* ::

    $ sudo easy_install pip
    $ sudo pip install pyserial

#. Download source code ::

   $ git clone https://github.com/chiva/Platex.git

#. Build Qt files ::

    $ python mkpyqt.py -b -r

#. Run main script ::

    $ python platex.pyw

.. [#] For Mac OS X 10.7 Lion

.. _Arduino software: http://code.google.com/p/arduino/wiki/Arduino1
.. _Python(x,y): http://python.org/ftp/python/2.7.2/python-2.7.2.msi
.. _Platex source code: https://github.com/chiva/Platex/downloads
.. _PyQwt source code: http://prdownloads.sourceforge.net/pyqwt/PyQwt-5.2.0.tar.gz?download
.. _macports: https://distfiles.macports.org/MacPorts/MacPorts-2.0.3-10.7-Lion.dmg