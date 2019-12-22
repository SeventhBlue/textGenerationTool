# #!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time:       2019/12/22 12:48
# @Author:     weiz
# @File:       otherFn.py
# @Description:
import os
import sys
from tkinter import _flatten

def readTXT(path):
    """
    读取txt文件
    :param path:
    :return:
    """
    # 按行读取
    with open(path, "r+", encoding='utf-8') as f:
        wordLib = f.readlines()

    # 去掉换行符
    for index in range(len(wordLib)):
        wordLib[index] = wordLib[index].strip('\n')

    return wordLib


def checkDuplicates(libPath):
    """
    检查字库是否有重复
    :param libPath:
    :return:
    """
    wordLib = readTXT(libPath)
    wordSet = set(wordLib)

    if len(wordLib) != len(wordSet):
        repeatTimes = 0
        repeatChar = []
        wordLib_sort = sorted(wordLib)
        wordSet_sort = sorted(wordSet)
        for i in range(len(wordSet_sort)):
            if wordSet_sort[i] != wordLib_sort[i + repeatTimes]:
                repeatChar.append(wordLib_sort[i + repeatTimes])
                repeatTimes += 1
        print("There are {} repeated characters in the font:{}".format(len(wordLib) - len(wordSet), repeatChar))
        sys.exit()
    else:
        print("The total number of characters in the font:{}".format(len(wordLib)))
        return wordLib


def detectingTextCoverage(textPath=None, wlPath=None):
    """
    检测文本中的字符的覆盖面
    :param textPath:
    :return:
    """
    if textPath == None:
        textPath = "./data/corpus"
    if wlPath == None:
        wlPath = chn_lib_path

    wl = readTXT(wlPath)
    wl_set = set(wl)
    textName = os.listdir(textPath)
    text_all = []
    for name in textName:
        path_name = os.path.join(textPath, name)
        text_all.append(readTXT(path_name))

    text_all = list(_flatten(text_all))  # 多维转一维
    chars = []
    for string in text_all:
        for char in set(string):
            chars.append(char)
    chars_set = set(chars)
    print("字库中字符总数:{}".format(len(wl_set)))
    print("字库中不存在的字符:{}".format(''.join(sorted(chars_set - wl_set))))
    print("文章中不存在的字符:{}".format(''.join(sorted(wl_set - chars_set))))
    characteRcoverage = len(chars_set - (wl_set - chars_set)) / len(wl_set)
    print("字符覆盖率:{:.2f}%".format(characteRcoverage * 100))



chn_lib_path = "./data/chars/chn.txt"         # 字库的路径

if __name__ == "__main__":
    wordLib = checkDuplicates(chn_lib_path)
    detectingTextCoverage()
