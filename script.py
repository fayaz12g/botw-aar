import os
import math
import binascii
import struct

def float_to_hex(f):
    return ''.join('{:02x}'.format(c) for c in struct.pack('!f', f))

def little_endian(hex_str):
    return ''.join(reversed([hex_str[i:i+2] for i in range(0, len(hex_str), 2)]))


def pmtok_hud(ratio_value, HUD_pos, ui_folder):
    ratio_value = float(ratio_value)
    scale_factor = (16/9) / ratio_value
    ieee_hex = float_to_hex(scale_factor)
    little_endian_hex = '0F' + little_endian(ieee_hex)

    original_hex = bytes.fromhex('0F 00 00 80 3F')
    replacement_hex = bytes.fromhex(little_endian_hex)

    for root, dirs, files in os.walk(ui_folder):
        for file in files:
            if file.endswith('.bfres'):
                with open(os.path.join(root, file), 'rb') as bfres_file:
                    content = bfres_file.read()
                content = content.replace(original_hex, replacement_hex)
                with open(os.path.join(root, file), 'wb') as bfres_file:
                    bfres_file.write(content)
                    print(f"Modified {file}")
    if HUD_pos == "corner":
        # Shift stuff
        pass
