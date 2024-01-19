from PIL import Image, ImageDraw, ImageFont
import PIL.features

# brew install libraqm
assert PIL.features.check('raqm'), "libraqm required"

# 画布大小
size = (320, 18)

# 黑白格式
FORMAT = '1'
BG = 0
FG = 1

# Y offset, 多数字体有自带行间距，可以用此参数消除行间距
YOFF = 0  # or -1


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
    "./fonts/wqy-unibit.bdf", size=16, index=0)


draw = ImageDraw.Draw(im)

# 代码段用于检查字体渲染
# draw.text((0, YOFF), "Friday是我的谎言", font=font, fill=FG, language='zh-CN')
# im.save('font.png')
# im.show()

draw.rectangle([(0, 0), size], fill=BG)

content = ''
for i, c in enumerate(CHARS):
    charmap = []
    draw.text((0, YOFF), c, font=font, fill=FG)

    for y in range(17):
        v = 0
        if ord(c) < 0x80:
            for x in range(0, 8):
                b = im.getpixel((x, y))
                v = (v << 1) + b
            charmap.append(v)
        else:
            for x in range(0, 16):
                b = im.getpixel((x, y))
                v = (v << 1) + b
            charmap.append(v >> 8)
            charmap.append(v & 0xFF)

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

const CH_CN Font16CN_Table[] =
{
""" + content + """
};

cFONT Font16CN = {
  Font16CN_Table,
  sizeof(Font16CN_Table) / sizeof(CH_CN),  /*size of table*/
  8, /* ASCII Width */
  16, /* Width */
  18, /* Height */
};

"""
with open('ch_font.c', 'w', encoding='utf-8') as f:
    f.write(content)
