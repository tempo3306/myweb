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

FLAG = 1  # 标记
CHARSET = ""  # 符号源
IMG_SIZE1 = (113, 33)  # 图片大小
IMG_SIZE2 = (113, 50)  # 图片大小
POS1 = (10, 6)
POS2 = (10, 6)
FONT_SIZE = 24  # 字体大小
FONT_TYPE = 'Calibri.ttf'  # 字体类型
BG_COLOR = (255, 255, 255)  # 背景颜色
FG_COLOR = (0, 0, 255)  # 字体颜色
RED_COLOR = (255, 0, 0)  # 字体颜色
GREEN_COLOR = (0, 255, 0)  # 字体颜色
BLUE_COLOR = (0, 0, 255)  # 字体颜色
D_COLOR = (0, 0, 0)  # 干扰颜色
DIR = './'  # 保存路径
LENGTH = 5  # 验证码的字符数
LNUM = 10  # 干扰线条数
PNUM = 100  # 干扰点数
PROBA = 2  # 随机概率因子


# pic = Image.new('RGB', IMG_SIZE, BG_COLOR)  # 图片
# draw = ImageDraw.Draw(pic)  # 画笔

class Create_pic():
    num = 1

    def get_redpic(self):
        numstr = get_randnum()
        pic = draw(charset=numstr, fg_color=RED_COLOR)
        pic = transform(pic)
        pic = rectangle(pic)
        pic = circle(pic)
        pic = bottom_circle(pic)
        pic = addpoint(pic)
        pic = addline(pic)
        save(pic, self.num)
        self.num += 1

    def get_greenpic(self):
        pass


    def get_bluepic(self):
        pass


# 生成随机数字
def get_randnum(num=6):
    chars = string.digits
    random = Random()
    randnum = ''
    for i in range(num):
        randnum += chars[random.randint(0, 9)]
    print(randnum)
    return randnum

def get_randcolor():
    r= random.randint(0, 255)
    g= random.randint(0, 255)
    b= random.randint(0, 255)
    return (r, g, b)


def get_randstr(num=2):
    chars = string.ascii_letters
    random = Random()
    randstr = ''
    for i in range(num):
        randstr += chars[random.randint(0, 9)]
    print(randstr)
    return randstr



def draw(charset='2011', size=IMG_SIZE1, fg_color=FG_COLOR, pos=POS1):
    """
    画画
    """
    pic = Image.new('RGB', size, BG_COLOR)  # 图片
    draw = ImageDraw.Draw(pic)
    charset = charset[0] + "".join([' ' + charset[x] for x in range(1, len(charset))])
    hold = ImageFont.truetype(FONT_TYPE, FONT_SIZE)
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
    img = cv2.rectangle(img, (int(0), int(0)), (int(width - 1), int(height - 1)), RED_COLOR, 1)
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

def save(pic, name):
    """
    保存中间结果
    """
    pic.save(DIR + '%s.png' % name)
    pic.show()


if __name__ == '__main__':
    C = Create_pic()
    C.get_redpic()