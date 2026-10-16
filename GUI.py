import streamlit as st

from file_handling import (
    calc_bit_width,
    tags_to_binary,
    convert_bitStream_bytes,
    write_binary_file,
    bytes_to_bitStream,
    binary_to_tags,
    write_decompressed_file,
    read_binary_file_from_upload
)

from lz77_compression import compress
from lz77_decompression import decompress


st.set_page_config(
    page_title="LZ77 Algorithm",
    page_icon="📄",
    layout="wide",
)



# Keep results available for the download button
if "binary_data" not in st.session_state:
    st.session_state.binary_data = None

if "decompressed_text" not in st.session_state:
    st.session_state.decompressed_text = None

st.title("LZ77 Text File Compressor")
st.write("Compress a text file or decompress a compressed.bin file.")


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


# Download button
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