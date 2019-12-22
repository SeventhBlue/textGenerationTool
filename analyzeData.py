# -*- coding: utf-8 -*-#
# Author:      weiz
# Date:        2019/12/11 下午4:31
# Name:        analyzeData.py
# Description: 分析数据集，包括字符数最多、最小，平均数，标准差等
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font = FontProperties(fname="./data/fonts/chn/simhei.ttf", size=15)
font1 = FontProperties(fname="./data/fonts/chn/simhei.ttf", size=10)

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


def statisticalData(label, wordLib):
    """
    统计数据的个数
    :param label:数据格式是：20455828_2605100732.jpg 263 82 29 56 35 435 890 293 126 129
    :param wordLib:字库
    :return:
    """
    statInfo = np.zeros(len(wordLib), dtype=np.int32)
    for row in label:
        imgName, index = row.split(' ', 1)
        indexList = index.split()
        for i in indexList:
            statInfo[int(i)] += 1
    return statInfo


def autolabel(ax, rects, xpos='center'):
    """
    在柱状图上显示数量
    :param ax:
    :param rects:
    :param xpos:
    :return:
    """
    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() * offset[xpos], 1.01 * height,
                '{}'.format(height), ha=ha[xpos], va='bottom')


def drawbar(arr, xlab, isSave, title=None):
    """
    柱状图显示字符的数量
    :param arr:
    :param xlab:
    :param title:
    :return:
    """
    if title == None:
        title = "字符数量按区间分布情况"
    ind = np.arange(len(arr))  # the x locations for the groups
    width = 0.5  # the width of the bars

    total_num = 0
    for val in arr:
        total_num += val
    bar_label = "Total number of character categories:" + str(total_num)

    plt.ion()
    fig, ax = plt.subplots(figsize=(12, 8))
    rects1 = ax.bar(ind, arr, width, color='SkyBlue', label=bar_label)


    ax.set_ylabel("num", fontproperties=font)
    ax.set_title(label=title, fontproperties=font)
    ax.set_xticks(ind)
    ax.set_xticklabels(xlab, rotation=45, fontproperties=font)
    ax.legend()

    autolabel(ax, rects1)
    plt.ioff()
    plt.show()
    if isSave:
        saveName = title + ".png"
        plt.savefig(saveName)


def analyzeData(statInfo, num_intervals=None, isSave=None):
    """
    按区间整体性显示分布信息
    :param statInfo:传入的值是每个字符的数量，格式是列表：[123,456,789]
    :param num_intervals: 区间个数，默认18个区间
    :param isSave:
    :return:
    """
    if num_intervals == None:
        num_intervals = 18
    if isSave == None:
        isSave = False
    xlabel = []   # x轴的标签
    max_statInfo = max(statInfo)  # 字符出现最多的个数
    intervals = max_statInfo // num_intervals
    dict_in_intervals_num = {}   # 字典的格式：{0:[low, up, num]}，分别代表区间的索引，区间下限，区间上限，落在这个区间字符的数量
    for i in range(num_intervals):  # 统计落在不同区间字符的种类数
        if i == 0:   # 如果是开始区间[0, intervals]
            low = i * intervals
            up = (i+1) * intervals
        elif i == (num_intervals - 1):  # 如果是最后一个区间[low， max_statInfo]
            low = i * intervals + 1
            up = max_statInfo
        else:                    # 其他区间
            low = i * intervals + 1
            up = (i+1) * intervals
        string = str(low) + '-' + str(up)
        xlabel.append(string)
        dict_in_intervals_num[i] = [low, up, 0]
    for num in statInfo:      # 统计每个区间的个数
        for val in dict_in_intervals_num.values():
            if val[0] <= num <= val[1]:
                val[2] += 1
    val_num = []   # 从字典中提取出每个区间的个数，与xlabel对应
    for val in dict_in_intervals_num.values():
        val_num.append(val[2])

    drawbar(val_num, xlabel, isSave)


def displayCharNum(statInfo, low=None, up=None):
    """
    详细的显示[low,up]中字符数量分布及统计信息
    :param statInfo:传入的值是每个字符的数量，格式是列表：[123,456,789]
    :param wordLib:
    :return:
    """
    if low == None:
        low = 0
    if up == None:
        up = len(statInfo)
    if len(statInfo[low:up]) == 0:
        print("Index settings are incorrect")
        sys.exit()
    x_values = range(len(statInfo[low:up]))
    y_values = statInfo[low:up]
    char_0_num = 0     # 统计字符数量为0的个数
    for d in y_values:
        if d == 0:
            char_0_num += 1
    plt.figure(figsize=(12, 8))
    plt.scatter(x_values, y_values, s=1)
    plt.scatter(0, 0, s=5)   # 不参与计算。只是为了显示原点，让text文本正常显示

    note0 = "当前统计总数/总字符总数:{:.2f}%".format(sum(y_values)/sum(statInfo)*100)
    note1 = "当前统计的字符数的最大值:{}".format(max(y_values))
    note2 = "当前统计字符数为 0的个数:{}".format(char_0_num)
    note3 = "当前统计的字符数的平均值:{}".format(int(np.mean(y_values)))
    note4 = "当前统计的字符数的标准差:{}".format(int(np.std(y_values)))
    note5 = "当前统计的字符数的最小值:{}".format(min(y_values))

    x = (up-low) - (up-low) // 4
    space = max(y_values) // 70
    y = max(y_values)
    plt.text(x, (y - space * 0), note0, fontproperties=font1)  # 左下角是原点;像素坐标需要坐标轴最大的值来确定
    plt.text(x, (y - space * 2), note1, fontproperties=font1)  # 左下角是原点;像素坐标需要坐标轴最大的值来确定
    plt.text(x, (y - space * 4), note2, fontproperties=font1)
    plt.text(x, (y - space * 6), note3, fontproperties=font1)
    plt.text(x, (y - space * 8), note4, fontproperties=font1)
    plt.text(x, (y - space * 10), note5, fontproperties=font1)

    # 设置图表标题， 并给坐标轴加上标签
    title = "其中{}个字符数量分布(字符总数是：{})".format(len(y_values), len(statInfo))
    plt.title(title, fontproperties=font)
    plt.xlabel("字符的类别", fontproperties=font)
    plt.ylabel("数量", fontproperties=font)
    # 设置刻度标记的大小
    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.show()

    analyzeData(y_values)



def saveStatisInfo(statInfo, statisName):
    """
    保存统计信息（统计每个字符的个数）
    :param statInfo: 统计的信息
    :param statisName: 保存统计信息文件的名字
    :return:
    """
    if os.path.exists(statisName):
        os.remove(statisName)  # 删除原来的统计信息，以防混乱
        print("Old {} deleted!".format(statisName))
    # 保存这次生成的字符统计信息
    statInfo_file = open(statisName, mode='a', encoding='utf-8')
    for i in range(len(statInfo)):
        c_s_i = str(statInfo[i])
        statInfo_file.write(c_s_i + '\n')
    statInfo_file.close()


def readStatInfo(path):
    """
    读取统计信息
    :param path:文件里的数据格式是每行存一个数
    :return:
    """
    statInfo = readTXT(path)
    for i, num_str in enumerate(statInfo):
        statInfo[i] = int(num_str)
    return statInfo



labelPath = "./output/label_std.txt"          # 生成的标准label
chn_lib_path = "./data/chars/chn.txt"         # 字库的路径
if __name__ == "__main__":
    label = readTXT(labelPath)
    wordLib = readTXT(chn_lib_path)
    statInfo = statisticalData(label, wordLib)
    saveStatisInfo(statInfo, "statInfo_tmp.txt")

    #statInfo = readStatInfo("statInfo_tmp.txt")   # 保存statInfo_tmp.txt文件后可以注释上面代码，可使用这行代码让运行速度变快
    analyzeData(statInfo)
    displayCharNum(statInfo, 0, 1500)