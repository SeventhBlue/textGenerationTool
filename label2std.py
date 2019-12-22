# -*- coding: utf-8 -*-#
# Author:      weiz
# Date:        2019/12/6 下午4:25
# Name:        label2std.py
# Description: 1.改变label的格式；2.改变label和图片的名字；
import os
import numpy as np
import sys
import cv2
import shutil

def readTXT(path):
    """
    读取txt文件
    :param path:
    :return:
    """
    # 按行读取预料库的中文
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


def delOldFile(stdName, statisName):
    """
    删除旧的文件，以防混乱
    :param stdName:
    :param statisName:
    :return:
    """
    if os.path.exists(stdName):
        os.remove(stdName)                        # 删除原来的label_std，以防混乱
        print("Old {} deleted!".format(stdName))
    if os.path.exists(statisName):
        os.remove(statisName)                   # 删除原来的统计信息，以防混乱
        print("Old {} deleted!".format(statisName))


def saveStatisInfo(stdLib, statInfo, statisName):
    """
    保存统计信息（统计每个字符的个数）
    :param stdLib: 字库的列表
    :param statInfo: 统计的信息
    :param statisName: 保存统计信息文件的名字
    :return:
    """
    # 保存这次生成的字符统计信息
    statInfo_file = open(statisName, mode='a', encoding='utf-8')
    for i in range(len(stdLib)):
        c_s_i = str(i) + ':' + stdLib[i] + ' ' + str(statInfo[i])  # 保存的数据格式是:字符在字典的索引:字符 个数
        statInfo_file.write(c_s_i + '\n')
    statInfo_file.close()


def findSpecifySuffix(path, ret, suffix):
    """
    Finding specified suffix file in specify path
    :param path:
    :param ret:
    :param suffix:
    :return:
    """
    filelist = os.listdir(path)
    for filename in filelist:
        de_path = os.path.join(path, filename)
        if os.path.isfile(de_path):
            if de_path.endswith(suffix):  # Specify to find the txt file. eg:.jpg
                ret.append(de_path)
        else:
            findSpecifySuffix(de_path, ret, suffix)

def changeImageName(imgFile, changeImgFile):
    """
    改变生成图片的名字（一般生成的是训练数据时用）
    :param imgFile:
    :param changeImgFile:
    :return:
    """
    if os.path.exists(changeImgFile):
        shutil.rmtree(changeImgFile)
        print("Old {} deleted!".format(changeImgFile))
    os.mkdir(changeImgFile)
    ret = []
    findSpecifySuffix(imgFile, ret, ".jpg")
    for imagePath in ret:
        img = cv2.imread(imagePath)
        (filepath, tempfilename) = os.path.split(imagePath)
        # (filename, extension) = os.path.splitext(tempfilename)
        tempfilename = addChar + tempfilename
        newPath = os.path.join(changeImgFile, tempfilename)
        cv2.imwrite(newPath, img)


def label2std(charLib, label, stdLabelName, imgFile, changeImgFile, isChangeName=False):
    """
    把label文件的格式从 [00000002 0077B-3-1=] 生成 [00000002.jpg 0 0 7 7 37 91 3 91 1 89] 格式
    :param charLib:
    :param label:
    :param stdLabelName:
    :param imgFile:
    :param changeImgFile:
    :param isChangeName: 改变生成图片的名字，一般生成验证集数据时用
    :return:
    """
    statInfo = np.zeros(len(charLib), dtype=np.int32)  # 统计这次生成的数据每个字符的个数变量

    writeLine = []
    degree_of_completion = 0
    progressBarTarget = len(label)
    for charLine in label:
        imageName, chn = charLine.split(' ', 1)
        if isChangeName:
            tmp = addChar + imageName + ".jpg"
        else:
            tmp = imageName + ".jpg"
        for char in chn:
            limit = 0
            for index in range(len(charLib)):
                if char == charLib[index]:
                    tmp = tmp + ' ' + str(index)
                    statInfo[index] += 1
                    break
                else:
                    limit += 1
            if limit == len(charLib):
                print("The '{}' character does not exist in the font.".format(char))
                sys.exit()

        writeLine.append(tmp)
        tmp = ''
        if len(writeLine) == 1000:  # 积累到一定数量就保存label_std
            label_file = open(stdLabelName, mode='a')
            for Line in writeLine:
                label_file.write(Line + '\n')
            label_file.close()
            writeLine.clear()
            degree_of_completion = degree_of_completion + 1000
            done = int(50 * degree_of_completion / progressBarTarget)
            sys.stdout.write(
                "\r[%s%s] %d%%" % ('█' * done, ' ' * (50 - done), 100 / progressBarTarget * degree_of_completion))
            sys.stdout.flush()

    # 防止某些label_std没有保存
    if len(writeLine) > 0:
        label_file = open(stdLabelName, mode='a')
        for Line in writeLine:
            label_file.write(Line + '\n')
        label_file.close()
        writeLine.clear()
        print("Degree of completion:{}%".format(100))
        print("save!!!")

    if isChangeName:
        changeImageName(imgFile, changeImgFile)

    return statInfo


chn_lib_path = "./data/chars/chn.txt"         # 字库的路径
labelPath = "./output/images/tmp_labels.txt"     # 需要更改的label
label_std = "./output/label_std.txt"             # 生成的标准label
charStatisInfo = './output/charStatisInfo.txt'   # 每次字符的生成数量的统计信息

imagesFile = "./output/images"
changeImagesFile = "./output/changeImages"       # 图片改变名字后存放的路径
addChar = "t"                                    # 改变名字时添加的字符

if __name__ == "__main__":
    delOldFile(label_std, charStatisInfo)
    wordLib = checkDuplicates(chn_lib_path)

    label_tmp = readTXT(labelPath)

    statInfo = label2std(wordLib, label_tmp, label_std, imagesFile, changeImagesFile)

    saveStatisInfo(wordLib, statInfo, charStatisInfo)