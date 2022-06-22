from importlib import reload
from types import ModuleType
from typing import *
from os import system


def pycls() -> None:
    """效果等同于windows终端的cls命令，可以清空当前终端所显示的内容（实质上是将终端内容移到上方直到超出屏幕显示范围）"""
    system('cls')
    return None


def rl(userModule: ModuleType) -> ModuleType:
    """重载用户的包"""
    return reload(userModule)
