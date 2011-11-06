from PyQt4.QtCore import QThread, QMutex, QMutexLocker, QWriteLocker, SIGNAL

import threading, serial, time, os, logging
import pyfirmata
from boards import BOARDS

logger = logging.getLogger(__name__)

class SearchBoard(QThread):
    def __init__(self, lock, parent=None):
        super(SearchBoard, self).__init__(parent)
        self.lock = lock
        self.stopped = False
        self.mutex = QMutex()
        self.completed = False
    
    def initialize(self, boards, layout=BOARDS['arduino']):
        self.layout = layout
        self.boards = boards
        self.stopped = False
        self.completed = False
    
    def run(self):
        logging.debug("SearchBoard thread started")
        self.getBoard()
        self.stop()
        self.emit(SIGNAL("finished(bool)"), self.completed)
    
    def stop(self):
        with QMutexLocker(self.mutex):
            self.stopped = True
        logging.debug("SearchBoard thread stopped")
         
    def isStopped(self):
        with QMutexLocker(self.mutex):
            return self.stopped
    
    def getBoard(self):
        """
        Helper function to get the one and only board connected to the computer
        running this. It assumes a normal arduino layout, but this can be
        overriden by passing a different layout dict as the ``layout`` parameter.
        ``base_dir`` and ``identifier`` are overridable as well. It will raise an
        IOError if it can't find a board, on a serial, or if it finds more than
        one.
        """
        ports = []
        for i in xrange(256):
            try:
                s = serial.Serial(i)
                ports.append(s.portstr)
                s.close()
            except serial.SerialException:
                pass
        logger.debug("Found %d serial port(s): %s", len(ports), ports)
        if self.isStopped():
            return
        for port in ports:
            try:
                board = pyfirmata.Board(port, self.layout)
            except ValueError, e:
                logger.warning(str(e))
            except TypeError, e:
                logger.debug(str(e))
            else:
                with QWriteLocker(self.lock):
                    self.boards.append(board)
            if self.isStopped():
                return
        logger.debug("Found %d Arduino board(s): %s", len(self.boards), [x.sp.port for x in self.boards if x.sp.port in ports])
        self.completed = True

class Iterator(threading.Thread):
    def __init__(self, board):
        super(Iterator, self).__init__()
        self.board = board

    def run(self):
        while 1:
            try:
                while self.board.bytes_available():
                    self.board.iterate()
                time.sleep(0.001)
            except (AttributeError, serial.SerialException, OSError), e:
                # this way we can kill the thread by setting the board object
                # to None, or when the serial port is closed by board.exit()
                break
            except Exception, e:
                # catch 'error: Bad file descriptor'
                # iterate may be called while the serial port is being closed,
                # causing an "error: (9, 'Bad file descriptor')"
                if getattr(e, 'errno', None) == 9:
                    break
                try:
                    if e[0] == 9:
                        break
                except (TypeError, IndexError):
                    pass
                raise
                
def to_two_bytes(integer):
    """
    Breaks an integer into two 7 bit bytes.
    
    >>> for i in range(32768):
    ...     val = to_two_bytes(i)
    ...     assert len(val) == 2
    ...
    >>> to_two_bytes(32767)
    ('\\x7f', '\\xff')
    >>> to_two_bytes(32768)
    Traceback (most recent call last):
        ...
    ValueError: Can't handle values bigger than 32767 (max for 2 bits)
    
    """
    if integer > 32767:
        raise ValueError, "Can't handle values bigger than 32767 (max for 2 bits)"
    return chr(integer % 128), chr(integer >> 7)
    
def from_two_bytes(bytes):
    """
    Return an integer from two 7 bit bytes.
    
    >>> for i in range(32766, 32768):
    ...     val = to_two_bytes(i)
    ...     ret = from_two_bytes(val)
    ...     assert ret == i
    ...
    >>> from_two_bytes(('\\xff', '\\xff'))
    32767
    >>> from_two_bytes(('\\x7f', '\\xff'))
    32767
    """
    lsb, msb = bytes
    try:
        # Usually bytes have been converted to integers with ord already
        return msb << 7 | lsb
    except TypeError:
        # But add this for easy testing
        # One of them can be a string, or both
        try:
            lsb = ord(lsb)
        except TypeError:
            pass
        try:
            msb = ord(msb)
        except TypeError:
            pass
        return msb << 7 | lsb
    
def two_byte_iter_to_str(bytes):
    """
    Return a string made from a list of two byte chars.
    
    >>> string, s = 'StandardFirmata', []
    >>> for i in string:
    ...   s.append(i)
    ...   s.append('\\x00')
    >>> two_byte_iter_to_str(s)
    'StandardFirmata'
    
    >>> string, s = 'StandardFirmata', []
    >>> for i in string:
    ...   s.append(ord(i))
    ...   s.append(ord('\\x00'))
    >>> two_byte_iter_to_str(s)
    'StandardFirmata'
    """
    bytes = list(bytes)
    chars = []
    while bytes:
        lsb = bytes.pop(0)
        try:
            msb = bytes.pop(0)
        except IndexError:
            msb = 0x00
        chars.append(chr(from_two_bytes((lsb, msb))))
    return ''.join(chars)
    
def str_to_two_byte_iter(string):
    """
    Return a iter consisting of two byte chars from a string.
    
    >>> string, iter = 'StandardFirmata', []
    >>> for i in string:
    ...   iter.append(i)
    ...   iter.append('\\x00')
    >>> assert iter == str_to_two_byte_iter(string)
     """
    bytes = []
    for char in string:
        bytes += list(to_two_bytes(ord(char)))
    return bytes

def break_to_bytes(value):
    """
    Breaks a value into values of less than 255 that form value when multiplied.
    (Or almost do so with primes)
    Returns a tuple
    
    >>> break_to_bytes(200)
    (200,)
    >>> break_to_bytes(800)
    (200, 4)
    >>> break_to_bytes(802)
    (2, 2, 200)
    """
    if value < 256:
        return (value,)
    c = 256
    least = (0, 255)
    for i in range(254):
        c -= 1
        rest = value % c
        if rest == 0 and value / c < 256:
            return (c, value / c)
        elif rest == 0 and value / c > 255:
            parts = list(break_to_bytes(value / c))
            parts.insert(0, c)
            return tuple(parts)
        else:
            if rest < least[1]:
                least = (c, rest)
    return (c, value / c)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
