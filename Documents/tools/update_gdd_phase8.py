#!/usr/bin/env python3
"""BAB VIII: replace the UAS roadmap framing with the next-phase roadmap.

Only Bab VIII (and its table-of-contents entry) is touched; mechanics,
assets, and other chapters stay as they are.
"""

import os
import sys

from docx import Document
from docx.oxml.ns import qn

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))

BASE = os.path.dirname(TOOLS_DIR)
DOCX_PATH = os.path.join(BASE, "GDD", "230030309_Muhammad_Sufyan_Game_Design_Document_GDD_Lentera_Dirah.docx")
HTML_PATH = os.path.join(BASE, "HTML Artifacts", "230030309_Muhammad_Sufyan_Game_Design_Document_GDD_Lentera_Dirah.html")

OLD_CHAPTER = "PENGEMBANGAN UAS"
NEW_CHAPTER = "PENGEMBANGAN FASE BERIKUTNYA"

# (old, new, minimum number of replacements expected)
TEXT_REPLACEMENTS = [
    (
        "8.2 Peta Jalan Ekspansi Menuju Proyek Akhir (UAS)",
        "8.2 Peta Jalan Ekspansi Menuju Fase Berikutnya",
        1,
    ),
    (
        "Prototipe Tugas 1 ini dirancang agar dapat langsung dikembangkan menjadi Proyek Akhir (UAS) tanpa membangun ulang dari awal, melalui tahapan ekspansi berikut:",
        "Prototipe ini dirancang agar dapat langsung dikembangkan ke fase berikutnya tanpa membangun ulang dari awal, melalui tahapan ekspansi berikut:",
        1,
    ),
    (
        "Level 1 (Desa Girah Bagian Luar — Prototipe Tugas 1)",
        "Level 1 (Desa Girah Bagian Luar — prototipe saat ini)",
        1,
    ),
    (
        "Implementasi Fitur Wajib UAS:",
        "Implementasi Fitur Lanjutan:",
        1,
    ),
]

# HTML uses typographic markup, so it gets its own exact anchors.
HTML_REPLACEMENTS = [
    (
        "8. BAB VIII: STRUKTUR PROJECT UNITY &amp; PETA JALAN PENGEMBANGAN UAS",
        "8. BAB VIII: STRUKTUR PROJECT UNITY &amp; PETA JALAN PENGEMBANGAN FASE BERIKUTNYA",
        1,
    ),
    (
        "BAB VIII<br>STRUKTUR PROJECT UNITY &amp; PETA JALAN PENGEMBANGAN UAS",
        "BAB VIII<br>STRUKTUR PROJECT UNITY &amp; PETA JALAN PENGEMBANGAN FASE BERIKUTNYA",
        1,
    ),
    (
        '<h2 class="section-title">8.2 Peta Jalan Ekspansi Menuju Proyek Akhir (UAS)</h2>',
        '<h2 class="section-title">8.2 Peta Jalan Ekspansi Menuju Fase Berikutnya</h2>',
        1,
    ),
    (
        "Prototipe Tugas 1 ini dirancang agar dapat langsung dikembangkan menjadi Proyek Akhir (UAS) tanpa membangun ulang dari awal, melalui tahapan ekspansi berikut:",
        "Prototipe ini dirancang agar dapat langsung dikembangkan ke fase berikutnya tanpa membangun ulang dari awal, melalui tahapan ekspansi berikut:",
        1,
    ),
    (
        "Level 1 (<i>Desa Girah Bagian Luar</i> &mdash; Prototipe Tugas 1)",
        "Level 1 (<i>Desa Girah Bagian Luar</i> &mdash; prototipe saat ini)",
        1,
    ),
    (
        "<li><b>Implementasi Fitur Wajib UAS:</b>",
        "<li><b>Implementasi Fitur Lanjutan:</b>",
        1,
    ),
]


def all_paragraphs(document):
    for paragraph in document.paragraphs:
        yield paragraph
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    yield paragraph


def replace_text(paragraph, old, new):
    """Replace text across every w:t node, including runs inside hyperlinks."""
    nodes = paragraph._p.findall(".//" + qn("w:t"))
    texts = [node.text or "" for node in nodes]
    full = "".join(texts)
    index = full.find(old)

    if index == -1:
        return False

    end = index + len(old)
    cursor = 0
    inserted = False

    for node, text in zip(nodes, texts):
        start = cursor
        stop = cursor + len(text)
        cursor = stop

        if stop <= index or start >= end:
            continue

        local_start = max(index, start) - start
        local_end = min(end, stop) - start

        if not inserted:
            node.text = text[:local_start] + new + text[local_end:]
            inserted = True
        else:
            node.text = text[:local_start] + text[local_end:]

    return inserted


def update_docx():
    document = Document(DOCX_PATH)
    paragraphs = list(all_paragraphs(document))

    if OLD_CHAPTER not in "".join(paragraph.text for paragraph in paragraphs):
        print("DOCX already updated (BAB VIII)")
        return

    chapter_changes = 0
    for paragraph in paragraphs:
        if OLD_CHAPTER in paragraph.text and replace_text(paragraph, OLD_CHAPTER, NEW_CHAPTER):
            chapter_changes += 1

    if chapter_changes != 2:
        raise SystemExit(f"Judul bab: {chapter_changes} penggantian (harus 2: TOC + heading)")

    for old, new, expected in TEXT_REPLACEMENTS:
        changes = 0
        for paragraph in paragraphs:
            if old in paragraph.text and replace_text(paragraph, old, new):
                changes += 1
        if changes < expected:
            raise SystemExit(f"Gagal mengganti ({changes}/{expected}): {old[:70]!r}")

    document.save(DOCX_PATH)
    print("DOCX updated (BAB VIII)")


def update_html():
    with open(HTML_PATH, encoding="utf-8") as handle:
        text = handle.read()

    if OLD_CHAPTER not in text:
        print("HTML already updated (BAB VIII)")
        return

    for old, new, expected in HTML_REPLACEMENTS:
        count = text.count(old)
        if count != expected:
            raise SystemExit(f"HTML anchor {count}x (harus {expected}): {old[:80]!r}")
        text = text.replace(old, new)

    with open(HTML_PATH, "w", encoding="utf-8") as handle:
        handle.write(text)

    print(f"HTML updated (BAB VIII): {len(HTML_REPLACEMENTS)} anchors")


if __name__ == "__main__":
    update_html()
    update_docx()
    print("Done.")
