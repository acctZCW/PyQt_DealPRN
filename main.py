import glob
import os.path
import shutil
import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QApplication, QWidget

from Models import prndeal, QNewMainWindow
from designs import MainWindow, StartAlert


class App_MainWindow(QNewMainWindow.QNewMainWindow, MainWindow.Ui_MainWindow, prndeal.PlotPrn):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setupPlotPrn()
        self.saveFigPath = "C:/"
        self.tempPath = 'C:/ProgramData/PrnTemp'

    @pyqtSlot()
    def on_batchDrawButton_clicked(self):

        get_directory_path = QFileDialog.getExistingDirectory(self, '请选择文件夹', 'C:/')

        files = glob.glob(os.path.join(get_directory_path, "**.prn"))
        if not files:
            QMessageBox.warning(self, "警告", "所选文件夹中没有prn文件")
            return
        # print("读取到的文件为")
        # print(files)
        # 读取文件并绘制
        for f in files:
            self.readFile(f)
            self.Plot()

        # 保存全部图片
        save_file = os.path.join(get_directory_path, 'graphs')
        if not os.path.exists(save_file):
            os.mkdir(save_file)
        filelist = os.listdir(self.tempPath)
        # print(filelist)
        for f in filelist:
            src = os.path.join(self.tempPath, f)
            dst = os.path.join(save_file, f)
            shutil.move(src, dst)

        QMessageBox.information(self, '提示', '绘图已完成')

    @pyqtSlot()
    def on_chooseFileButton_clicked(self):
        # print("the folder has been chosen successfully!")
        get_file_path = QFileDialog.getOpenFileName(self, "选择需要绘制的文件", r'C:\Users\Administrator\Desktop',
                                                    "all files(*.*)")
        self.chooseFileLine.setText(str(get_file_path[0]))

    @pyqtSlot()
    def on_readFileButton_clicked(self):
        # if not self.chooseFileLine.text():
        #     QMessageBox.warning(self, "警告", "请选择文件")
        #     return
        # self.file_folder, self.file_name = os.path.split(self.chooseFileLine.text())
        # self.ReadPrn(self.chooseFileLine.text())
        # # 读入用户自定义绘图信息
        # self.x_label = self.xAxisLine.text()
        # self.y_label = self.yAxisLine.text()
        # self.title = self.titleLine.text()
        #
        # # 将读取数据显示在dataTable中
        # self.tableModel = QtGui.QStandardItemModel()
        # self.tableModel.setHorizontalHeaderItem(0, QtGui.QStandardItem('Angle'))
        # self.tableModel.setHorizontalHeaderItem(1, QtGui.QStandardItem('Gain/dB'))
        # for i in range(len(self.x_list)):
        #     self.tableModel.setItem(i, 0, QtGui.QStandardItem(str(self.x_list[i])))
        #     self.tableModel.setItem(i, 1, QtGui.QStandardItem(str(self.y_list[i])))
        # self.dataTable.setModel(self.tableModel)
        # self.dataTable.resizeColumnToContents(0)
        # self.dataTable.resizeColumnToContents(1)
        # print("the file has been read in!")

        self.readFile(self.chooseFileLine.text())
        # 将读取数据显示在dataTable中
        self.tableModel = QtGui.QStandardItemModel()
        self.tableModel.setHorizontalHeaderItem(0, QtGui.QStandardItem('Angle'))
        self.tableModel.setHorizontalHeaderItem(1, QtGui.QStandardItem('Gain/dB'))
        for i in range(len(self.x_list)):
            self.tableModel.setItem(i, 0, QtGui.QStandardItem(str(self.x_list[i])))
            self.tableModel.setItem(i, 1, QtGui.QStandardItem(str(self.y_list[i])))
        self.dataTable.setModel(self.tableModel)
        self.dataTable.resizeColumnToContents(0)
        self.dataTable.resizeColumnToContents(1)

    @pyqtSlot()
    def on_plotFileButton_clicked(self):
        # self.Plot()
        # pix = QtGui.QPixmap(os.path.join('C:/ProgramData/PrnTemp', self.file_name.split('.')[0] + '.png'))
        # print(os.path.join('C:/ProgramData/PrnTemp', self.file_name.split('.')[0] + '.png'))
        # self.dataGraphics.setPixmap(pix)
        # self.dataGraphics.setScaledContents(True)
        # print("over")
        self.plotFile()

    @pyqtSlot()
    def on_saveFigButton_clicked(self):
        get_directory_path = QFileDialog.getExistingDirectory(self, "选取保存路径", self.saveFigPath)
        shutil.move(os.path.join('C:/ProgramData/PrnTemp', self.file_name.split('.')[0] + '.png'),
                    os.path.join(get_directory_path, self.file_name.split('.')[0] + '.png'))
        self.saveFigPath = get_directory_path

    def readFile(self, filename):
        if not filename:
            QMessageBox.warning(self, "警告", "请选择文件")
            return
        self.file_folder, self.file_name = os.path.split(filename)
        self.ReadPrn(filename)
        # 读入用户自定义绘图信息
        self.x_label = self.xAxisLine.text()
        self.y_label = self.yAxisLine.text()
        self.title = self.titleLine.text()

        # print("the file has been read in!")

    def plotFile(self):
        if (not self.x_list) or (not self.y_list):
            QMessageBox.warning(self, '警告', '未读取数据！')
        self.Plot()
        pix = QtGui.QPixmap(os.path.join(self.tempPath, self.file_name.split('.')[0] + '.png'))
        # print(os.path.join(self.tempPath, self.file_name.split('.')[0] + '.png'))
        self.dataGraphics.setPixmap(pix)
        self.dataGraphics.setScaledContents(True)
        # print("over")


class App_StartAlert(QWidget, StartAlert.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    # 设置高DPI适配，使得设计界面和实际程序界面能够统一
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    # 创建整个窗体
    app = QApplication(sys.argv)
    mainWindow = App_MainWindow()
    startAlert = App_StartAlert()

    mainWindow.show()
    startAlert.show()
    sys.exit(app.exec_())
