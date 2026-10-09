from tkinter import filedialog

def select_file():
    return filedialog.askopenfilename()

def read_file(filename):
    with open(filename, "r") as file:
        return file.read()


def number_to_binary(number, bits):
    return format(number, f"0{bits}b")

def binary_to_number(binary):
    return int(binary, 2)

def binary_to_char(binary):
    return chr(int(binary, 2))


def char_to_binary(char):
    return format(ord(char), "08b")


def tag_to_binary(tag):
    pos = number_to_binary(tag["pos"], 16)
    length = number_to_binary(tag["len"], 16)

    if tag["sym"] == "NULL":
        flag = "1"
        return pos + length + flag

    else:
        flag = "0"
        symbol = char_to_binary(tag["sym"])
        return pos + length + flag + symbol


def tags_to_binary(tags):
    binary_data = ""

    for tag in tags:
        binary_data += tag_to_binary(tag)

    return binary_data

def write_binary_file(filename, binary_data):
    with open(filename, "w") as file:
        file.write(binary_data)

def write_decompressed_file(filename, text):
    with open(filename, "w") as file:
        file.write(text)
        
def binary_to_tags(binary_data):
    tags = []
    index = 0

    while index < len(binary_data):
        pos_binary = binary_data[index:index + 16]
        index += 16

        length_binary = binary_data[index:index + 16]
        index += 16

        pos = binary_to_number(pos_binary)
        length = binary_to_number(length_binary)

        flag = binary_data[index]
        index += 1

        if flag == "1":
            next_symbol = "NULL"

        else:
            symbol_binary = binary_data[index:index + 8]
            index += 8

            next_symbol = binary_to_char(symbol_binary)

        tag = f"< {pos} , {length} , {next_symbol} >"
        tags.append(tag)

    return tags