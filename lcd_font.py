from PIL import Image, ImageDraw, ImageFont
import PIL.features

# brew install libraqm
assert PIL.features.check('raqm'), "libraqm required"

HEIGHT = 64
WIDTH = 32
# 画布大小
size = (320, HEIGHT)

# 黑白格式
FORMAT = '1'
BG = 0
FG = 1

# Y offset, 多数字体有自带行间距，可以用此参数消除行间距
YOFF = 2  # or -1


# CHARS = "晴天卧槽可以了！你好世界最怕你一生碌碌无为，还安慰自己平凡可贵。雾霾"

CHARS = ''
# 读入待转换的字符
with open('char.txt', 'r', encoding='utf-8') as f:
    CHARS = f.read()

# 为chars去重
CHARS = sorted(set(CHARS))
# CHARS = ''.join(list(set(CHARS)))

im = Image.new(FORMAT, size, BG)

font = ImageFont.truetype(
    "./fonts/DigitalDisplay.ttf", size=89, index=0)

draw = ImageDraw.Draw(im)

# 代码段用于检查字体渲染
draw.text((0, YOFF), "12:23", font=font, fill=FG, language='zh-CN')
# im.save('font.png')
im.show()

draw.rectangle([(0, 0), size], fill=BG)

content = ''
for i, c in enumerate(CHARS):
    charmap = []
    draw.text((0, YOFF), c, font=font, fill=FG)
    # width = WIDTH//2 if ord(c) < 0x80 else WIDTH
    width = WIDTH

    for y in range(HEIGHT):
        v = 0
        for x in range(width):
            b = im.getpixel((x, y))
            v = (v << 1) + b
            # 当凑足8个bit时，写入charmap
            if x % 8 == 7:
                charmap.append(v)
                v = 0
        # 当凑不足8个bit时，补足位移,写入charmap
        if width % 8 != 0:
            charmap.append(v << (8 - width % 8))

    draw.rectangle([(0, 0), size], fill=BG)
    content += '{'
    # print("{", end='')
    c = c.replace('\\', '\\\\').replace('\"', '\\\"')
    content += '"{}", {{ {} }}, '.format(c, ', '.join(
        map(lambda c: "0x%02x" % c, charmap)))
    # print('"{}", {}'.format(c, ', '.join(
    #     map(lambda c: "0x%02x" % c, charmap))), end="")
    content += '},\n'
    # print("},")

print(content)
content = """
#include "fonts.h"

const CH_CN Font_Table[] =
{
""" + content + """
};

cFONT FontLCD = {
  Font_Table,
  sizeof(Font_Table) / sizeof(CH_CN),  /*size of table*/
  """+str(WIDTH)+""", /* ASCII Width */
  """+str(WIDTH)+""", /* Width */
  """+str(HEIGHT)+""", /* Height */
};

"""
with open('ch_font.c', 'w', encoding='utf-8') as f:
    f.write(content)
