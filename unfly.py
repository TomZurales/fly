#!/usr/bin/python3

import sys
import zlib

ZIP_EXT = ".zip"

CENTRAL_DIRECTORY_HEADER = b'\x50\x4b\x01\x02'
MAGIC = b'\x8B\xAD\xF0\x0D'

if "-h" in sys.argv:
    print("Usage: unfly input_file.zip output_file [-h] [-b] [-z]")
    print("-h   Show this help message")
    print("-z   Unzip the payload before writing it to the output file")
    sys.exit()

with open(sys.argv[1], "rb") as f:
    zip_file = f.read()

if zip_file.find(MAGIC) == -1:
    print("This file contains no hidden data")
    sys.exit()

payload_begin = zip_file.find(MAGIC) + len(MAGIC)
payload_end = zip_file.find(CENTRAL_DIRECTORY_HEADER)

out = zip_file[payload_begin:payload_end]
if "-z" in sys.argv:
    out = zlib.decompress(out)
with open(sys.argv[2], 'wb') as f:
    f.write(out)
