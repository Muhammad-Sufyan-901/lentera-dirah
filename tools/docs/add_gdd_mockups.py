#!/usr/bin/env python3
"""Menambahkan mockup visual Menu Utama dan Layar Penyelesaian ke Bab VI GDD
(HTML + DOCX) menggunakan tangkapan layar hasil build final."""

import base64
import copy
import os

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.shared import Cm, Pt

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.path.join(ROOT, "docs")

DOCX_PATH = os.path.join(BASE, "gdd", "230030309_Muhammad_Sufyan_Game_Design_Document_GDD_Lentera_Dirah.docx")
HTML_PATH = os.path.join(BASE, "html", "230030309_Muhammad_Sufyan_Game_Design_Document_GDD_Lentera_Dirah.html")
MENU_IMG = os.path.join(ROOT, "Game", "Docs", "preview_menu.png")
RESULT_IMG = os.path.join(ROOT, "Game", "Docs", "preview_victory3.png")

SECTION_ID = "gdd-6-4"
SECTION_TITLE = "6.4 Mockup Visual Menu Utama dan Layar Penyelesaian"


def data_uri(path):
    with open(path, "rb") as handle:
        encoded = base64.b64encode(handle.read()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def set_cell_text(cell, text):
    paragraph = cell.paragraphs[0]
    template = paragraph.runs[0] if paragraph.runs else None
    bold = template.bold if template is not None else None
    size = template.font.size if template is not None else None
    name = template.font.name if template is not None else None
    for child in list(paragraph._p):
        if child.tag.endswith("}pPr"):
            continue
        paragraph._p.remove(child)
    run = paragraph.add_run(text)
    run.bold = bold
    if size is not None:
        run.font.size = size
    if name is not None:
        run.font.name = name
    for extra in cell.paragraphs[1:]:
        extra._element.getparent().remove(extra._element)


def apply_html():
    with open(HTML_PATH, encoding="utf-8") as handle:
        html = handle.read()

    if SECTION_ID in html:
        raise SystemExit("[HTML] Bagian 6.4 sudah ada")

    # TOC
    anchor_toc = '<tr><td class="toc-sub"><a href="#gdd-6-3">6.3 Mockup Visual Wireframe HUD Gameplay</a></td></tr>'
    if anchor_toc not in html:
        raise SystemExit("[HTML] Baris TOC 6.3 tidak ditemukan")
    html = html.replace(
        anchor_toc,
        anchor_toc + '\n      <tr><td class="toc-sub"><a href="#gdd-6-4">6.4 Mockup Visual Menu Utama dan Layar Penyelesaian</a></td></tr>',
        1,
    )

    menu_uri = data_uri(MENU_IMG)
    result_uri = data_uri(RESULT_IMG)

    section = f"""    <!-- ==================== BAB VII & VIII: ASSET REFERENCES & ROADMAP ==================== -->
    <div class="page-break"></div>
    <h2 class="section-title" id="{SECTION_ID}">{SECTION_TITLE}</h2>
    <p>
      Selain wireframe HUD, dokumentasi desain antarmuka juga dilengkapi mockup visual hasil implementasi build final.
      Dua layar di bawah ini menjadi titik masuk dan titik penutup pengalaman pemain: <b>Menu Utama</b> sebagai pusat navigasi,
      serta <b>Layar Penyelesaian</b> sebagai rekapitulasi perjalanan tiga level.
    </p>

    <div style="margin: 14pt 0 8pt 0; text-align: center;">
      <img src="{menu_uri}" alt="Mockup Menu Utama Lentera Dirah"
           style="width: 100%; max-width: 16cm; border: 2pt solid #c99738; border-radius: 4pt;">
      <p style="margin: 5pt 0 0 0; text-align: center; font-size: 10pt; font-style: italic; color: #444444;">
        Gambar 6.2. Mockup Menu Utama — latar gapura candi bentar, pohon beringin, dan penjor.
      </p>
    </div>

    <table class="data-table">
      <thead>
        <tr>
          <th style="width: 24%;" bgcolor="#e8eef5">Elemen Menu Utama</th>
          <th style="width: 76%;" bgcolor="#e8eef5">Fungsi</th>
        </tr>
      </thead>
      <tbody>
        <tr><td><b>MULAI BERMAIN</b></td><td>Membuka halaman Pilih Kesulitan (Mudah / Normal / Sulit) sebelum memasuki Level 1.</td></tr>
        <tr><td><b>CARA BERMAIN</b></td><td>Menampilkan panduan tujuan, kontrol, energi lentera, mekanik Rwa Bhineda, kesulitan, dan tips.</td></tr>
        <tr><td><b>PENGATURAN</b></td><td>Mengatur volume BGM/SFX dan mode layar penuh.</td></tr>
        <tr><td><b>KREDIT</b></td><td>Menampilkan atribusi aset, lisensi, dan ucapan terima kasih.</td></tr>
        <tr><td><b>KELUAR</b></td><td>Menutup aplikasi permainan.</td></tr>
      </tbody>
    </table>

    <div style="margin: 16pt 0 8pt 0; text-align: center;">
      <img src="{result_uri}" alt="Mockup Layar Penyelesaian Lentera Dirah"
           style="width: 100%; max-width: 16cm; border: 2pt solid #c99738; border-radius: 4pt;">
      <p style="margin: 5pt 0 0 0; text-align: center; font-size: 10pt; font-style: italic; color: #444444;">
        Gambar 6.3. Mockup Layar Penyelesaian — skor total, gelar, rekor, dan tombol Selesai.
      </p>
    </div>

    <table class="data-table">
      <thead>
        <tr>
          <th style="width: 24%;" bgcolor="#e8eef5">Elemen Layar Penyelesaian</th>
          <th style="width: 76%;" bgcolor="#e8eef5">Fungsi</th>
        </tr>
      </thead>
      <tbody>
        <tr><td><b>Judul Hasil</b></td><td>Menampilkan "LEVEL n SELESAI" untuk level 1–2 dan "SEMUA LEVEL SELESAI" setelah level 3.</td></tr>
        <tr><td><b>Skor Level &amp; Skor Total</b></td><td>Merinci perolehan skor level aktif dan akumulasi seluruh level.</td></tr>
        <tr><td><b>Gelar</b></td><td>Penyuci Agung, Murid Teladan, atau Pejalan Malam berdasarkan waktu dan sisa nyawa.</td></tr>
        <tr><td><b>Rekor Skor</b></td><td>Menampilkan rekor terbaik yang tersimpan di <code>PlayerPrefs</code> setelah level 3.</td></tr>
        <tr><td><b>SELESAI / LEVEL BERIKUTNYA</b></td><td>Lanjut ke level berikutnya (level 1–2) atau kembali ke Menu Utama (level 3).</td></tr>
        <tr><td><b>MENU UTAMA</b></td><td>Keluar dari hasil level dan kembali ke Menu Utama kapan saja.</td></tr>
      </tbody>
    </table>

"""

    anchor = "    <!-- ==================== BAB VII & VIII: ASSET REFERENCES & ROADMAP ==================== -->"
    if anchor not in html:
        raise SystemExit("[HTML] Anchor Bab VII tidak ditemukan")
    html = html.replace(anchor, section, 1)

    with open(HTML_PATH, "w", encoding="utf-8") as handle:
        handle.write(html)
    print("[HTML] Mockup 6.4 ditambahkan")


def apply_docx():
    doc = Document(DOCX_PATH)

    # Cegah duplikasi
    for paragraph in doc.paragraphs:
        if paragraph.text.strip().startswith("6.4 Mockup Visual"):
            raise SystemExit("[DOCX] Bagian 6.4 sudah ada")

    # TOC: salin baris 6.3
    toc = doc.tables[1]
    for index, row in enumerate(toc.rows):
        if "6.3 Mockup Visual Wireframe" in row.cells[0].text:
            new_tr = copy.deepcopy(row._tr)
            row._tr.addnext(new_tr)
            new_row = toc.rows[index + 1]
            set_cell_text(new_row.cells[0], SECTION_TITLE)
            break

    # Anchor: tabel wireframe (T13)
    anchor = doc.tables[13]._tbl

    def insert_paragraph(text="", style=None, bold_lead=None, italic=False, align=None, page_break=False):
        nonlocal anchor
        paragraph = doc.add_paragraph(style=style) if style else doc.add_paragraph()
        if page_break:
            paragraph.add_run().add_break(WD_BREAK.PAGE)
        if bold_lead:
            run = paragraph.add_run(bold_lead)
            run.bold = True
            run.font.size = Pt(12)
        if text:
            run = paragraph.add_run(text)
            run.font.size = Pt(12)
            run.italic = italic
        if align is not None:
            paragraph.alignment = align
        anchor.addnext(paragraph._p)
        anchor = paragraph._p

    def insert_picture(path):
        nonlocal anchor
        doc.add_picture(path, width=Cm(15.4))
        paragraph = doc.paragraphs[-1]
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        anchor.addnext(paragraph._p)
        anchor = paragraph._p

    insert_paragraph(page_break=True)
    insert_paragraph(SECTION_TITLE, style="Heading 2")
    insert_paragraph(
        "Selain wireframe HUD, dokumentasi desain antarmuka juga dilengkapi mockup visual hasil implementasi build final. "
        "Dua layar di bawah ini menjadi titik masuk dan titik penutup pengalaman pemain: Menu Utama sebagai pusat navigasi, "
        "serta Layar Penyelesaian sebagai rekapitulasi perjalanan tiga level."
    )

    insert_picture(MENU_IMG)
    insert_paragraph("Gambar 6.2. Mockup Menu Utama — latar gapura candi bentar, pohon beringin, dan penjor.",
                     italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    insert_paragraph("Menu Utama menyediakan lima tombol: MULAI BERMAIN (membuka halaman Pilih Kesulitan), CARA BERMAIN "
                     "(panduan tujuan, kontrol, energi, mekanik Rwa Bhineda, kesulitan, dan tips), PENGATURAN (volume BGM/SFX "
                     "dan layar penuh), KREDIT (atribusi aset dan lisensi), serta KELUAR.")

    insert_picture(RESULT_IMG)
    insert_paragraph("Gambar 6.3. Mockup Layar Penyelesaian — skor total, gelar, rekor, dan tombol Selesai.",
                     italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    insert_paragraph("Layar Penyelesaian menampilkan judul hasil (LEVEL n SELESAI atau SEMUA LEVEL SELESAI), skor level dan "
                     "skor total, gelar (Penyuci Agung / Murid Teladan / Pejalan Malam), rekor skor, serta tombol LEVEL BERIKUTNYA "
                     "atau SELESAI dan MENU UTAMA.")

    doc.save(DOCX_PATH)
    print("[DOCX] Mockup 6.4 ditambahkan")


if __name__ == "__main__":
    apply_html()
    apply_docx()
