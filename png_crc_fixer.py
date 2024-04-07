from zlib import crc32
"""
This script will take a file named broken.png with incorrect CRCs and fix them.
There will be an output file names fixed.png with correct CRCs.
"""

with open("broken.png", "rb") as image_file, open("fixed.png", "wb") as output_file:
    header = image_file.read(8)
    output_file.write(header)
    data_left = True
    while data_left:
        chunk_length = image_file.read(4)
        chunk_length_int = int.from_bytes(chunk_length, "big")
        chunk_type = image_file.read(4)
        chunk_data = image_file.read(chunk_length_int)
        crc_data = image_file.read(4)

        proper_crc = crc32(chunk_type + chunk_data).to_bytes(4, byteorder='big')
        print(f"{chunk_type.decode()} CRC {crc_data.hex()} should be {proper_crc.hex()} chunk size is {chunk_length_int}")
        output_file.write(chunk_length)
        output_file.write(chunk_type)
        output_file.write(chunk_data)
        output_file.write(proper_crc)

        if chunk_length_int == 0:
            data_left = False
