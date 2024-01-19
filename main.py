from PIL import Image, ImageFont, ImageDraw


def get_font_size(character: str, font: ImageFont):
    # 获取字体大小
    bbox = font.getbbox(character)
    # print(bbox)  # left, top, right, bottom
    width = bbox[2]
    height = bbox[3]-bbox[0]
    # print(width, height)
    return width, height


def create_binary_image(font: ImageFont, character: str,
                        width: int, height: int):
    fwidth, fheight = get_font_size(character, font)

    image = Image.new('1', (width, height), 1)  # 1表示二值化图片，白底黑字
    draw = ImageDraw.Draw(image)
    # anchor='mm'表示以图片中心为锚点
    draw.text((0, height*0.8), character,
              anchor='ls', font=font, fill=0)  # 0表示黑色字体
    # image.show()
    return image


def image_to_matrix(image: Image, width: int, height: int):
    # 图片转换为矩阵
    matrix = []
    pixels = list(image.getdata())
    # print(pixels)
    # for i in range(0, height):
    #     for j in range(0, width, 8):
    #         byte = 0
    #         for k in range(8):
    #             if j + k < width and pixels[i * width + j + k] == 0:
    #                 byte |= (1 << (7 - k))
    #         matrix.append(byte)
    #
    for i in range(0, height*width, 8):
        byte = 0
        for j in range(8):
            if i + j < height*width and pixels[i + j] == 0:
                byte |= (1 << (7 - j))
        matrix.append(byte)
    return matrix


def wrap_struct_data(character: str, width: int, height: int, matrix):
    # 按照定长分割行
    matrix_s = ''
    for i, b in enumerate(matrix):
        if i % 12 == 0:
            matrix_s += '\n'
        matrix_s += f'0x{b:02x},'

    character = character.replace('\\', '\\\\').replace('\"', '\\\"')
    struct_data = f"\"{character}\",\n {int(width)}, {int(height)},{matrix_s}"

    return struct_data


def char_to_map(char: str, font_path, font_size: int):
    """
    字符转换为字模
    :param char: 字符
    :param font_path: 字体文件路径
    :param font_size: 字体大小
    :return: 字模
    """
    # 读取字体文件
    font = ImageFont.truetype(font_path, font_size)
    # 获取字体大小
    width, height = get_font_size(char, font)
    # 创建二值化图片
    image = create_binary_image(font, char, width, 21)
    # image.show()
    # 图片转换为矩阵
    matrix = image_to_matrix(image, width, 21)
    # 封装格式
    struct_data = wrap_struct_data(char, width, 21, matrix)
    # print(struct_data)
    return struct_data


font_path = "./fonts/SourceHanSansCN-Light.otf"
# char_to_map('我', font_path, 16)

chars = ''
# 读入待转换的字符
with open('char.txt', 'r', encoding='utf-8') as f:
    chars = f.read()

# 为chars去重
chars = sorted(set(chars.replace('\n', '')))

# for i, c in enumerate(chars):
#     print(i, c)

# 将字符转换为字模
char_map = '\n'.join(
    ['{'+char_to_map(c, font_path, 16)+'},' for c in chars])

result_map = f"""\
#include "fonts.h"

const CH_CN_v vFont_Table[] = {'{'}
{char_map}
{'}'};

vFONT Font16v = {'{'}
  vFont_Table,
    {21},
  sizeof(vFont_Table) / sizeof(CH_CN_v),
{'}'};
"""

# print(result_map)
with open('font16v.c', 'w', encoding='utf-8') as f:
    f.write(result_map)
