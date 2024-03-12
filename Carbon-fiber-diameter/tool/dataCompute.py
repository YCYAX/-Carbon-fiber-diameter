"""
数据计算
"""
from typing import List, Dict, Any, Tuple

from log.log import log
from tool.draw import drawBitumen
import sympy
import random
import math

OLD_WIGHT = 2592
OLD_HIGH = 1944
NEW_WIGHT = 1280
NEW_HIGH = 720


@log
def linearEquation(pos: list[list[tuple[int, int], tuple[int, int]]]) -> list[dict[float | str]]:
    """
    计算直线方程
    :param pos: 点的坐标
    :return: 所有直线方程
    """
    lines = []
    # 循环读取
    for pos_list in pos:
        # 创建方程
        k = sympy.Symbol('k')
        b = sympy.Symbol('b')
        # 获取点
        x1, y1 = pos_list[0]
        x2, y2 = pos_list[1]
        f1 = k * x1 + b - y1
        f2 = k * x2 + b - y2
        # 获取结果
        res = sympy.solve([f1, f2], [k, b])
        # 添加方程
        line_b = eval(str(res[b]))
        line_k = eval(str(res[k]))
        line = {'b': line_b,
                'k': line_k,
                'function': f"({line_k}) * x + ({line_b}) - y"}
        lines.append(line)
    return lines


@log
def lineVertical(pos: list[list[tuple[int, int], tuple[int, int]]], lines: list[dict[float | str]]) -> \
        tuple[list[float], list[list[tuple[int, int]]]]:
    """
    垂直直线计算
    :param pos: 点的坐标
    :param lines: 直线信息
    :return: 平均像素列表/垂直坐标
    """

    def map_range_x(val: int | float) -> int | float:
        """
        区间映射x
        :param val:被映射值
        :return: 映射后数值
        """
        mapped_val = (val - 0) * (2592 - 0) / (1280 - 0) + 0
        return mapped_val

    def map_range_y(val: int | float) -> int | float:
        """
        区间映射y
        :param val:被映射值
        :return: 映射后数值
        """
        mapped_val = (val - 0) * (1944 - 0) / (720 - 0) + 0
        return mapped_val

    # 计数器
    NUMBER = 1
    # 取平均数次数，请注意，实际上我们将对您填写的次数*2，填写4次实际取8次
    # 对该沥青丝的每一组边随机取值，所以双倍取次数
    AVERAGE = 4
    # 总直径列表
    D = []
    # 直径
    d = 0
    # 垂直线上坐标
    vertical_list = []
    for index in range(len(pos)):
        # print(index)
        # 两条直线为一组，奇数对比后一条，偶数对比前一条
        if NUMBER % 2 != 0:
            # 获取对比直线方程
            contrast_line = lines[index + 1]['function']
        else:
            # 获取对比直线方程
            contrast_line = lines[index - 1]['function']
        # 获取x范围
        x1 = pos[index][0][0]
        x2 = pos[index][1][0]
        if x1 > x2:
            xMax = x1
            xMin = x2
        elif x2 > x1:
            xMax = x2
            xMin = x1
        else:
            xMin, xMax = x1, x2
        # 获取已知直线方程k,b
        line_k = lines[index]['k']
        line_b = lines[index]['b']
        for i in range(AVERAGE):
            # 随机取垂直直线x点
            vertical_x = random.randint(xMin, xMax)
            # 计算垂直直线y点
            vertical_y = line_k * vertical_x + line_b
            # 因两条直线垂直时，斜率乘积为-1
            vertical_k = -1 / line_k
            # 计算垂直直线b
            vertical_b = vertical_y - (vertical_k * vertical_x)
            # 计算该垂直线与另一条直线交点
            x = sympy.Symbol('x')
            y = sympy.Symbol('y')
            f1 = vertical_k * x + vertical_b - y
            f2 = eval(contrast_line)
            res = sympy.solve([f1, f2], [x, y])
            # 处理结果,得到交点坐标
            focal_x = eval(str(res[x]))
            focal_y = eval(str(res[y]))
            # 计算直线距离 两点间距离公式
            d += math.pow(((map_range_x(vertical_x) - map_range_x(focal_x)) ** 2) +
                          ((map_range_y(vertical_y) - map_range_y(focal_y)) ** 2), 0.5)
            # print(d)
            # 存入数据
            vertical_list.append([(vertical_x, vertical_y), (int(focal_x), int(focal_y))])
        # 两条直线为一组，偶数清除d数据
        if NUMBER % 2 == 0:
            D.append(d)
            d = 0
        NUMBER += 1
    # 平均像素
    return [i / AVERAGE / 2 for i in D], vertical_list


@log
def pixelRestoration(zoomPixel: list[float], INPUT_POWER: int) -> list[float]:
    """
    像素还原
    :param zoomPixel: 缩放前像素列表
    :param INPUT_POWER: 输入倍率
    :return: 按比例还原后像素列表
    """
    # 40倍比例尺
    SCALE = 0.17
    # 默认倍率
    POWER = 40
    # 计算
    originalPixel = [i * SCALE * (POWER / INPUT_POWER) for i in zoomPixel]
    return originalPixel
