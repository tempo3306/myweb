'''
1.圆圈 不同颜色圆圈
2.颜色数字
3.颜色六边形
4.脚下有圆圈

'''

from random import Random  # 用于生成随机码
import random
import string
from io import StringIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cv2
import numpy as np
import pickle



FLAG = 1  # 标记
CHARSET = ""  # 符号源
IMG_SIZE1 = (113, 33)  # 图片大小
IMG_SIZE2 = (113, 50)  # 图片大小
POS1 = (6, 3)
POS2 = (6, 3)
SINGLE_SIZE = 32  # 字体大小
FONT_TYPE = 'Calibri.ttf'  # 字体类型
BG_COLOR = (255, 255, 255)  # 背景颜色
FG_COLOR = (0, 0, 255)  # 字体颜色
RED_COLOR = (255, 0, 0)  # 字体颜色
GREEN_COLOR = (0, 255, 0)  # 字体颜色
BLUE_COLOR = (0, 0, 255)  # 字体颜色
COLOR_LIST = ['red', 'green', 'blue']
COLOR_QUESTION = {
    'red': 0,
    'green': 1,
    'blue': 2
}
COLOR_KEY = {'red': RED_COLOR, 'green': GREEN_COLOR, 'blue': BLUE_COLOR}
D_COLOR = (0, 0, 0)  # 干扰颜色
DIR = './'  # 保存路径
LENGTH = 5  # 验证码的字符数
LNUM = 10  # 干扰线条数
PNUM = 100  # 干扰点数
PROBA = 2  # 随机概率因子

QUESIONS = {
    0: ['请输入红色数字的校验码', ''],
    1: ['请输入绿色数字的校验码', ''],
    2: ['请输入蓝色数字的校验码', ''],
    3: ['请输入第1到第4位图像校验码', (0, 4)],
    4: ['请输入第2到第5位图像校验码', (1, 5)],
    5: ['请输入第3到第6位图像校验码', (2, 6)],
    6: ['请输入第1到第3位图像校验码', (0, 3)],
    7: ['请输入第2到第4位图像校验码', (1, 4)],
    8: ['请输入第3到第5位图像校验码', (2, 5)],
    9: ['请输入第4到第6位图像校验码', (3, 6)]
}


# '请输入红色圆形后3位数字校验码',


# ownpic = Image.new('RGB', IMG_SIZE, BG_COLOR)  # 图片
# draw = ImageDraw.Draw(ownpic)  # 画笔

class Create_pic():
    def get_colorpic(self):
        qa_name = []
        for i in range(1, 301):
            colors, qa = get_num_color()
            pic = color_draw(colors)
            # ownpic = draw(charset=numstr, fg_color=RED_COLOR)
            # ownpic = transform(ownpic)
            pic = rectangle(pic)
            # ownpic = circle(ownpic)
            # ownpic = bottom_circle(ownpic)
            pic = addpoint(pic)
            pic = addline(pic)
            name = save(pic, i)
            qa_name.append((name, qa))
        print(qa_name)
        print(len(qa_name))
        with open('color0_300.pkl', 'wb') as cofile:
            pickle.dump(qa_name, cofile)



# 生成随机数字
def get_randnum(num=6):
    chars = string.digits
    random = Random()
    randnum = ''
    for i in range(num):
        randnum += chars[random.randint(0, 9)]
    return randnum


##生成颜色次序   某一种颜色3或4个
def get_colors(num=6):
    # 主色
    main_color, secondary_color = random.sample(COLOR_LIST, 2)
    # choose 3 4
    main_num = random.randint(3, 4)
    # pos 0, 1, 2
    pos = random.randint(0, 2)
    secondary_num = num - main_num
    templist = [0] * num
    for i in range(pos, pos + main_num):
        templist[i] = 1
    colorlist = []
    for i in range(num):
        if templist[i]:
            colorlist.append(main_color)
        else:
            colorlist.append(secondary_color)
    return (colorlist, [main_color, main_num, pos])


##组合数字和颜色
def get_num_color():
    randnum = get_randnum()
    colorlist, info = get_colors()
    qa = get_q_a_a(randnum, info)
    return (list(zip(randnum, colorlist)), qa)  # zip只能迭代一次


def get_q_a_a(charset, info):
    # 从0到10依次计算答案  0,1,2 由主色决定
    q_a_a = []
    # info = [main_color, main_num, pos]  #主色，数量， 位置
    main_color, main_num, pos = info
    # 主色问题1
    question1 = QUESIONS[COLOR_QUESTION[main_color]][0]
    answer1 = charset[pos: pos + main_num]
    q_a_a.append((question1, answer1))
    # 3-10 次序数字
    for i in range(3, 10):
        question = QUESIONS[i][0]
        x, y = QUESIONS[i][1]
        answer = charset[x: y]
        q_a_a.append((question, answer))
    return q_a_a


# 生成随机颜色
def get_randcolor():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)


def get_randstr(num=2):
    chars = string.ascii_letters
    random = Random()
    randstr = ''
    for i in range(num):
        randstr += chars[random.randint(0, 9)]
    return randstr


def color_draw(colors, size=IMG_SIZE1):
    pic = Image.new('RGB', size, BG_COLOR)  # 图片
    draw = ImageDraw.Draw(pic)
    hold = ImageFont.truetype(FONT_TYPE, SINGLE_SIZE)
    x, y = POS1
    index = 0
    # print('f', list(colors))
    colors = list(colors)
    for char, color in colors:
        draw.text((x + 16 * index, y), char, font=hold, fill=COLOR_KEY[color])
        index += 1
    return pic


def draw(charset='2011', size=IMG_SIZE1, fg_color=FG_COLOR, pos=POS1):
    """
    画画
    """
    pic = Image.new('RGB', size, BG_COLOR)  # 图片
    draw = ImageDraw.Draw(pic)
    # charset = charset[0] + "".join(['' + charset[x] for x in range(1, len(charset))])
    hold = ImageFont.truetype(FONT_TYPE, SINGLE_SIZE)
    draw.text(pos, charset, font=hold, fill=fg_color)  # FG_COLOR  字体颜色
    return pic


def transform(pic, size=IMG_SIZE1):
    """
    变换,还不太明白这个变换
    """
    draw = ImageDraw.Draw(pic)  # 画笔
    params = [1 - float(random.randint(1, 2)) / 100, 0, 0, 0, 1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500, 0.001, float(random.randint(1, 2)) / 500]
    pic = pic.transform(size, Image.PERSPECTIVE, params)
    draw = ImageDraw.Draw(pic)
    return pic


def addpoint(pic, size=IMG_SIZE1):
    """
    增加干扰点
    """
    draw = ImageDraw.Draw(pic)  # 画笔
    width, height = size
    for i in range(width):
        for j in range(height):
            tmp = random.randint(0, 100)
            if (tmp <= PROBA):
                draw.point((i, j), get_randcolor())
    return pic


def addline(pic, size=IMG_SIZE1):
    """
    增加干扰线
    """
    draw = ImageDraw.Draw(pic)  # 画笔
    width, height = size
    for i in range(LNUM):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line(((x1, y1), (x2, y2)), get_randcolor())
    return pic


def flush(pic):
    """
    打磨润色
    """
    pic = pic.filter(ImageFilter.EDGE_ENHANCE_MORE)
    pic = pic.filter(ImageFilter.SMOOTH)
    return pic


##加边框
def rectangle(pic, size=IMG_SIZE1):
    img = np.asarray(pic)
    width, height = size
    color = random.sample(COLOR_LIST, 1)[0]
    img = cv2.rectangle(img, (int(0), int(0)), (int(width - 1), int(height - 1)), COLOR_KEY[color], 1)
    # cv2.rectangle(img, (20, 20), (100, 100), (55, 255, 155), 5)
    return Image.fromarray(np.uint8(img))


##给数字加圆
def circle(pic, size=IMG_SIZE1):
    img = np.asarray(pic)
    width, height = size
    x, y = POS1
    for i in range(6):
        cv2.ellipse(img, (x + 5 + 17 * i, y + 10), (7, 10), 0, 0, 360, BLUE_COLOR, 0)
        # img = cv2.circle(img, (x + 12 * i, y + 10), 10, BLUE_COLOR, 1)  # 修改最后一个参数
    return Image.fromarray(np.uint8(img))


def bottom_circle(pic, size=IMG_SIZE1):
    img = np.asarray(pic)
    width, height = size
    x, y = POS1
    for i in range(6):
        img = cv2.circle(img, (x + 6 + 17 * i, y + 23), 2, BLUE_COLOR, 1)  # 修改最后一个参数
    return Image.fromarray(np.uint8(img))


def save(pic, num, show=False):
    """
    保存中间结果
    """
    name = 'own%s.png' %num
    pic.save(DIR + 'ownpic/own%s.png' % num)
    if show:
        pic.show()
    return name

if __name__ == '__main__':
    # print(get_colors())

    C = Create_pic()
    C.get_colorpic()
