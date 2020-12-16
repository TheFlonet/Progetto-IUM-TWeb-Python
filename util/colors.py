from random import random


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def colors(color_num):
    """
    :param color_num: how many color the function has to create
    :return: a list of color in rgb format
    """
    ret = []
    step = 256 / color_num
    for i in range(color_num):
        r = int(random() * 256 + step) % 256
        g = int(random() * 256 + step) % 256
        b = int(random() * 256 + step) % 256
        ret.append('#%02x%02x%02x' % (r, g, b))
    return ret
