from PyQt5.QtWidgets import QApplication
import sys
from src.Window import Window

style_sheet = """
    background-color: #ffffff;
"""

app = QApplication(sys.argv)
window = Window()
window.setStyleSheet(style_sheet)
window.show()
sys.exit(app.exec_())
