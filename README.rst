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

Execute this in command line ::

$ sudo git clone git://gist.github.com/1427486.git build_scripts && sudo ./build_scripts/build-linux.sh

DO NOT BUILD IN PRODUCTION ENVIROMENTS !!!

Until a packaging and installing toolchain is developed you can run the main script inside the ``Platex`` folder created where you run the previous script ::

$ python platex.pyw

.. [#] For Linux 11.10 Oneiric Ocelot

**Mac** [#]_

Execute this in command line ::

$ sudo git clone git://gist.github.com/1427486.git build_scripts && sudo ./build_scripts/build-mac.sh

DO NOT BUILD IN PRODUCTION ENVIROMENTS !!!

Until a packaging and installing toolchain is developed you can run the main script inside the ``Platex`` folder created where you run the previous script ::

$ python platex.pyw

.. [#] For Mac OS X 10.7 Lion

.. _Arduino software: http://code.google.com/p/arduino/wiki/Arduino1
.. _Python(x,y): http://python.org/ftp/python/2.7.2/python-2.7.2.msi
.. _Platex source code: https://github.com/chiva/Platex/downloads
.. _PyQwt source code: http://prdownloads.sourceforge.net/pyqwt/PyQwt-5.2.0.tar.gz?download