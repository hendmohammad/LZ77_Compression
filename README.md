
# LZ77 Text File Compression

A Python project that implements the **LZ77 lossless compression algorithm** to compress text files into binary files and decompress them back to their original text.

## Features
- Compress and decompress text files.
- Encode LZ77 tags into binary format.
- Store metadata in the compressed file.
- Provide a command-line interface and a Streamlit GUI.

## Technologies
- Python
- Streamlit
- Binary file handling

## Project Structure

```text
LZ77_Compression/
├── GUI.py
├── main.py
├── lz77_compression.py
├── decompression.py
├── file_handling.py
└── Output/
```

## How to Run

Install Streamlit:

```bash
py -m pip install streamlit
```

Run the GUI:

```bash
py -m streamlit run GUI.py
```

Or run the command-line version:

```bash
py main.py
```

## Usage

**Compression:** Upload a `.txt` file, select Compression, and download the resulting `.bin` file.

**Decompression:** Upload a previously compressed `.bin` file, select Decompression, and download the recovered `.txt` file.

## Learning Objectives

This project demonstrates lossless compression, string matching, bit manipulation, binary file handling, and GUI development using Python.
