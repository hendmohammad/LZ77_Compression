from file_handling import (
    select_file,
    read_file,
    tags_to_binary,
    write_binary_file,
    binary_to_tags,
    write_decompressed_file
)

from compression import compress
from decompression import decompress


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

            binary_data = tags_to_binary(tags)

            write_binary_file("Output/compressed.txt", binary_data)

            print("\nCompression completed.")
            print("Compressed data saved in compressed.txt")

        else:
            print("\nNo file selected.")

    # Decompression
    elif choice == "2":

        filename = select_file()

        if filename:
            binary_data = read_file(filename)

            tags = binary_to_tags(binary_data)

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
