Platex
======

Platex is an experimentation platform based on Arduino, Firmata and Python that will allow you to interface with chips, sensors and shields without writing a single line of code.

Installation
------------

**Linux**

Download the appropiate version for your Linux distribution from the Downloads_ section.

To install and run the project in Ubuntu, download the latest ``deb`` package, install it by double-clicking and once finished run ``platex`` in a terminal.

.. _Downloads: https://github.com/chiva/Platex/downloads

Building
--------

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

Execute this in a terminal ::

$ sudo bash -c "wget https://raw.github.com/gist/1427486/build-linux.sh && bash build-linux.sh"

DO NOT BUILD IN PRODUCTION ENVIROMENTS !!!

When finished a ``Platex-dist`` folder will appear where you executed the script. It contains the ``rpm`` and ``deb`` package installers for the different flavours of Linux.

.. [#] For Linux 11.10 Oneiric Ocelot

**Mac** [#]_

Execute this in a terminal ::

$ sudo bash -c "curl -O https://raw.github.com/gist/1427486/build-mac.sh && bash build-mac.sh"

DO NOT BUILD IN PRODUCTION ENVIROMENTS !!!

Until a packaging and installing toolchain is developed you can run the main script inside the ``Platex`` folder created where you run the previous script ::

$ /Library/Frameworks/Python.framework/Versions/Current/bin/python platex.pyw

.. [#] For Mac OS X 10.7 Lion

.. _Arduino software: http://code.google.com/p/arduino/wiki/Arduino1
.. _Python(x,y): http://python.org/ftp/python/2.7.2/python-2.7.2.msi
.. _Platex source code: https://github.com/chiva/Platex/downloads
.. _PyQwt source code: http://prdownloads.sourceforge.net/pyqwt/PyQwt-5.2.0.tar.gz?download