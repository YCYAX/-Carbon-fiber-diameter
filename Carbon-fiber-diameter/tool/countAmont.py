"""
计算沥青丝数量
"""

import numpy
import numpy as np

from log.log import log


@log
def posBitumenWire(ImageArray: numpy.ndarray, PhotoType: str) -> list[list[tuple[int, int], tuple[int, int]]]:
    """
    定位图片上的沥青丝
    :param ImageArray: 图像数据
    :param PhotoType: 照片方向
    :return: 沥青丝组成
    """
    # 图像的长宽高
    HIGH = 720
    WIDTH = 1280
    # 搜寻边界阈值
    SEARCH_BOUNDARY = 5
    # 检查存在数量阈值
    CHECK_BOUNDARY = 5
    # 列表去重范围
    LIST_REMOVE = 20

    @log
    def searchingCell(check_list: list[int], mode: str) -> list:
        """
        搜索单元格 5*5,正确的点单元格附近应有数据
        :param check_list: 检验点坐标
        :param mode: 方向模式
        :return: 处理后的点坐标
        """
        # 真实点位
        result = []
        real_list = []
        # 匹配模式
        match mode:
            case 'up':
                # 遍历
                for centralPos in check_list:
                    # 确定中心点
                    x = centralPos
                    # print(centralPos)
                    # 检查中心点 5*5 范围内255
                    if x - SEARCH_BOUNDARY < 0:
                        check_array = ImageArray[0:SEARCH_BOUNDARY, x:x + SEARCH_BOUNDARY]
                    elif x + SEARCH_BOUNDARY > WIDTH:
                        check_array = ImageArray[0:SEARCH_BOUNDARY, x - SEARCH_BOUNDARY:x]
                    else:
                        check_array = ImageArray[0:SEARCH_BOUNDARY, x - SEARCH_BOUNDARY:x + SEARCH_BOUNDARY]
                    check_number = np.sum(check_array == 255)
                    # print(check_number)
                    #  判断数量
                    if check_number >= CHECK_BOUNDARY:
                        real_list.append(centralPos)
                # print(real_list)
            case 'down':
                # 遍历
                for centralPos in check_list:
                    # 确定中心点
                    x = centralPos
                    # print(centralPos)
                    # 检查中心点 5*5 范围内255
                    if x - SEARCH_BOUNDARY < 0:
                        check_array = ImageArray[HIGH - SEARCH_BOUNDARY:HIGH, x:x + SEARCH_BOUNDARY]
                    elif x + SEARCH_BOUNDARY > WIDTH:
                        check_array = ImageArray[HIGH - SEARCH_BOUNDARY:HIGH, x - SEARCH_BOUNDARY:x]
                    else:
                        check_array = ImageArray[HIGH - SEARCH_BOUNDARY:HIGH, x - SEARCH_BOUNDARY:x + SEARCH_BOUNDARY]
                    check_number = np.sum(check_array == 255)
                    # print(check_number)
                    #  判断数量
                    if check_number >= CHECK_BOUNDARY:
                        real_list.append(centralPos)
            case 'left':
                # 遍历
                for centralPos in check_list:
                    # 确定中心点
                    y = centralPos
                    # print(centralPos)
                    # 检查中心点 5*5 范围内255
                    if y - SEARCH_BOUNDARY < 0:
                        check_array = ImageArray[y:y + SEARCH_BOUNDARY, 0:SEARCH_BOUNDARY]
                    elif y + SEARCH_BOUNDARY > HIGH:
                        check_array = ImageArray[y - SEARCH_BOUNDARY:y, 0:SEARCH_BOUNDARY]
                    else:
                        check_array = ImageArray[y - SEARCH_BOUNDARY:y + SEARCH_BOUNDARY, 0:SEARCH_BOUNDARY]
                    check_number = np.sum(check_array == 255)
                    # print(check_number)
                    #  判断数量
                    if check_number >= CHECK_BOUNDARY:
                        real_list.append(centralPos)
            case 'right':
                # 遍历
                for centralPos in check_list:
                    # 确定中心点
                    y = centralPos
                    # print(centralPos)
                    # 检查中心点 5*5 范围内255
                    if y - SEARCH_BOUNDARY < 0:
                        check_array = ImageArray[y:y + SEARCH_BOUNDARY, WIDTH - SEARCH_BOUNDARY:WIDTH]
                    elif y + SEARCH_BOUNDARY > HIGH:
                        check_array = ImageArray[y - SEARCH_BOUNDARY:y, WIDTH - SEARCH_BOUNDARY:WIDTH]
                    else:
                        check_array = ImageArray[y - SEARCH_BOUNDARY:y + SEARCH_BOUNDARY, WIDTH - SEARCH_BOUNDARY:WIDTH]
                    check_number = np.sum(check_array == 255)
                    # print(check_number)
                    #  判断数量
                    if check_number >= CHECK_BOUNDARY:
                        real_list.append(centralPos)
        # 判断是否为空
        if real_list:
            # 去重
            result.append(real_list[0])
            # 对于每个元素，我们都检查它是否大于结果列表中最后一个元素加上 LIST_REMOVE
            for i in range(1, len(real_list)):
                if real_list[i] > result[-1] + LIST_REMOVE:
                    result.append(real_list[i])
            return result
        else:
            return result

    # 图像的上下两边界
    up_list: list = ImageArray[0].tolist()
    down_list: list = ImageArray[-1].tolist()
    # 图像的左右两边界
    left_list: list = [ImageArray[i][0] for i in range(HIGH)]
    right_list: list = [ImageArray[i][-1] for i in range(HIGH)]
    # 查找上下边界255 数组长度1280
    up_index = [i for i in range(WIDTH) if up_list[i] == 255]
    down_index = [i for i in range(WIDTH) if down_list[i] == 255]
    # 查找左右边界255 数组长度720
    left_index = [i for i in range(HIGH) if left_list[i] == 255]
    right_index = [i for i in range(HIGH) if right_list[i] == 255]
    # 匹配照片模式
    match PhotoType:
        case 'up down':
            # 以此点为中心5*5单元格搜索
            up = searchingCell(up_index, 'up')
            down = searchingCell(down_index, 'down')
            # 坐标
            pos = [[(i, 0), (j, -HIGH)] for i, j in zip(up, down)]
            return pos
        case 'left right':
            # 以此点为中心5*5单元格搜索
            left = searchingCell(left_index, 'left')
            right = searchingCell(right_index, 'right')
            # 坐标
            pos = [[(0, -i), (WIDTH, -j)] for i, j in zip(left, right)]
            return pos
        case 'right down':
            # 左上 -> 右下
            # 以此点为中心5*5单元格搜索
            up = searchingCell(up_index, 'up')
            down = searchingCell(down_index, 'down')
            left = searchingCell(left_index, 'left')
            right = searchingCell(right_index, 'right')
            # 坐标
            # 翻转为正确顺序
            # up = up[::-1]
            # down = down[::-1]
            # 取坐标
            up = [(i, 0) for i in up]
            down = [(i, -HIGH) for i in down]
            left = [(0, -i) for i in left]
            right = [(WIDTH, -i) for i in right]
            # 连接
            left_up = left + up
            down_right = down + right
            pos = [[i, j] for i, j in zip(left_up, down_right)]
            return pos
        case 'left down':
            # 上右 -> 左下
            # 以此点为中心5*5单元格搜索
            up = searchingCell(up_index, 'up')
            down = searchingCell(down_index, 'down')
            left = searchingCell(left_index, 'left')
            right = searchingCell(right_index, 'right')
            # 坐标
            # 取坐标
            up = [(i, 0) for i in up]
            down = [(i, -HIGH) for i in down]
            left = [(0, -i) for i in left]
            right = [(WIDTH, -i) for i in right]
            # 连接
            up_right = up + right
            left_down = left + down
            pos = [[i, j] for i, j in zip(up_right, left_down)]
            return pos
