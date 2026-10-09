def extracting_info_from_tag(tag):

    # removing "<" , ">" , white spaces on both sides
    cleaned_tag = tag.replace('<', '').replace('>', '').replace('"', '').strip()

    # take each character till the comma ","
    position, length, next_symbol = cleaned_tag.split(',', 2)

    # remove white spaces 
    position = int(position.strip())
    length = int(length.strip())
    next_symbol = next_symbol.strip()

    # if empty string >> the next symbol is white space

    if next_symbol == '':
        next_symbol = ' '

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







