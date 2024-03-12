"""
消息类
"""
from PyQt5.QtWidgets import QMessageBox


class MessageBox:
    """
    消息类
    """

    @classmethod
    def warning(cls, titleMessage: str, textMessage: str, animateTime: int) -> None:
        """
        警告消息 提供标题，文字，和自动消失时间
        :param titleMessage: 标题消息
        :param textMessage: 文字消息
        :param animateTime: 自动消失时间
        :return: None
        """
        # 创建box对象
        msgBox = QMessageBox()
        # 设置属性
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(textMessage)
        msgBox.setWindowTitle(titleMessage)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # 自动确认
        msgBox.button(QMessageBox.Ok).animateClick(animateTime)
        msgBox.exec()
        del msgBox

    @classmethod
    def information(cls, titleMessage: str, textMessage: str, animateTime: int) -> None:
        """
        提示消息 提供标题，文字，和自动消失时间
        :param titleMessage: 标题消息
        :param textMessage: 文字消息
        :param animateTime: 自动消失时间
        :return: None
        """
        # 创建box对象
        msgBox = QMessageBox()
        # 设置属性
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(textMessage)
        msgBox.setWindowTitle(titleMessage)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # 自动确认
        msgBox.button(QMessageBox.Ok).animateClick(animateTime)
        msgBox.exec()
        del msgBox
