"""
绘图
"""
import cv2
import matplotlib.pyplot as plt
import numpy

from log.log import log
import threading


@log
def drawBitumen(pos: list[list[tuple[int, int], tuple[int, int]]], imgPath: str) -> None:
    """
    画出沥青丝
    :param pos: 坐标点位置
    :param imgPath: 图片路径
    :return: None
    """
    # 设置路径
    tmp = imgPath.split(".")[0] + 'draw.jpg'
    # 设置标题
    # 关闭交互
    plt.ioff()
    # 每个坐标进行画图
    for pos_list in pos:
        pos_x = [pos_tuple[0] for pos_tuple in pos_list]
        pos_y = [pos_tuple[1] for pos_tuple in pos_list]
        plt.plot(pos_x, pos_y, color='black')
    # 限制坐标轴
    plt.xlim(0, 1280)
    plt.ylim(0, -720)
    # 反转Y坐标轴
    plt.gca().invert_yaxis()
    # 上移x轴坐标
    plt.gca().xaxis.set_ticks_position('top')
    # 保存图片
    plt.savefig("./result/" + tmp.split('/')[-1])
    plt.close()
    # print(imgName)
    # 展示
    tmp = tmp.encode('gbk').decode()
    image = cv2.imread(tmp)
    t = threading.Thread(target=showImage, args=(tmp, image,))
    t.start()


def showImage(tmp, image: numpy.ndarray):
    cv2.imshow(tmp, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
