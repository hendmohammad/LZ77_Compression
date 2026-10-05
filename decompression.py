def extracting_info_from_tag(tag):
    cleaned_tag = ''
    # removing white space and some of the special characters from tag
    # I didn't remove the comma ',' because it separates  the items of the tag
    for char in tag:
        if char == ' ' or char == '"' or char == '<' or char == '>':
            continue
        else:
            cleaned_tag += char

    # cleaned_tag will be something like 0,0,A
    position , length , next_symbol = cleaned_tag.split(',') # position's and length's data type is 'str' !!

    position = int(position)
    length = int(length)

    return position, length, next_symbol



def decompress(tags):
    decompressed_string = ''
    for tag in tags:
        position, length , next_symbol = extracting_info_from_tag(tag)

        if length == 0:
            decompressed_string += next_symbol
        else:
            i = len(decompressed_string) - position
            for k in range(length):
              decompressed_string += decompressed_string[ i + k ]
            if next_symbol != 'null' and next_symbol != 'NULL':
                decompressed_string += next_symbol

    return decompressed_string







