
import streamlit as st
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

st.set_page_config(
    page_title="LZ77 Algorithm",
    layout="wide",
)
#declaring them as global variables because we need them in st.download_button
binary_data = ''
decompressed_text = ''

st.title("LZ77 Algorithm")

with st.form("LZ77"):
    f = st.file_uploader("Choose a file", type="txt")

    option = st.radio(
        "Choose an option",
        ["Compression", "Decompression"],
        index=None)

    if st.form_submit_button("Submit"):
        if f is not None:
            f = f.getvalue()
            f = str(f)
            if option == "Compression":
                try:
                   text = f
                   tags = compress(text)
                   st.write("Tags:")
                   st.write(tags)
                   binary_data = tags_to_binary(tags)
                   write_binary_file(
                    "Output/compressed.txt",
                    binary_data
                   )
                   st.success("File successfully compressed")
                except:
                    st.error("can not compress file")

            else:

                f = f.replace("b'", '')
                f = f.replace("'", '')

                binary_data = f
                try:
                  tags = binary_to_tags(binary_data)
                  decompressed_text = decompress(tags)
                  decompressed_text = decompressed_text.replace("b'", '')
                  decompressed_text = decompressed_text.replace("'", '')
                  write_decompressed_file(
                    "Output/decompressed.txt",
                    decompressed_text
                  )
                  st.success("File successfully decompressed")
                except:
                  st.error("can not decompress file")



if option == "Compression":
    st.download_button('Download', data=binary_data, file_name="compressed.txt")
else:
    st.download_button('Download', data=decompressed_text, file_name="decompressed.txt")