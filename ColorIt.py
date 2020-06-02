import os
import sys


class colors:
    RED = (255, 0, 66)
    ORANGE = (245, 170, 66)
    YELLOW = (245, 252, 71)
    GREEN = (92, 252, 71)
    BLUE = (71, 177, 252)
    PURPLE = (189, 71, 252)
    WHITE = (255, 255, 255)


def initColorIt():
    if sys.platform.startswith('win32'):
        os.system("cls")
    elif sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
        os.system("clear")


def color(text, rgb):
    return "\033[38;2;{};{};{}m{}\033[0m".format(str(rgb[0]), str(rgb[1]), str(rgb[2]), text)


def background(text, rgb):
    return "\033[48;2;{};{};{}m{}\033[0m".format(str(rgb[0]), str(rgb[1]), str(rgb[2]), text)
