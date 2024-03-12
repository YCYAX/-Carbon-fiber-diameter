"""
表格导出
"""
import os
import time
import openpyxl


class Xlsx:
    """
    表格导出类
    """
    # 日期
    DAY: str = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    # 路径
    FILE_ALL_NAME: str = f'./result/分析数据{DAY}.xlsx'

    @classmethod
    def valDir(cls) -> None:
        """
        验证文件夹
        :return: None
        """
        # 验证路径
        if os.path.isdir("./result/"):
            pass
        else:
            # 创建文件夹
            os.mkdir("./result/")

    @classmethod
    def valFile(cls) -> None:
        """
        验证文件
        :return: None
        """

        def val(file_name: str) -> None:
            """
            验证文件
            :param file_name: 文件路径
            :return: None
            """
            # 验证路径
            if os.path.isfile(file_name):
                pass
            else:
                # 获取活动表
                workbook = openpyxl.Workbook()
                # 获取表格
                sheet = workbook.active
                # 写入表头
                columns = ['A1', 'B1', 'C1', 'D1']
                columns_info = ['图片名称', '选择的倍率', '像素值', '计算所得直径μm']
                for index in range(len(columns)):
                    sheet[columns[index]] = columns_info[index]
                # 保存内容
                workbook.save(file_name)
                workbook.close()

        val(cls.FILE_ALL_NAME)

    def writeData(self, data: list) -> bool:
        """
        写入数据
        :param data: 数据
        :return: True
        """
        # 匹配模式
        workbook = openpyxl.load_workbook(self.FILE_ALL_NAME)
        # 获取表格
        sheet = workbook.active
        # 添加时间
        try:
            for item in data:
                sheet.append(item)
        except ValueError:
            return False
        # 保存数据
        workbook.save(self.FILE_ALL_NAME)
        workbook.close()
        return True
