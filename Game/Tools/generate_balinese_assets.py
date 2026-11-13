#!/usr/bin/env python3
"""Generate original CC0 pixel-art Balinese props for Lentera Dirah.

Pure Python standard library (zlib + struct) - no Pillow required.
Output: Game/Assets/_Project/Art/Environment/*.png (RGBA, 16 px grid,
palette matching the Ninja Adventure art direction and the GDD).
"""

import math
import os
import struct
import zlib

OUT_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Assets", "_Project", "Art", "Environment")
)

# --- Rwa Bhineda palette -----------------------------------------------------
MIDNIGHT = (0x12, 0x13, 0x24, 255)
GOLD = (0xFF, 0xB8, 0x4D, 255)
GOLD_DARK = (0xB8, 0x7A, 0x22, 255)
CREAM = (0xE8, 0xE2, 0xD0, 255)
STONE_LIGHT = (0xB8, 0xB0, 0x9A, 255)
STONE = (0x8E, 0x88, 0x76, 255)
STONE_DARK = (0x5A, 0x55, 0x48, 255)
STONE_SHADOW = (0x33, 0x30, 0x2A, 255)
BRICK = (0x9A, 0x5A, 0x40, 255)
BRICK_DARK = (0x6B, 0x3A, 0x28, 255)
LEAF = (0x3E, 0x6B, 0x3A, 255)
LEAF_DARK = (0x27, 0x4A, 0x2A, 255)
LEAF_LIGHT = (0x5C, 0x8A, 0x4A, 255)
TRUNK = (0x6B, 0x4A, 0x2F, 255)
TRUNK_DARK = (0x46, 0x2F, 0x1E, 255)
ROOF = (0x8C, 0x3B, 0x2E, 255)
ROOF_DARK = (0x5A, 0x24, 0x1C, 255)


class Canvas:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.px = [[None] * width for _ in range(height)]

    def set(self, x, y, color):
        if color is not None and 0 <= x < self.w and 0 <= y < self.h:
            self.px[y][x] = color

    def rect(self, x0, y0, x1, y1, color):
        for y in range(int(y0), int(y1) + 1):
            for x in range(int(x0), int(x1) + 1):
                self.set(x, y, color)

    def hline(self, x0, x1, y, color):
        for x in range(int(x0), int(x1) + 1):
            self.set(x, int(y), color)

    def vline(self, x, y0, y1, color):
        for y in range(int(y0), int(y1) + 1):
            self.set(int(x), y, color)

    def ellipse(self, cx, cy, rx, ry, color):
        for y in range(int(cy - ry), int(cy + ry) + 1):
            for x in range(int(cx - rx), int(cx + rx) + 1):
                dx = (x - cx) / max(rx, 0.001)
                dy = (y - cy) / max(ry, 0.001)
                if dx * dx + dy * dy <= 1.0:
                    self.set(x, y, color)

    def line(self, x0, y0, x1, y1, color):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def mirror_left(self):
        for y in range(self.h):
            for x in range(self.w // 2):
                source = self.px[y][x]
                if source is not None:
                    self.px[y][self.w - 1 - x] = source

    def outline(self, color=MIDNIGHT):
        snapshot = [row[:] for row in self.px]
        for y in range(self.h):
            for x in range(self.w):
                if snapshot[y][x] is not None:
                    continue
                for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + ox, y + oy
                    if 0 <= nx < self.w and 0 <= ny < self.h and snapshot[ny][nx] is not None:
                        self.px[y][x] = color
                        break

    def save(self, path):
        raw = bytearray()
        for row in self.px:
            raw.append(0)
            for color in row:
                if color is None:
                    raw.extend((0, 0, 0, 0))
                else:
                    raw.extend(color)

        def chunk(tag, data):
            return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

        header = struct.pack(">IIBBBBB", self.w, self.h, 8, 6, 0, 0, 0)
        png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b"")

        with open(path, "wb") as handle:
            handle.write(png)
        print(f"  wrote {os.path.basename(path)} ({self.w}x{self.h})")


def upscale(source, factor):
    canvas = Canvas(source.w * factor, source.h * factor)
    for y in range(source.h):
        for x in range(source.w):
            color = source.px[y][x]
            if color is None:
                continue
            canvas.rect(x * factor, y * factor, x * factor + factor - 1, y * factor + factor - 1, color)
    return canvas


# --- Gapura / Candi Bentar ---------------------------------------------------
def draw_candi_bentar():
    canvas = Canvas(96, 80)

    # Split gate: left tower occupies x 4..31, gap x 32..63 (2 tiles wide), mirrored.
    tiers = [
        (0, 56, 79),   # base
        (2, 46, 56),
        (5, 38, 46),
        (8, 30, 38),
        (10, 22, 30),
        (12, 16, 22),
    ]

    for inset, top, bottom in tiers:
        x0 = 4 + inset
        x1 = 31 - inset
        canvas.rect(x0, top, x1, bottom, STONE)
        canvas.hline(x0, x1, top, STONE_LIGHT)
        canvas.hline(x0, x1, bottom, STONE_DARK)

    # brick masonry on the base
    for y in range(58, 79, 4):
        canvas.hline(4, 31, y, STONE_DARK)
        offset = 0 if (y // 4) % 2 else 2
        for x in range(5 + offset, 31, 4):
            canvas.set(x, y - 2, BRICK)
            canvas.set(x + 1, y - 2, BRICK_DARK)

    # carved niche with gold frame
    canvas.rect(11, 60, 24, 72, STONE_SHADOW)
    canvas.hline(11, 24, 60, GOLD)
    canvas.hline(11, 24, 72, GOLD_DARK)
    canvas.vline(11, 60, 72, GOLD_DARK)
    canvas.vline(24, 60, 72, GOLD_DARK)
    canvas.vline(17, 63, 71, GOLD)
    canvas.set(18, 62, GOLD)

    # tier trim
    canvas.hline(6, 29, 46, GOLD_DARK)
    canvas.hline(9, 26, 38, GOLD)
    canvas.hline(12, 23, 30, GOLD_DARK)
    canvas.hline(14, 21, 22, GOLD)
    canvas.rect(17, 11, 18, 16, GOLD)
    canvas.set(17, 10, CREAM)
    canvas.set(18, 10, CREAM)

    # low threshold strip inside the gap so the passage reads as a doorway
    canvas.rect(33, 77, 62, 79, STONE_DARK)
    canvas.hline(33, 62, 76, STONE_SHADOW)

    canvas.mirror_left()
    canvas.outline()
    return canvas


# --- Pohon Beringin ----------------------------------------------------------
def draw_beringin_big():
    canvas = Canvas(64, 80)

    # roots and trunk
    canvas.rect(27, 44, 36, 77, TRUNK)
    canvas.rect(33, 44, 36, 77, TRUNK_DARK)
    canvas.line(26, 74, 20, 79, TRUNK)
    canvas.line(37, 74, 43, 79, TRUNK_DARK)
    canvas.line(28, 76, 24, 79, TRUNK_DARK)

    # canopy mass
    canvas.ellipse(32, 31, 30, 21, LEAF_DARK)
    canvas.ellipse(32, 29, 27, 18, LEAF)
    canvas.ellipse(13, 33, 11, 10, LEAF)
    canvas.ellipse(51, 33, 11, 10, LEAF)
    canvas.ellipse(21, 19, 12, 10, LEAF)
    canvas.ellipse(43, 19, 12, 10, LEAF)

    # canopy highlights
    canvas.ellipse(23, 17, 8, 5, LEAF_LIGHT)
    canvas.ellipse(41, 21, 7, 4, LEAF_LIGHT)
    canvas.ellipse(15, 29, 5, 4, LEAF_LIGHT)
    canvas.ellipse(50, 30, 4, 3, LEAF_LIGHT)

    # inner shadow pockets
    canvas.ellipse(32, 40, 12, 5, LEAF_DARK)
    canvas.ellipse(9, 40, 4, 3, LEAF_DARK)
    canvas.ellipse(55, 40, 4, 3, LEAF_DARK)

    # hanging aerial roots
    for x, start, end in ((10, 41, 60), (16, 44, 66), (23, 45, 58), (41, 45, 63), (48, 44, 68), (54, 41, 59)):
        for y in range(start, end, 2):
            canvas.set(x, y, TRUNK_DARK)

    canvas.outline()
    return canvas


def draw_beringin_small():
    canvas = Canvas(40, 56)

    canvas.rect(17, 28, 23, 52, TRUNK)
    canvas.rect(21, 28, 23, 52, TRUNK_DARK)
    canvas.line(16, 50, 11, 55, TRUNK)
    canvas.line(24, 50, 29, 55, TRUNK_DARK)

    canvas.ellipse(20, 20, 18, 13, LEAF_DARK)
    canvas.ellipse(20, 19, 16, 11, LEAF)
    canvas.ellipse(9, 23, 7, 6, LEAF)
    canvas.ellipse(31, 23, 7, 6, LEAF)
    canvas.ellipse(14, 12, 7, 5, LEAF_LIGHT)
    canvas.ellipse(26, 15, 5, 4, LEAF_LIGHT)
    canvas.ellipse(20, 27, 8, 3, LEAF_DARK)

    for x, start, end in ((7, 28, 42), (12, 30, 46), (28, 30, 44), (33, 28, 40)):
        for y in range(start, end, 2):
            canvas.set(x, y, TRUNK_DARK)

    canvas.outline()
    return canvas


# --- Pura Meru ---------------------------------------------------------------
def draw_meru():
    canvas = Canvas(48, 96)

    # stone platform
    canvas.rect(5, 84, 42, 95, STONE_DARK)
    canvas.rect(8, 87, 39, 95, STONE)
    canvas.hline(8, 39, 87, STONE_LIGHT)
    canvas.hline(5, 42, 84, STONE_SHADOW)
    for x in range(9, 39, 6):
        canvas.vline(x, 88, 94, STONE_DARK)

    # central pole
    canvas.rect(21, 18, 26, 86, TRUNK)
    canvas.vline(26, 18, 86, TRUNK_DARK)

    # seven tiered roofs (bottom -> top)
    tiers = [(76, 36), (66, 32), (56, 29), (46, 26), (36, 22), (26, 18), (17, 14)]

    for index, (top_y, width) in enumerate(tiers):
        bottom = top_y + 7
        x0 = 24 - width // 2
        x1 = 23 + width // 2
        inner = max(3, width - 10)

        canvas.rect(x0, top_y + 3, x1, bottom, ROOF)
        canvas.hline(x0, x1, bottom, ROOF_DARK)
        canvas.rect(x0 + 2, top_y, x0 + inner - 4, top_y + 3, ROOF)
        canvas.rect(x1 - inner + 4, top_y, x1 - 2, top_y + 3, ROOF)
        canvas.hline(x0, x1, top_y + 6, GOLD_DARK)
        canvas.hline(x0 + 1, x1 - 1, top_y + 2, GOLD)

        # upturned eave tips
        canvas.set(x0 - 1, top_y + 2, ROOF)
        canvas.set(x0 - 2, top_y + 1, ROOF)
        canvas.set(x1 + 1, top_y + 2, ROOF)
        canvas.set(x1 + 2, top_y + 1, ROOF)

    # finial
    canvas.rect(23, 8, 24, 16, GOLD_DARK)
    canvas.rect(22, 10, 25, 12, GOLD)
    canvas.set(23, 6, CREAM)
    canvas.set(24, 6, CREAM)
    canvas.set(23, 5, GOLD)

    canvas.outline()
    return canvas


# --- Bale Kulkul -------------------------------------------------------------
def draw_bale_kulkul():
    canvas = Canvas(48, 48)

    canvas.rect(5, 40, 42, 47, STONE_DARK)
    canvas.rect(7, 42, 40, 47, STONE)
    canvas.hline(7, 40, 42, STONE_LIGHT)

    for x in (9, 37):
        canvas.rect(x, 21, x + 3, 44, TRUNK)
        canvas.vline(x + 3, 21, 44, TRUNK_DARK)

    canvas.rect(6, 18, 41, 22, TRUNK_DARK)
    canvas.hline(6, 41, 18, TRUNK)
    canvas.hline(7, 40, 19, GOLD_DARK)

    # tiered thatch roof
    canvas.rect(7, 12, 40, 18, ROOF)
    canvas.rect(9, 8, 38, 12, ROOF)
    canvas.rect(12, 5, 35, 8, ROOF)
    canvas.hline(7, 40, 18 - 1, ROOF_DARK)
    canvas.hline(9, 38, 8, GOLD_DARK)
    canvas.hline(12, 35, 5, GOLD)
    canvas.set(23, 3, GOLD)
    canvas.set(24, 3, GOLD)

    # hanging drum
    canvas.vline(23, 22, 25, TRUNK_DARK)
    canvas.rect(17, 25, 30, 35, TRUNK)
    canvas.rect(18, 26, 29, 34, BRICK)
    canvas.hline(17, 30, 25, GOLD_DARK)
    canvas.hline(17, 30, 35, GOLD_DARK)
    canvas.hline(18, 29, 29, GOLD)
    canvas.set(19, 27, CREAM)
    canvas.set(20, 27, CREAM)

    canvas.outline()
    return canvas


# --- Pelinggih ---------------------------------------------------------------
def draw_pelinggih():
    canvas = Canvas(24, 32)

    canvas.rect(3, 27, 20, 31, STONE_DARK)
    canvas.rect(4, 28, 19, 31, STONE)
    canvas.hline(4, 19, 28, STONE_LIGHT)

    canvas.rect(7, 17, 16, 28, TRUNK)
    canvas.vline(15, 17, 28, TRUNK_DARK)
    canvas.hline(7, 16, 20, GOLD_DARK)
    canvas.hline(7, 16, 24, GOLD_DARK)

    canvas.rect(5, 13, 18, 17, ROOF)
    canvas.rect(7, 9, 16, 13, ROOF)
    canvas.rect(9, 6, 14, 9, ROOF)
    canvas.hline(5, 18, 16, ROOF_DARK)
    canvas.hline(5, 18, 13, GOLD_DARK)
    canvas.hline(7, 16, 9, GOLD)
    canvas.set(11, 4, GOLD)
    canvas.set(12, 4, GOLD)
    canvas.set(11, 3, CREAM)

    canvas.outline()
    return canvas


# --- Penjor ------------------------------------------------------------------
def draw_penjor():
    canvas = Canvas(16, 64)

    for y in range(58, 8, -1):
        x = 4 + int(round(5 * (1 - y / 58.0)))
        canvas.set(x, y, GOLD_DARK)
        canvas.set(x + 1, y, TRUNK)
        if y % 8 == 0:
            canvas.set(x, y, GOLD)

    # top leaves (janur crest)
    canvas.line(9, 9, 2, 2, LEAF)
    canvas.line(9, 9, 4, 1, LEAF_LIGHT)
    canvas.line(9, 8, 8, 0, LEAF)
    canvas.line(10, 8, 13, 1, LEAF_LIGHT)
    canvas.line(10, 9, 15, 4, LEAF)
    canvas.line(9, 11, 2, 7, LEAF_DARK)
    canvas.line(10, 13, 14, 10, LEAF_DARK)

    # hanging janur decorations
    for y in range(15, 47, 7):
        canvas.rect(9, y, 12, y + 4, CREAM)
        canvas.set(13, y + 1, GOLD)
        canvas.set(8, y + 2, GOLD_DARK)
        canvas.rect(3, y + 1, 4, y + 5, GOLD)
        canvas.rect(5, y + 3, 6, y + 6, CREAM)

    # lamp at the base
    canvas.rect(3, 56, 7, 61, GOLD_DARK)
    canvas.rect(4, 57, 6, 60, GOLD)
    canvas.set(5, 58, CREAM)

    canvas.outline()
    return canvas


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"Generating Balinese environment art into {OUT_DIR}")

    gapura = draw_candi_bentar()
    gapura.save(os.path.join(OUT_DIR, "Gapura_CandiBentar.png"))
    upscale(gapura, 2).save(os.path.join(OUT_DIR, "Gapura_Menu.png"))

    draw_beringin_big().save(os.path.join(OUT_DIR, "PohonBeringin_Besar.png"))
    draw_beringin_small().save(os.path.join(OUT_DIR, "PohonBeringin_Kecil.png"))
    draw_meru().save(os.path.join(OUT_DIR, "PuraMeru.png"))
    draw_bale_kulkul().save(os.path.join(OUT_DIR, "BaleKulkul.png"))
    draw_pelinggih().save(os.path.join(OUT_DIR, "Pelinggih.png"))
    draw_penjor().save(os.path.join(OUT_DIR, "Penjor.png"))

    print("Done.")


if __name__ == "__main__":
    main()
