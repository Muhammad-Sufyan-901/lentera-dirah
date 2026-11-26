#!/usr/bin/env python3
"""Penyempurnaan Tahap 2:
1. Menghilangkan kode-kode tersisa di Tabel 4.2, 7.3, dan 7.6 (lontarCount, OnTriggerEnter2D, Mathf.Sin, PlayOneShot, dll).
2. Memperbaiki tata letak halaman PDF agar rapi tanpa potongan baris terisolasi (orphan break).
3. Menyelaraskan teks DOCX agar identik.
"""

import os
from docx import Document

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.path.join(ROOT, "docs")
DOCX_PATH = os.path.join(BASE, "gdd", "230030309_Muhammad_Sufyan_Game_Design_Document_GDD_Lentera_Dirah.docx")
HTML_PATH = os.path.join(BASE, "html", "230030309_Muhammad_Sufyan_Game_Design_Document_GDD_Lentera_Dirah.html")


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


def update_html():
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    def swap(old, new, label):
        nonlocal html
        if old not in html:
            raise SystemExit(f"[HTML] Anchor gagal: {label}")
        html = html.replace(old, new, 1)

    # 1. Tabel 4.2 Trigger Victory & GameOver
    swap(
        "<td><code>lontarCount == 3</code> dan pemain menyentuh Altar.</td>",
        "<td>Ketiga naskah Lontar Suci pada level tersebut telah terkumpul dan Bahula menyentuh Altar.</td>",
        "4.2 Trigger Victory",
    )
    swap(
        "<td><code>playerHealth &lt;= 0</code> atau <code>lanternEnergy &lt;= 0</code>.</td>",
        "<td>Nyawa Bahula habis akibat sentuhan musuh atau energi lentera padam sepenuhnya (0%).</td>",
        "4.2 Trigger GameOver",
    )

    # 2. Tabel 7.3 Objek Interaktif
    swap(
        "Objek koleksi utama (<code>CollectibleItem.cs</code>), dilengkapi <code>Point Light 2D</code> kuning emas (<code>#FFB84D</code>) dan animasi mengambang sinusoidal (<code>Mathf.Sin</code>).",
        "Objek koleksi utama di setiap level yang memancarkan pendar cahaya keemasan (#FFB84D) dan melayang lembut secara berirama untuk menarik perhatian pemain.",
        "7.3 Lontar Suci",
    )
    swap(
        "Menambah energi cahaya lentera sebesar <code>+35%</code> saat disentuh pemain (<code>OnTriggerEnter2D</code>).",
        "Menambah energi cahaya lentera sebesar +35% saat disentuh atau dilewati oleh karakter Bahula.",
        "7.3 Guci Minyak",
    )
    swap(
        "Ditempatkan di pusat peta desa; saat <code>lontarCount == 3</code>, <code>Point Light 2D</code> menyala terang dan memicu kondisi <code>Victory</code>.",
        "Terletak di pusat setiap wilayah; begitu ketiga Lontar berhasil dikumpulkan, altar menyala terang benderang dengan pendar cahaya emas dan menyelesaikan level.",
        "7.3 Altar",
    )

    # 3. Tabel 7.6 Audio
    swap(
        '<th style="width: 46%;" bgcolor="#e8eef5">Pemicu Event pada Script C#</th>',
        '<th style="width: 46%;" bgcolor="#e8eef5">Fungsi dan Pemicu Audio dalam Permainan</th>',
        "7.6 Header Audio",
    )
    swap(
        "Diputar berulang sejak permainan dimulai.",
        "Alunan instrumen tradisional Bali Gendér Wayang (1928) yang diputar berulang untuk membangun atmosfer malam yang sakral dan misterius.",
        "7.6 BGM",
    )
    swap(
        "<td>Dipanggil via <code>PlayOneShot(&#8203;sfxLontar)</code> saat mengambil Lontar.</td>",
        "<td>Denting genta suci pendeta (Bajra) yang berbunyi secara instan saat Bahula berhasil mengambil naskah Lontar Suci.</td>",
        "7.6 SFX Lontar",
    )
    swap(
        "<td>Dipanggil saat menekan <code>Spacebar</code> untuk <i>Holy Light Burst</i>.</td>",
        "<td>Deru resonansi cahaya suci saat pemain menekan tombol Spasi untuk melumpuhkan roh bayangan di sekitarnya.</td>",
        "7.6 SFX Burst",
    )
    swap(
        "<td>Dipanggil saat mengambil Guci Minyak Obor.</td>",
        "<td>Suara percikan api obor yang menyala kembali saat Bahula mengambil guci Minyak Obor.</td>",
        "7.6 SFX Minyak",
    )
    swap(
        "<td>Dipanggil saat nyawa berkurang (<code>Hurt</code>) dan Altar disucikan (<code>Victory</code>).</td>",
        "<td>Efek suara benturan saat Bahula terluka akibat musuh, serta tabuhan gong kemenangan saat Altar suci berhasil dibersihkan.</td>",
        "7.6 SFX Hurt & Victory",
    )

    # 4. Tata Letak Cetak (Print CSS & Page Breaks)
    # Tambahkan style cetak agar tabel tidak terpotong canggung
    print_css_old = """      .page-break {
        border-top: none !important;
        margin: 0 !important;
        padding: 0 !important;
        page-break-before: always !important;
      }
    }"""
    print_css_new = """      .page-break {
        border-top: none !important;
        margin: 0 !important;
        padding: 0 !important;
        page-break-before: always !important;
      }
      table {
        page-break-inside: auto;
      }
      tr {
        page-break-inside: avoid;
        page-break-after: auto;
      }
      .wireframe-table {
        page-break-inside: avoid !important;
      }
      h1, h2, h3 {
        page-break-after: avoid;
      }
    }"""
    swap(print_css_old, print_css_new, "Print CSS rules")

    # Wireframe table class
    swap(
        """    <h2 class="section-title" id="gdd-6-3">6.3 Mockup Visual Wireframe HUD Gameplay</h2>
    <!-- Tabel HUD Wireframe yang Kompatibel 100% di Browser, Word, dan PDF -->
    <table style="width: 100%; border-collapse: collapse; border: 2.5pt solid #c99738; background-color: #121324; color: #ffffff; font-family: Arial, Helvetica, sans-serif; margin: 12pt 0;">""",
        """    <div class="page-break"></div>
    <h2 class="section-title" id="gdd-6-3">6.3 Mockup Visual Wireframe HUD Gameplay</h2>
    <!-- Tabel HUD Wireframe yang Kompatibel 100% di Browser, Word, dan PDF -->
    <table class="wireframe-table" style="width: 100%; border-collapse: collapse; border: 2.5pt solid #c99738; background-color: #121324; color: #ffffff; font-family: Arial, Helvetica, sans-serif; margin: 12pt 0; page-break-inside: avoid;">""",
        "Wireframe page break & class",
    )

    # Bab VIII Page Break
    swap(
        """    <h1 class="chapter-title" id="gdd-bab8" style="margin-top: 22pt;">BAB VIII<br>STRUKTUR PROJECT UNITY &amp; PETA JALAN PENGEMBANGAN FASE BERIKUTNYA</h1>""",
        """    <div class="page-break" id="gdd-bab8"></div>
    <h1 class="chapter-title">BAB VIII<br>STRUKTUR PROJECT UNITY &amp; PETA JALAN PENGEMBANGAN FASE BERIKUTNYA</h1>""",
        "Bab VIII page break",
    )

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print("[HTML] Tahap 2 OK")


def update_docx():
    doc = Document(DOCX_PATH)

    # 1. Tabel 8 (State Table)
    t8 = doc.tables[8]
    set_cell_text(t8.rows[6].cells[2], "Ketiga naskah Lontar Suci pada level tersebut telah terkumpul dan Bahula menyentuh Altar.")
    set_cell_text(t8.rows[7].cells[2], "Nyawa Bahula habis akibat sentuhan musuh atau energi lentera padam sepenuhnya (0%).")

    # 2. Tabel 16 (Tabel 7.3 Objek Interaktif)
    t16 = doc.tables[16]
    set_cell_text(t16.rows[1].cells[2], "Objek koleksi utama di setiap level yang memancarkan pendar cahaya keemasan (#FFB84D) dan melayang lembut secara berirama untuk menarik perhatian pemain.")
    set_cell_text(t16.rows[2].cells[2], "Menambah energi cahaya lentera sebesar +35% saat disentuh atau dilewati oleh karakter Bahula.")
    set_cell_text(t16.rows[3].cells[2], "Terletak di pusat setiap wilayah; begitu ketiga Lontar berhasil dikumpulkan, altar menyala terang benderang dengan pendar cahaya emas dan menyelesaikan level.")

    # 3. Tabel 19 (Tabel 7.6 Audio)
    t19 = doc.tables[19]
    set_cell_text(t19.rows[0].cells[2], "Fungsi dan Pemicu Audio dalam Permainan")
    set_cell_text(t19.rows[1].cells[2], "Alunan instrumen tradisional Bali Gendér Wayang (1928) yang diputar berulang untuk membangun atmosfer malam yang sakral dan misterius.")
    set_cell_text(t19.rows[2].cells[2], "Denting genta suci pendeta (Bajra) yang berbunyi secara instan saat Bahula berhasil mengambil naskah Lontar Suci.")
    set_cell_text(t19.rows[3].cells[2], "Deru resonansi cahaya suci saat pemain menekan tombol Spasi untuk melumpuhkan roh bayangan di sekitarnya.")
    set_cell_text(t19.rows[4].cells[2], "Suara percikan api obor yang menyala kembali saat Bahula mengambil guci Minyak Obor.")
    set_cell_text(t19.rows[5].cells[2], "Efek suara benturan saat Bahula terluka akibat musuh, serta tabuhan gong kemenangan saat Altar suci berhasil dibersihkan.")

    doc.save(DOCX_PATH)
    print("[DOCX] Tahap 2 OK")


if __name__ == "__main__":
    update_html()
    update_docx()
