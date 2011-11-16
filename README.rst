Platex
======

Platex is an experimentation platform based on Arduino, Firmata and Python that will allow you to interface with chips, sensors and shields without writing a single line of code.

Installation
------------

**Windows**

#. Install `Python 2.7`_

#. Install `PyQt 4.8`_

#. Get *pyserial* ::

    > cd \Python27\Scripts
    > easy_install pip
    > pip install pyserial

#. Download `source code`_

#. Build Qt files ::

    > mkpyqt.py -b -r

#. Execute ``platex.pyw``

**Linux** [#]_

#. Install all dependencies ::

    $ sudo apt-get install git avrdude python-qt4 python-pip
    $ sudo pip install pyserial --upgrade

#. Download source code ::

    $ git clone https://github.com/chiva/Platex.git

#. Build Qt files ::

    $ python mkpyqt.py -b -r

#. Run main script ::

    $ python platex.pyw

.. [#] For Linux 11.10 Oneiric Ocelot

**Mac** [#]_

#. Go to the *App Store* and download and install *Xcode*

#. Install macports_

#. Install dependencies ::

    $ sudo port install py27-pyqt4 && sudo port select --set python python27

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

.. _Python 2.7: http://python.org/ftp/python/2.7.2/python-2.7.2.msi
.. _PyQt 4.8: http://www.riverbankcomputing.co.uk/static/Downloads/PyQt4/PyQt-Py2.7-x86-gpl-4.8.6-1.exe
.. _source code: https://github.com/chiva/Platex/downloads
.. _macports: https://distfiles.macports.org/MacPorts/MacPorts-2.0.3-10.7-Lion.dmg