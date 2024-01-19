
def print_gb2312_characters():
    content = ""
    # ASCII characters
    for k in range(32, 127):
        char_ascii = chr(k)
        content += char_ascii
        # print(char_ascii, end='\n')
    return content


if __name__ == "__main__":
    res = print_gb2312_characters()
    with open('char.txt', 'w', encoding='utf-8') as f:
        f.write(res)
