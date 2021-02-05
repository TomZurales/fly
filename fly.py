#!/usr/bin/python3

import sys
import zlib

ZIP_EXT = ".zip"

CENTRAL_DIRECTORY_HEADER = b'\x50\x4b\x01\x02'
CENTRAL_DIRECTORY_PTR_OFFSET = -6
MAGIC = b'\x8B\xAD\xF0\x0D'

if "-h" in sys.argv:
    print("Usage: fly input_file.zip payload output_file [-h] [-b] [-z]")
    print("-h   Show this help message")
    print("-z   Zip the payload before adding it to the input file")
    sys.exit()

with open(sys.argv[1], "rb+") as f:
    zip_file = f.read()

with open(sys.argv[2], "rb") as f:
    p = f.read()
    if "-z" in sys.argv:
        p = zlib.compress(p)
    payload = b''.join([MAGIC, p])

payload_pos = zip_file.find(CENTRAL_DIRECTORY_HEADER)
pre_payload = zip_file[:payload_pos]
post_payload = zip_file[payload_pos:]
payload_size = len(bytes(payload))
central_directory_ptr = int.from_bytes(post_payload[CENTRAL_DIRECTORY_PTR_OFFSET:CENTRAL_DIRECTORY_PTR_OFFSET + 4], byteorder='little')
central_directory_ptr += payload_size
post_payload = b"".join([post_payload[:CENTRAL_DIRECTORY_PTR_OFFSET], central_directory_ptr.to_bytes(4, "little"), post_payload[CENTRAL_DIRECTORY_PTR_OFFSET + 2:]])

out = b"".join([pre_payload, payload, post_payload])

new_file = sys.argv[3]
if new_file[-4:] != ZIP_EXT:
    new_file = "".join([new_file, ZIP_EXT])
with open(new_file, 'wb') as f:
    f.write(out)
