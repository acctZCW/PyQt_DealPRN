import csv
import os
import matplotlib.pyplot as plt


def ScienceNum2Num(science_num: str):
    """
    将科学计数法数字转换为一般数字

    :param science_num: str
    :return: normal_num: float
    """
    temp = science_num.split('e+')
    base, index = temp[0], temp[1]
    return round(float(base) * (10 ** (int(index))), 3)


class PlotPrn(object):
    def __init__(self):
        self.x_list = []
        self.y_list = []
        self.sweepPoint = 721
        self.rotateTime = 28.8

        self.xName = "Time"
        self.yName = "dB"

        self.x_label = ""
        self.y_label = ""
        self.title = ""

        self.graphPath = r"./graphs"
        self.searchIsempty = True

        self.file_name = ""
        self.file_folder = ""

        #print("PlotPrn构造函数调用")

    def setupPlotPrn(self):
        self.x_list = []
        self.y_list = []
        self.sweepPoint = 721
        self.rotateTime = 28.8

        self.xName = "Time"
        self.yName = "dB"

        self.x_label = ""
        self.y_label = ""
        self.title = ""

        self.graphPath = r"./graphs"
        self.searchIsempty = True

        self.file_name = ""
        self.file_folder = ""

        #print("setupPlotPrn调用")

    def Time2Angle(self, time: float):
        temp = (float(time) * 360) / float(self.rotateTime)

    def ReadPrn(self, file_name: str):
        """读取Prn文件，并将数据写入x_list和y_list。同时读取用户输入信息，如标题、标签

        :param file_name: str
        :return:
        """
        with open(file_name) as f:
            reader = csv.reader(f)
            header_row = next(reader)
            header_row = next(reader)

            x_index = [i for i, x in enumerate(header_row) if x.find(self.xName) != -1]
            y_index = [i for i, x in enumerate(header_row) if x.find(self.yName) != -1]

            # 对表头进行判定
            if x_index and y_index:
                self.searchIsempty = False
                for row in reader:
                    self.x_list.append(row[x_index[0]])
                    self.y_list.append(row[y_index[0]])
        temp = list(map(ScienceNum2Num, self.y_list))
        self.y_list = temp
        temp = list(map((lambda time: round((float(time) * 360) / float(self.rotateTime)-180, 2)), self.x_list))
        self.x_list = temp

        # print("读取到的X列表为")
        # print(self.x_list)
        # print("读取到的Y列表为")
        # print(self.y_list)

    def Plot(self):
        """对单个文件进行打印

        """
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False
        fig, ax = plt.subplots()
        ax.plot(self.x_list, self.y_list, c='red')

        # 设置图像参数
        ax.set_xlabel(self.x_label, fontsize=16)
        ax.set_ylabel(self.y_label, fontsize=16)
        ax.set_title(self.title, fontsize=20)

        if not os.path.exists(os.path.abspath('C:/ProgramData/PrnTemp')):
            os.makedirs(os.path.abspath('C:/ProgramData/PrnTemp'))
        plt.savefig(os.path.join(os.path.abspath('C:/ProgramData/PrnTemp'),
                                 self.file_name.split(".")[0]))

        self.x_list, self.y_list = [], []
        # print("plot success")

    def Plot_all(self, save_folder):
        # print("绘制的文件为：")
        # print(save_folder)
        temp = list(map(ScienceNum2Num, self.y_list))
        self.y_list = temp
        temp = list(map((lambda time: round((float(time) * 360) / float(self.rotateTime)-180, 2)), self.x_list))
        self.x_list = temp

        if self.searchIsempty:
            self.x_list, self.y_list = [], []
        # print("需要进行绘图的列表为：")
        # print(self.x_list)
        # print(self.y_list)

        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        fig, ax = plt.subplots()
        ax.plot(self.x_list, self.y_list, c='red')
        # print("plot success")

        # 设置图像参数
        ax.set_xlabel(self.x_label, fontsize=16)
        ax.set_ylabel(self.y_label, fontsize=16)
        ax.set_title(self.title, fontsize=20)

        self.graphPath = r"C:\Users\zcw\Desktop\Try the python2Origin\graphs"
        if not os.path.exists(os.path.abspath(self.graphPath)):
            os.makedirs((os.path.abspath(self.graphPath)))
        plt.savefig(os.path.abspath(self.graphPath) + "\\" +
                    (save_folder.split('\\')[-1]).split('.')[0])

        self.x_list, self.y_list = [], []
        plt.clf()

