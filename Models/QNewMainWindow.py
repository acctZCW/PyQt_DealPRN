import os
import shutil
import sys

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from designs import StartAlert


class QNewMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(QNewMainWindow, self).__init__(parent)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '提示', '是否关闭窗口？',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 删除临时目录
            if os.path.exists('C:/ProgramData/PrnTemp'):
                shutil.rmtree('C:/ProgramData/PrnTemp')
            event.accept()
            sys.exit(0)
        else:
            event.ignore()
