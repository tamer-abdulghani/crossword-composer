import sys
from PyQt5.QtWidgets import QApplication, QWidget
from gui.gui import *
from gui.gui_controller import *

app = QApplication(sys.argv)
crosswords = Gui_controller(app)
crosswords.show()
sys.exit(app.exec_())