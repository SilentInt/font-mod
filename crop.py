from PIL import Image, ImageDraw, ImageFont, ImageFilter

im = Image.open("./blue30.png")

POS = (0, 0)

X = POS[0] * 80
Y = POS[1] * 80

im1 = im.crop((X, Y, X + 30, Y + 30))


for y in range(im1.size[1]):
    for x in range(im1.size[0]):

        pix = r, g, b, a = im1.getpixel((x, y))
        r = (255 * (255 - a) + r * a) // 255
        g = (255 * (255 - a) + g * a) // 255
        b = (255 * (255 - a) + b * a) // 255
        a = 255

        im1.putpixel((x, y), (r, g, b, a))
        print(pix, r)


im1.show()

im1 = im1.resize((64, 64), Image.LANCZOS)
im1 = im1.filter(ImageFilter.SHARPEN)
im1 = im1.convert('1', dither=Image.NONE)

# im1 = im1.convert('1', dither=Image.FLOYDSTEINBERG)
# im1.show()
# im1.save('./test.bmp')


buf = []
# NOTE: can only handle 8-bit boudary
for y in range(im1.size[1]):
    for x in range(im1.size[0]):
        if x % 8 == 0:
            buf.append(0)

        bit = int(im1.getpixel((x, y)) == 0)
        buf[-1] = (buf[-1] << 1) | bit


# print(buf)
# print(len(buf))

content = """
uint8_t img[] = {
"""+", ".join(map(str, buf))+"""
};
"""
with open('img.h', 'w') as fp:
    fp.write(content)

# with open('raw-img.bin', 'wb') as fp:
#     fp.write(bytes(buf))
