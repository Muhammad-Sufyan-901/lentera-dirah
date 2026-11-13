#!/usr/bin/env python3
"""Restyle Bahula into a Balinese-looking young man.

White shirt/sarong + brown udeng (head wrap) + gold sash, keeping the
Ninja Adventure animation frames intact.

Source (pristine, CC0): Game/Tools/source/*_original.png
Output: Game/Assets/_Project/Art/Characters/*.png

Pure Python standard library (zlib + struct).
"""

import os
import struct
import zlib

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(TOOLS_DIR, "source")
OUT_DIR = os.path.normpath(os.path.join(TOOLS_DIR, "..", "Assets", "_Project", "Art", "Characters"))

FRAME = 16

# Original palette (Ninja Adventure monk)
OUTLINE = (0x14, 0x1B, 0x1B)
HAIR_DARK = (0x3B, 0x36, 0x43)
HAIR_LIGHT = (0x4E, 0x48, 0x4A)
ROBE_RED = (0xD1, 0x4B, 0x34)
SKIN = (0xEF, 0x91, 0x4F)
BAND_GREEN = (0x56, 0x86, 0x4C)
GREEN_DARK = (0x34, 0x5A, 0x52)
EYE_WHITE = (0xE3, 0xF1, 0xF5)
SHADOW_PINK = (0xD3, 0xA2, 0xC0)

# Balinese palette
UDENG_MID = (0x6B, 0x4A, 0x2F)
UDENG_LIGHT = (0x8A, 0x62, 0x38)
UDENG_DARK = (0x4A, 0x30, 0x18)
UDENG_SHADOW = (0x3F, 0x2A, 0x18)
SHIRT = (0xF4, 0xEF, 0xE6)
SHIRT_SHADE = (0xD8, 0xD1, 0xC2)
SKIN_SHADE = (0xC9, 0x7A, 0x45)
SKIN_MID = (0xE0, 0x8A, 0x4C)
GOLD = (0xFF, 0xB8, 0x4D)
GOLD_DARK = (0xB8, 0x7A, 0x22)


def read_png(path):
    data = open(path, "rb").read()
    pos = 8
    idat = bytearray()
    width = height = 0
    color_type = 6

    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        chunk_type = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + length]
        pos += 12 + length

        if chunk_type == b"IHDR":
            width, height, _depth, color_type, _comp, _filt, _inter = struct.unpack(">IIBBBBB", chunk)
        elif chunk_type == b"IDAT":
            idat += chunk
        elif chunk_type == b"IEND":
            break

    raw = zlib.decompress(bytes(idat))
    bpp = 4 if color_type == 6 else 3
    stride = width * bpp
    pixels = bytearray()
    previous = bytearray(stride)
    cursor = 0

    for _y in range(height):
        filter_type = raw[cursor]
        cursor += 1
        line = bytearray(raw[cursor:cursor + stride])
        cursor += stride

        if filter_type == 1:
            for x in range(bpp, stride):
                line[x] = (line[x] + line[x - bpp]) & 255
        elif filter_type == 2:
            for x in range(stride):
                line[x] = (line[x] + previous[x]) & 255
        elif filter_type == 3:
            for x in range(stride):
                left = line[x - bpp] if x >= bpp else 0
                line[x] = (line[x] + ((left + previous[x]) // 2)) & 255
        elif filter_type == 4:
            for x in range(stride):
                a = line[x - bpp] if x >= bpp else 0
                b = previous[x]
                c = previous[x - bpp] if x >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                predictor = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + predictor) & 255

        pixels += line
        previous = line

    return width, height, bpp, pixels


def write_png(path, width, height, pixels):
    raw = bytearray()
    for y in range(height):
        raw.append(0)
        raw += pixels[y * width * 4:(y + 1) * width * 4]

    def chunk(tag, payload):
        return (struct.pack(">I", len(payload)) + tag + payload +
                struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF))

    data = (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))
    open(path, "wb").write(data)


def restyle_sheet(pixels, width, height, bpp, head_band_limit, robe_start):
    """Recolor a 16 px frame sheet. head_band_limit / robe_start are frame-local."""
    out = bytearray(pixels)
    for y in range(height):
        frame_y = y % FRAME
        for x in range(width):
            offset = (y * width + x) * bpp
            if pixels[offset + 3] == 0:
                continue
            color = (pixels[offset], pixels[offset + 1], pixels[offset + 2])
            mapped = None

            if frame_y <= head_band_limit:
                if color == HAIR_DARK:
                    mapped = UDENG_DARK
                elif color == HAIR_LIGHT:
                    mapped = UDENG_LIGHT
                elif color == BAND_GREEN:
                    mapped = UDENG_MID
                elif color == GREEN_DARK:
                    mapped = UDENG_SHADOW
            elif frame_y < robe_start:
                # clean-shaven jaw: blend the monk's moustache into skin
                if color in (HAIR_LIGHT, HAIR_DARK):
                    mapped = SKIN
            else:
                if color == ROBE_RED:
                    mapped = SHIRT
                elif color == HAIR_DARK:
                    mapped = SHIRT_SHADE
                elif color == HAIR_LIGHT:
                    mapped = SHIRT_SHADE
                elif color == BAND_GREEN:
                    mapped = GOLD
                elif color == GREEN_DARK:
                    mapped = GOLD_DARK
                elif color == SHADOW_PINK:
                    mapped = SHIRT

            if mapped is not None:
                out[offset] = mapped[0]
                out[offset + 1] = mapped[1]
                out[offset + 2] = mapped[2]

    # udeng fold line across the forehead (frame-local, all frames)
    for y in range(height):
        if y % FRAME != 4:
            continue
        for x in range(width):
            offset = (y * width + x) * bpp
            if pixels[offset + 3] == 0:
                continue
            color = (pixels[offset], pixels[offset + 1], pixels[offset + 2])
            if color in (HAIR_DARK, HAIR_LIGHT, BAND_GREEN, GREEN_DARK) and 4 <= (x % FRAME) <= 11:
                out[offset] = UDENG_LIGHT[0]
                out[offset + 1] = UDENG_LIGHT[1]
                out[offset + 2] = UDENG_LIGHT[2]

    return out


def restyle_faceset(pixels, width, height, bpp):
    out = bytearray(pixels)
    robe_start = int(height * 0.78)
    for y in range(height):
        for x in range(width):
            offset = (y * width + x) * bpp
            if pixels[offset + 3] == 0:
                continue
            color = (pixels[offset], pixels[offset + 1], pixels[offset + 2])
            mapped = None

            if color == HAIR_DARK:
                mapped = UDENG_DARK if y < robe_start else SHIRT_SHADE
            elif color == HAIR_LIGHT:
                mapped = UDENG_LIGHT if y < robe_start else SHIRT_SHADE
            elif color == BAND_GREEN:
                mapped = UDENG_MID if y < robe_start else GOLD
            elif color == GREEN_DARK:
                mapped = UDENG_SHADOW if y < robe_start else GOLD_DARK
            elif color == ROBE_RED and y >= robe_start:
                mapped = SHIRT

            if mapped is not None:
                out[offset] = mapped[0]
                out[offset + 1] = mapped[1]
                out[offset + 2] = mapped[2]

    return out


def main():
    jobs = [
        ("Bahula_SpriteSheet_original.png", "Bahula_SpriteSheet.png", "sheet"),
        ("Bahula_IdleSheet_original.png", "Bahula_IdleSheet.png", "sheet"),
        ("Bahula_Faceset_original.png", "Bahula_Faceset.png", "faceset"),
    ]

    for source_name, target_name, kind in jobs:
        source_path = os.path.join(SOURCE_DIR, source_name)
        target_path = os.path.join(OUT_DIR, target_name)

        if not os.path.exists(source_path):
            print(f"  skip {source_name} (source tidak ada)")
            continue

        width, height, bpp, pixels = read_png(source_path)

        if kind == "sheet":
            result = restyle_sheet(pixels, width, height, bpp, head_band_limit=9, robe_start=13)
        else:
            result = restyle_faceset(pixels, width, height, bpp)

        write_png(target_path, width, height, result)
        print(f"  restyled {target_name} ({width}x{height})")

    print("Done.")


if __name__ == "__main__":
    main()
