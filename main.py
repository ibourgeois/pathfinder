from PyQt5.QtWidgets import QApplication
import sys
from src.Window import Window

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
