from PyQt5.QtCore import QObject, pyqtSignalimport threading
from threading import *

class ComputeThread(Thread):
    update_signal = pyqtSignal(int)

    def __init__(self, window):
        threading.Thread.__init__(self)
        self.window = window

    def run(self):
        for i in range(10):
            # Do some computation...
            self.update_signal.emit(i)
