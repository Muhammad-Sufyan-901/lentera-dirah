#!/usr/bin/env python3
"""Mengganti mockup 6.4 dengan versi wireframe bergaya panel HUD (§6.3)."""

import base64
import os
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.path.join(ROOT, "docs")
DOCX_PATH = os.path.join(BASE, "gdd", "230030309_Muhammad_Sufyan_Game_Design_Document_GDD_Lentera_Dirah.docx")
HTML_PATH = os.path.join(BASE, "html", "230030309_Muhammad_Sufyan_Game_Design_Document_GDD_Lentera_Dirah.html")
MENU_IMG = os.path.join(ROOT, "Game", "Docs", "mockup_menu.png")
RESULT_IMG = os.path.join(ROOT, "Game", "Docs", "mockup_result.png")

INTRO = ("Mockup berikut disusun dengan gaya wireframe yang sama seperti panel HUD pada §6.3: latar "
         "<b>Dirah Midnight</b>, bingkai emas, panel garis putus-putus, serta label antarmuka berwarna emas dan cyan. "
         "Menu Utama menjadi titik masuk, sedangkan Layar Penyelesaian menjadi rekapitulasi perjalanan tiga level.")

INTRO_DOCX = ("Mockup berikut disusun dengan gaya wireframe yang sama seperti panel HUD pada §6.3: latar Dirah Midnight, "
              "bingkai emas, panel garis putus-putus, serta label antarmuka berwarna emas dan cyan. Menu Utama menjadi titik "
              "masuk, sedangkan Layar Penyelesaian menjadi rekapitulasi perjalanan tiga level.")


def data_uri(path):
    with open(path, "rb") as handle:
        return "data:image/png;base64," + base64.b64encode(handle.read()).decode("ascii")


def build_html_section():
    menu_uri = data_uri(MENU_IMG)
    result_uri = data_uri(RESULT_IMG)

    return f"""    <!-- ==================== BAB VII & VIII: ASSET REFERENCES & ROADMAP ==================== -->
    <div class="page-break"></div>
    <h2 class="section-title" id="gdd-6-4">6.4 Mockup Visual Menu Utama dan Layar Penyelesaian</h2>
    <p>{INTRO}</p>

    <div style="margin: 14pt 0 8pt 0; text-align: center;">
      <img src="{menu_uri}" alt="Mockup wireframe Menu Utama Lentera Dirah"
           style="width: 100%; max-width: 16cm; border: 2pt solid #c99738; border-radius: 4pt;">
      <p style="margin: 5pt 0 0 0; text-align: center; font-size: 10pt; font-style: italic; color: #444444;">
        Gambar 6.2. Mockup wireframe Menu Utama — konsisten dengan panel HUD pada §6.3.
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
      <img src="{result_uri}" alt="Mockup wireframe Layar Penyelesaian Lentera Dirah"
           style="width: 100%; max-width: 16cm; border: 2pt solid #c99738; border-radius: 4pt;">
      <p style="margin: 5pt 0 0 0; text-align: center; font-size: 10pt; font-style: italic; color: #444444;">
        Gambar 6.3. Mockup wireframe Layar Penyelesaian — skor total, gelar, rekor, dan tombol Selesai.
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


def replace_html():
    with open(HTML_PATH, encoding="utf-8") as handle:
        html = handle.read()

    h2 = html.find('<h2 class="section-title" id="gdd-6-4">')
    start = html.rfind("    <!-- ==================== BAB VII & VIII: ASSET REFERENCES & ROADMAP ==================== -->", 0, h2)
    end = html.find('<div class="page-break" id="gdd-bab7"></div>', h2)

    if h2 == -1 or start == -1 or end == -1:
        raise SystemExit("[HTML] Section 6.4 atau anchor Bab VII tidak ditemukan")

    html = html[:start] + build_html_section() + html[end:]

    with open(HTML_PATH, "w", encoding="utf-8") as handle:
        handle.write(html)
    print("[HTML] Mockup wireframe diterapkan")


def replace_docx():
    doc = Document(DOCX_PATH)

    section_index = None
    for index, paragraph in enumerate(doc.paragraphs):
        if paragraph.text.strip().startswith("6.4 Mockup Visual"):
            section_index = index
            break

    if section_index is None:
        raise SystemExit("[DOCX] Heading 6.4 tidak ditemukan")

    image_paragraphs = []
    intro_paragraph = None
    captions = []

    for paragraph in doc.paragraphs[section_index + 1:]:
        if paragraph.text.strip().startswith("BAB VII"):
            break
        if paragraph._p.xpath(".//w:drawing"):
            image_paragraphs.append(paragraph)
        elif paragraph.text.startswith("Selain wireframe") or paragraph.text.startswith("Mockup berikut"):
            intro_paragraph = paragraph
        elif paragraph.text.startswith("Gambar 6.2") or paragraph.text.startswith("Gambar 6.3"):
            captions.append(paragraph)

    if len(image_paragraphs) != 2:
        raise SystemExit(f"[DOCX] Jumlah gambar 6.4 tidak sesuai: {len(image_paragraphs)}")

    if intro_paragraph is not None:
        for child in list(intro_paragraph._p):
            if child.tag.endswith("}pPr"):
                continue
            intro_paragraph._p.remove(child)
        intro_paragraph.add_run(INTRO_DOCX)

    for paragraph, path in zip(image_paragraphs, [MENU_IMG, RESULT_IMG]):
        for child in list(paragraph._p):
            if child.tag.endswith("}pPr"):
                continue
            paragraph._p.remove(child)
        run = paragraph.add_run()
        run.add_picture(path, width=Cm(15.4))
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    if len(captions) >= 2:
        for paragraph, text in zip(captions, [
            "Gambar 6.2. Mockup wireframe Menu Utama — konsisten dengan panel HUD pada §6.3.",
            "Gambar 6.3. Mockup wireframe Layar Penyelesaian — skor total, gelar, rekor, dan tombol Selesai.",
        ]):
            for child in list(paragraph._p):
                if child.tag.endswith("}pPr"):
                    continue
                paragraph._p.remove(child)
            run = paragraph.add_run(text)
            run.italic = True
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.save(DOCX_PATH)
    print("[DOCX] Mockup wireframe diterapkan")


if __name__ == "__main__":
    replace_html()
    replace_docx()
