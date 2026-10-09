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


# calculating no. of bits needed to represent tag nums
def calc_bit_width(tags):
    max_pos = max(tag["pos"] for tag in tags)
    max_len = max(tag["len"] for tag in tags)

    pos_bits = max(1, max_pos.bit_length())  # need min 1 bit if length = 0
    len_bits =max(1, max_len.bit_length())  

    return pos_bits, len_bits


def tag_to_binary(tag, pos_bits, len_bits):

    pos = number_to_binary(tag["pos"], pos_bits)
    length = number_to_binary(tag["len"], len_bits)

    if tag["sym"] == "NULL":
        flag = "1"
        return pos + length + flag

    else:
        flag = "0"
        symbol = char_to_binary(tag["sym"])
        return pos + length + flag + symbol


def tags_to_binary(tags, pos_bits, len_bits):
    binary_data = ""

    for tag in tags:
        binary_data += tag_to_binary(tag, pos_bits, len_bits)

    return binary_data


# grouping each 8bit-sequence into 1 byte & getting all bytes together
def convert_bitStream_bytes(binary_data):

    byte_values = []

    for i in range(0, len(binary_data), 8):

        bit_group = binary_data[i:i+8]

        # if final sequence not 8 digits, make right padding
        if len(bit_group) < 8:
            bit_group = bit_group.ljust(8, "0")

        byte_value = binary_to_number(bit_group)
        byte_values.append(byte_value)

    final_bytes = bytes(byte_values)
    
    return final_bytes


def write_binary_file(filename, binary_data, pos_bits, len_bits, tag_count):
    # Save the metadata in a 6-byte header
    header = ( bytes([pos_bits, len_bits]) + tag_count.to_bytes(4, "big") )

    with open(filename, "wb") as file:
        file.write(header)
        file.write(binary_data)



def read_binary_file(filename):
    with open(filename, "rb") as file:

        header = file.read(6)
        if len(header) != 6:
            raise ValueError("Invalid compressed file header.")

        pos_bits = header[0]
        len_bits = header[1]
        tag_count = int.from_bytes(header[2:6], "big")

        compressed_bytes = file.read()

    return pos_bits, len_bits, tag_count, compressed_bytes


def bytes_to_bitStream(compressed_bytes):
    binary_data = ""

    for byte in compressed_bytes:
        binary_data += format(byte, "08b")

    return binary_data

        
def binary_to_tags(binary_data, pos_bits, len_bits, tag_count):
    tags = []
    index = 0

    for i in range(tag_count):

        # read position using its saved width
        pos_binary = binary_data[index:index + pos_bits]
        position = binary_to_number(pos_binary)
        index += pos_bits

        # read length using its saved width
        length_binary = binary_data[index:index + len_bits]
        length = binary_to_number(length_binary)
        index += len_bits

        # read the flag
        flag = binary_data[index]
        index += 1

        # read the symbol when the flag is 0 only
        if flag == "1":
            next_symbol = "NULL"
            
        else:
            symbol_binary = binary_data[index:index + 8]
            next_symbol = binary_to_char(symbol_binary)
            index += 8

        tag = f"< {position} , {length} , {next_symbol} >"
        tags.append(tag)

    return tags


def write_decompressed_file(filename, text):
    with open(filename, "w") as file:
        file.write(text)
