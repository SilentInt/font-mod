

def print_gb2312_characters():
    content = ""
    # ASCII characters
    for k in range(32, 127):
        char_ascii = chr(k)
        content += char_ascii
        # print(char_ascii, end='\n')
    for i in range(0xA1, 0xF8):
        for j in range(0xA1, 0xFF):
            # 避免遇到一些无效的编码
            if (i == 0xAA and j == 0xA1) or (i == 0xBA and j == 0xA1) or (i == 0xD7 and j == 0xFA):
                continue
            # 使用gb2312编码解码
            char_bytes = bytes([i, j])
            try:
                # 判断是否为ASCII字符
                if char_bytes[0] < 0x80 and char_bytes[1] < 0x80:
                    char_ascii = char_bytes.decode('ascii')
                    content += char_ascii
                    # print(char_ascii, end='\n')
                else:
                    char_gb2312 = char_bytes.decode('gb2312')
                    content += char_gb2312
                    # print(char_gb2312, end='\n')
            except UnicodeDecodeError:
                pass
    return content


if __name__ == "__main__":
    res = print_gb2312_characters()
    with open('char.txt', 'w', encoding='utf-8') as f:
        f.write(res)
