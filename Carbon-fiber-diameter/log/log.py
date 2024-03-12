"""
日志监控
"""
from functools import wraps
from datetime import datetime


def log(func):
    """
    日志
    """

    @wraps(func)
    def logging(*args, **kwargs):
        print(f'【日志】|{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}->函数{func.__name__}执行')
        return func(*args, **kwargs)

    return logging
