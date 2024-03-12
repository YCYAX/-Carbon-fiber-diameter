"""
图片处理
"""
import cv2
import numpy
from log.log import log


@log
def imagePreprocessing(ImagePath: str) -> numpy.ndarray:
    """
    图像预处理
    :param ImagePath: 照片路径
    :return: 照片的数组形式 numpy.ndarray
    """
    # 原图像
    origin_image = cv2.imread(ImagePath)
    image = cv2.resize(origin_image, (1280, 720))
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 图像锐化 加强边界
    # sharpen_op = numpy.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=numpy.float32)
    # sharpen_op = numpy.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]], dtype=numpy.float32)
    # sharpen_image = cv2.filter2D(gray_image, -1, sharpen_op)
    # sharpen_image = cv2.convertScaleAbs(sharpen_image)
    # 边缘检测 threshold1 控制细节, threshold2 控制明显轮廓
    canny_image = cv2.Canny(gray_image, threshold1=100, threshold2=150)
    # debug
    # cv2.imshow("123",canny_image)
    # cv2.waitKey(0)
    return canny_image
