
# import streamlit as st
# from file_handling import (
#     select_file,
#     read_file,
#     tags_to_binary,
#     write_binary_file,
#     binary_to_tags,
#     write_decompressed_file
# )

# from compression import compress
# from decompression import decompress

# st.set_page_config(
#     page_title="LZ77 Algorithm",
#     layout="wide",
# )
# #declaring them as global variables because we need them in st.download_button
# binary_data = ''
# decompressed_text = ''

# st.title("LZ77 Algorithm")

# with st.form("LZ77"):
#     f = st.file_uploader("Choose a file", type="txt")

#     option = st.radio(
#         "Choose an option",
#         ["Compression", "Decompression"],
#         index=None)

#     if st.form_submit_button("Submit"):
#         if f is not None:
#             f = f.getvalue()
#             f = str(f)
#             if option == "Compression":
#                 try:
#                    text = f
#                    tags = compress(text)
#                    st.write("Tags:")
#                    st.write(tags)
#                    binary_data = tags_to_binary(tags)
#                    write_binary_file(
#                     "Output/compressed.txt",
#                     binary_data
#                    )
#                    st.success("File successfully compressed")
#                 except:
#                     st.error("can not compress file")

#             else:

#                 f = f.replace("b'", '')
#                 f = f.replace("'", '')

#                 binary_data = f
#                 try:
#                   tags = binary_to_tags(binary_data)
#                   decompressed_text = decompress(tags)
#                   decompressed_text = decompressed_text.replace("b'", '')
#                   decompressed_text = decompressed_text.replace("'", '')
#                   write_decompressed_file(
#                     "Output/decompressed.txt",
#                     decompressed_text
#                   )
#                   st.success("File successfully decompressed")
#                 except:
#                   st.error("can not decompress file")



# if option == "Compression":
#     st.download_button('Download', data=binary_data, file_name="compressed.txt")
# else:
#     st.download_button('Download', data=decompressed_text, file_name="decompressed.txt")

import streamlit as st

from file_handling import (
    calc_bit_width,
    tags_to_binary,
    convert_bitStream_bytes,
    write_binary_file,
    bytes_to_bitStream,
    binary_to_tags,
    write_decompressed_file
)

from lz77_compression import compress
from lz77_decompression import decompress


st.set_page_config(
    page_title="LZ77 Algorithm",
    page_icon="📄",
    layout="wide",
)

st.title("LZ77 Text File Compressor")
st.write("Compress a text file or decompress a compressed .bin file.")

# Keep results available for the download button
if "binary_data" not in st.session_state:
    st.session_state.binary_data = None

if "decompressed_text" not in st.session_state:
    st.session_state.decompressed_text = None



# Read the header and compressed data from the uploaded .bin file
def read_binary_file_from_upload(uploaded_file):
    file_data = uploaded_file.getvalue()

    if len(file_data) < 6:
        raise ValueError("Invalid compressed file header.")

    pos_bits = file_data[0]
    len_bits = file_data[1]
    tag_count = int.from_bytes(file_data[2:6], "big")
    compressed_bytes = file_data[6:]

    return pos_bits, len_bits, tag_count, compressed_bytes


with st.form("LZ77"):

    f = st.file_uploader(
        "Choose a file",
        type=["txt", "bin"]
    )

    option = st.radio(
        "Choose an option",
        ["Compression", "Decompression"],
        index=None
    )

    submit = st.form_submit_button("Submit")

    if submit:

        if f is None:
            st.warning("Please select a file.")

        elif option is None:
            st.warning("Please choose an option.")

        else:
            try:

                # COMPRESSION
                if option == "Compression":

                    text = f.getvalue().decode("utf-8")

                    tags = compress(text)

                    if not tags:
                        st.warning("The uploaded file is empty.")

                    else:
                        st.write("Tags:")
                        st.write(tags)

                        pos_bits, len_bits = calc_bit_width(tags)

                        binary_data = tags_to_binary(
                            tags,
                            pos_bits,
                            len_bits
                        )

                        final_bytes = convert_bitStream_bytes(
                            binary_data
                        )

                        write_binary_file(
                            "Output/compressed.bin",
                            final_bytes,
                            pos_bits,
                            len_bits,
                            len(tags)
                        )

                        with open("Output/compressed.bin", "rb") as file:
                            st.session_state.binary_data = file.read()

                        st.session_state.decompressed_text = None

                        st.success("File successfully compressed!")

                # DECOMPRESSION
                elif option == "Decompression":

                    (
                        pos_bits,
                        len_bits,
                        tag_count,
                        compressed_bytes
                    ) = read_binary_file_from_upload(f)

                    binary_data = bytes_to_bitStream(compressed_bytes)

                    tags = binary_to_tags(
                        binary_data,
                        pos_bits,
                        len_bits,
                        tag_count
                    )

                    decompressed_text = decompress(tags)

                    write_decompressed_file(
                        "Output/decompressed.txt",
                        decompressed_text
                    )

                    st.session_state.decompressed_text = decompressed_text
                    st.session_state.binary_data = None

                    st.success("File successfully decompressed!")

            except Exception as e:
                st.error(f"Operation failed: {e}")


# Keep the download button outside the form, as in your old GUI
if option == "Compression" and st.session_state.binary_data is not None:

    st.download_button(
        "Download",
        data=st.session_state.binary_data,
        file_name="compressed.bin",
        mime="application/octet-stream"
    )

elif option == "Decompression" and st.session_state.decompressed_text is not None:

    st.download_button(
        "Download",
        data=st.session_state.decompressed_text.encode("utf-8"),
        file_name="decompressed.txt",
        mime="text/plain"
    )