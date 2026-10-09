from file_handling import (
    select_file,
    read_file,
    calc_bit_width,
    tags_to_binary,
    convert_bitStream_bytes,
    write_binary_file,
    read_binary_file,
    bytes_to_bitStream,
    binary_to_tags,
    write_decompressed_file
)

from lz77_compression import compress
from lz77_decompression import decompress


while True:

    print("\n\nLZ77 Text File Compressor: \n ")
    print("1. Compress")
    print("2. Decompress")
    print("3. Exit")

    choice = input("Choose an option: ")

    # Compression
    if choice == "1":

        filename = select_file()

        if filename:
            text = read_file(filename)

            tags = compress(text)
            pos_bits, len_bits = calc_bit_width(tags)
            binary_data = tags_to_binary(tags,pos_bits, len_bits)
            final_bytes = convert_bitStream_bytes(binary_data)

            write_binary_file("Output/compressed.bin",final_bytes, pos_bits, len_bits, len(tags))
            print("\nCompression completed.")
            print("Compressed data saved in compressed.bin")

        else:
            print("\nNo file selected.")

    # Decompression
    elif choice == "2":

        filename = select_file()

        if filename:

            # reading metadata and compressed bytes
            pos_bits, len_bits, tag_count, compressed_bytes = ( read_binary_file(filename) )

            # converting bytes into bitstream
            binary_data = bytes_to_bitStream(compressed_bytes)

            # decoding bitstream into tags
            tags = binary_to_tags(binary_data, pos_bits, len_bits, tag_count)

            decompressed_text = decompress(tags)

            write_decompressed_file(
                "Output/decompressed.txt",
                decompressed_text
            )

            print("\nDecompression completed.")
            print("Decompressed data saved in decompressed.txt")
        
        else:
            print("\nNo file selected.")

    # Exit
    elif choice == "3":

        print("\nGoodbye!")
        break

    else:

        print("\nInvalid choice. Please choose 1, 2, or 3.")
