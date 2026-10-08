from file_handling import (
    read_file,
    tags_to_binary,
    write_binary_file,
    binary_to_tags,
    write_decompressed_file
)

from compression import compress
from decompression import decompress


while True:

    print("\n===== LZ77 Compression =====")
    print("1. Compress")
    print("2. Decompress")
    print("3. Exit")

    choice = input("Choose an option: ")

    # Compression
    if choice == "1":

        text = read_file("file1.txt")

        tags = compress(text)

        binary_data = tags_to_binary(tags)

        write_binary_file("file2.txt", binary_data)

        print("\nCompression completed.")
        print("Compressed data saved in file2.txt")

    # Decompression
    elif choice == "2":

        binary_data = read_file("file2.txt")

        tags = binary_to_tags(binary_data)

        decompressed_text = decompress(tags)
        write_decompressed_file("decompressed.txt", decompressed_text)

        print("\nDecompression completed.")
        print("Decompressed text:")
        print(decompressed_text)

    # Exit
    elif choice == "3":

        print("\nGoodbye!")
        break

    else:

        print("\nInvalid choice. Please choose 1, 2, or 3.")

