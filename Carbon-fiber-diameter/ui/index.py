"""
主页面
"""
import cv2
import numpy as np
from PyQt5.QtGui import QPixmap
from tool.xlsx import Xlsx
from tool.draw import drawBitumen
from tool.pictureProcessing import imagePreprocessing
from tool.countAmont import posBitumenWire
from box.messageBox import MessageBox
from tool.dataCompute import linearEquation, lineVertical, pixelRestoration
from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QFileDialog, QLabel, QLineEdit


class Index(QWidget):
    def __init__(self):
        super().__init__()
        """
        资源验证
        """
        # 文件夹
        Xlsx.valDir()
        # 表格
        Xlsx.valFile()
        """
        初始化其他类
        """
        self.xlsx = Xlsx()
        """
        全局属性
        """
        # 图片路径
        self.JPGPath: str = ''
        # 单次结果
        self.res: list = []
        # 全局结果
        self.allres: list = []
        # 放大值
        self.SCALE: int = 4
        # 形状方式
        self.TYPE: str = "up down"
        # 窗口高宽
        self.UIHIGH = 600
        self.UIWIDTH = 500
        # 启动ui
        self.initUi()

    def initUi(self):
        """
        窗口属性
        """
        # 大小
        self.resize(self.UIWIDTH, self.UIHIGH)
        # 标题
        self.setWindowTitle("沥青丝直径识别")
        """
        划分区域
        """
        # top栏
        top_widget = QWidget(self)
        top_widget.setGeometry(0, 0, self.UIWIDTH, 50)
        # 图片显示区域
        image_widget = QWidget(self)
        image_widget.setGeometry(0, 50, 500, 500)
        # 文字显示区域
        down_widget = QWidget(self)
        down_widget.setGeometry(0, 550, self.UIWIDTH, 50)
        """
        创建下拉菜单
        """
        # 放大倍数
        scale = QComboBox(top_widget)
        scale.setGeometry(100, 0, 100, 50)
        scale.addItems(['4x', '10x', '40x', '100x'])
        scale.currentIndexChanged[str].connect(self.scaleChanged)
        # 丝的形态
        bitumenType = QComboBox(top_widget)
        bitumenType.setGeometry(200, 0, 100, 50)
        bitumenType.addItems(['上下', '左右', '左斜', '右斜'])
        bitumenType.currentIndexChanged[str].connect(self.typeChanged)
        """
        创建按钮
        """
        # 分析图片按钮
        main_button = QPushButton('开始分析', top_widget)
        main_button.setGeometry(0, 0, 100, 50)
        main_button.clicked.connect(self.main)
        # 打开图片
        open_button = QPushButton('打开图片', top_widget)
        open_button.setGeometry(300, 0, 100, 50)
        open_button.clicked.connect(self.openJPG)
        # 数据导出按钮
        out_button = QPushButton('导出数据', top_widget)
        out_button.setGeometry(400, 0, 100, 50)
        out_button.clicked.connect(self.dataOut)
        """
        创建标签
        """
        # 展示图片
        self.detect_image = QLabel(image_widget)
        self.detect_image.resize(self.UIHIGH, 500)
        self.detect_image.move(0, 0)
        """
        创建文本框
        """
        # 结果
        self.detect_res = QLineEdit(down_widget)
        self.detect_res.resize(self.UIWIDTH, 50)
        self.detect_res.move(0, 0)
        self.detect_res.setReadOnly(True)

    def main(self):
        """
        主处理逻辑
        """
        # unicode转gbk，字符串变为字节数组
        # 字节数组直接转字符串，不解码
        tmp_path = self.JPGPath.encode('gbk').decode()
        # print(tmp_path)
        # 读取图片
        try:
            image_array = imagePreprocessing(tmp_path)
            # 获得沥青丝位置
            BitumenPos = posBitumenWire(image_array, self.TYPE)
            # 计算方程
            lines = linearEquation(BitumenPos)
            # 得到垂直之后结果
            res = lineVertical(BitumenPos, lines)
            # 像素结果/垂直点位
            pixel, VerticalPos = res
            # 画图
            drawBitumen(BitumenPos + VerticalPos, self.JPGPath)
            # 获取最后结果
            self.res = pixelRestoration(pixel, self.SCALE)
            # 显示答案
            self.detect_res.setText(str(self.res))
            # 存入结果
            # ['图片名称', '选择的倍率', '像素值', '计算所得直径']
            for index in range(len(pixel)):
                self.allres.append([
                    self.JPGPath.split('/')[-1] + "第" + str(index + 1) + "根", self.SCALE, pixel[index],
                    self.res[index]
                ])
        except:
            self.allres.append([
                self.JPGPath.split('/')[-1] + '此照片读取错误', None, None, None
            ])

    def scaleChanged(self, value: str) -> None:
        """
        放大倍数改变
        :param value: 放大值
        :return: None
        """
        # 获取放大倍数
        self.SCALE = int(value.split('x')[0])
        # print(self.SCALE)

    def typeChanged(self, value: str) -> None:
        """
        方向性状改变
        :param value: 方向值
        :return: None
        """
        # 匹配形状
        match value:
            case '上下':
                self.TYPE = 'up down'
            case '左右':
                self.TYPE = 'left right'
            case '左斜':
                self.TYPE = 'left down'
            case '右斜':
                self.TYPE = 'right down'
        # print(self.TYPE)

    def openJPG(self) -> None:
        """
        获取图片路径并展示
        """
        # 读取路径
        path = QFileDialog.getOpenFileName(None, "请选择要分析的图片", None,
                                           "Photo Files (*.jpg);;Photo Files (*.png);;Photo Files (*.jpeg)")
        # 路径赋值
        self.JPGPath = path[0]
        # print(self.JPGPath)
        # 创建图片对象
        pix = QPixmap(self.JPGPath)
        self.detect_image.setPixmap(pix)
        self.detect_image.setScaledContents(True)

    def dataOut(self) -> None:
        """
        数据导出
        """
        if self.xlsx.writeData(self.allres):
            MessageBox.information("数据导出", '数据导出成功', 1000)
        else:
            MessageBox.warning("数据导出", '数据失败', 1000)
