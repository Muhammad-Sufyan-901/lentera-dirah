#!/usr/bin/env python3
"""GDD §6.2: document the three main-menu buttons (Mulai, Cara Bermain, Keluar)."""

import os

from docx import Document
from docx.oxml.ns import qn

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCX_PATH = os.path.join(BASE, "GDD", "230030309_Muhammad_Sufyan_Game_Design_Document_GDD_Lentera_Dirah.docx")
HTML_PATH = os.path.join(BASE, "HTML Artifacts", "230030309_Muhammad_Sufyan_Game_Design_Document_GDD_Lentera_Dirah.html")

MENU_PARAGRAPH = """    <p>
      Layar Main Menu menyediakan tiga tombol: <b>MULAI PENYUCIAN</b> untuk memulai alur permainan,
      <b>CARA BERMAIN</b> untuk membuka panel panduan (tujuan, kontrol, energi lentera, Bayangan Wabah, dan tips)
      yang dapat ditutup dengan tombol <b>KEMBALI</b> atau tombol <code>Esc</code>, serta
      <b>KELUAR</b> untuk menutup aplikasi.
    </p>

"""

MENU_PARAGRAPH_PLAIN = (
    "Layar Main Menu menyediakan tiga tombol: MULAI PENYUCIAN untuk memulai alur permainan, "
    "CARA BERMAIN untuk membuka panel panduan (tujuan, kontrol, energi lentera, Bayangan Wabah, dan tips) "
    "yang dapat ditutup dengan tombol KEMBALI atau tombol Esc, serta KELUAR untuk menutup aplikasi."
)

HTML_REPLACEMENTS = [
    (
        '<span style="font-size: 9pt;">Klik tombol <i>&ldquo;Mulai Penyucian&rdquo;</i></span>',
        '<span style="font-size: 9pt;">Pilih <i>&ldquo;Mulai Penyucian&rdquo;</i>, <i>&ldquo;Cara Bermain&rdquo;</i>, atau <i>&ldquo;Keluar&rdquo;</i></span>',
    ),
]

OLD_NODE_TEXT = "Klik tombol \u201cMulai Penyucian\u201d"
NEW_NODE_TEXT = "Pilih \u201cMulai Penyucian\u201d, \u201cCara Bermain\u201d, atau \u201cKeluar\u201d"


def walk_paragraphs(container):
    for paragraph in container.paragraphs:
        yield paragraph
    for table in container.tables:
        for row in table.rows:
            for cell in row.cells:
                yield from walk_paragraphs(cell)


def replace_text(paragraph, old, new):
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


def find_heading(document, prefix):
    for paragraph in document.paragraphs:
        if paragraph.text.strip().startswith(prefix):
            return paragraph
    raise SystemExit(f"Heading tidak ditemukan: {prefix!r}")


def update_html():
    with open(HTML_PATH, encoding="utf-8") as handle:
        text = handle.read()

    for old, new in HTML_REPLACEMENTS:
        count = text.count(old)
        if count != 1:
            raise SystemExit(f"HTML anchor {count}x: {old[:80]!r}")
        text = text.replace(old, new)

    anchor = '    <h2 class="section-title" id="gdd-6-3">6.3 Mockup Visual Wireframe HUD Gameplay</h2>'
    if text.count(anchor) != 1:
        raise SystemExit("Anchor 6.3 tidak unik")
    text = text.replace(anchor, MENU_PARAGRAPH + anchor)

    with open(HTML_PATH, "w", encoding="utf-8") as handle:
        handle.write(text)

    print("HTML updated (§6.2)")


def update_docx():
    document = Document(DOCX_PATH)
    paragraphs = list(walk_paragraphs(document))

    changed = 0
    for paragraph in paragraphs:
        if OLD_NODE_TEXT in paragraph.text and replace_text(paragraph, OLD_NODE_TEXT, NEW_NODE_TEXT):
            changed += 1

    if changed != 1:
        raise SystemExit(f"Teks diagram: {changed} penggantian (harus 1)")

    heading = find_heading(document, "6.3 Mockup Visual Wireframe HUD Gameplay")
    body_style = next(
        (p.style for p in document.paragraphs if "Sesuai teori perancangan" in p.text),
        None,
    )

    inserted = heading.insert_paragraph_before()
    if body_style is not None:
        inserted.style = body_style
    inserted.add_run(MENU_PARAGRAPH_PLAIN)

    document.save(DOCX_PATH)
    print("DOCX updated (§6.2)")


if __name__ == "__main__":
    update_html()
    update_docx()
    print("Done.")
