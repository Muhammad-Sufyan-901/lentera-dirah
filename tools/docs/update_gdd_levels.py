#!/usr/bin/env python3
"""Sinkronisasi GDD final: tiga level, halaman kesulitan, skor, dan alur hasil."""

import copy
import os

from docx import Document
from docx.text.paragraph import Paragraph

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.path.join(ROOT, "docs")
DOCX_PATH = os.path.join(BASE, "gdd", "230030309_Muhammad_Sufyan_Game_Design_Document_GDD_Lentera_Dirah.docx")
HTML_PATH = os.path.join(BASE, "html", "230030309_Muhammad_Sufyan_Game_Design_Document_GDD_Lentera_Dirah.html")

LEVEL_TABLE = """    <p><b>Struktur Tiga Level.</b> Permainan terdiri atas tiga level dengan peta, altar, tiga Lontar, tiga Minyak Obor, dan jumlah musuh yang berbeda. Level diaktifkan oleh <code>LevelManager</code>; saat level dimuat, posisi pemain, energi, nyawa, musuh, item, dan altar direset.</p>
    <table class="data-table">
      <thead>
        <tr>
          <th style="width: 10%;" bgcolor="#e8eef5">Level</th>
          <th style="width: 30%;" bgcolor="#e8eef5">Peta</th>
          <th style="width: 14%;" bgcolor="#e8eef5">Musuh</th>
          <th style="width: 46%;" bgcolor="#e8eef5">Objektif</th>
        </tr>
      </thead>
      <tbody>
        <tr><td><b>1</b></td><td>Desa Girah Bagian Luar</td><td>3</td><td>3 Lontar di sektor utara, barat, dan timur desa; altar di alun-alun.</td></tr>
        <tr><td><b>2</b></td><td>Hutan Bambu Lemah Tulis</td><td>4</td><td>3 Lontar di clearing utara, barat, dan timur; lorong bambu sempit.</td></tr>
        <tr><td><b>3</b></td><td>Pelataran Setra Gandamayu</td><td>5</td><td>3 Lontar di pura utara serta sayap barat dan timur; plaza dan pelinggih.</td></tr>
      </tbody>
    </table>

"""


def replace_in_paragraph(paragraph, old, new):
    if old not in paragraph.text:
        return False
    runs = paragraph.runs
    full = "".join(run.text for run in runs)
    index = full.find(old)
    if index == -1:
        return False
    end_target = index + len(old)
    cursor = 0
    inserted = False
    for run in runs:
        start = cursor
        stop = cursor + len(run.text)
        cursor = stop
        if stop <= index or start >= end_target:
            continue
        local_start = max(index, start) - start
        local_end = min(end_target, stop) - start
        if not inserted:
            run.text = run.text[:local_start] + new + run.text[local_end:]
            inserted = True
        else:
            run.text = run.text[:local_start] + run.text[local_end:]
    return inserted


def set_paragraph_text(paragraph, text):
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


def insert_rich_after(anchor, template, parts):
    new_p = copy.deepcopy(template._p)
    anchor._p.addnext(new_p)
    paragraph = Paragraph(new_p, anchor._parent)
    for child in list(paragraph._p):
        if child.tag.endswith("}pPr"):
            continue
        paragraph._p.remove(child)
    base = template.runs[0] if template.runs else None
    for text, bold in parts:
        run = paragraph.add_run(text)
        run.bold = bold
        if base is not None:
            if base.font.size is not None:
                run.font.size = base.font.size
            if base.font.name is not None:
                run.font.name = base.font.name
    return paragraph


def apply_html():
    with open(HTML_PATH, encoding="utf-8") as handle:
        html = handle.read()

    def swap(old, new, label):
        nonlocal html
        if old not in html:
            raise SystemExit(f"[HTML] anchor tidak ditemukan: {label}")
        html = html.replace(old, new, 1)

    swap(
        "Versi final prototipe (Tugas 3) menambahkan menu <b>Pengaturan &amp; Jeda</b>, layar <b>Kredit</b>, <b>tiga tingkat kesulitan</b>, mekanik <b>Rwa Bhineda Exposure</b>, serta hasil akhir dengan <b>gelar</b> dan <b>rekor waktu</b>. <i>Save</i> progres tidak diimplementasikan karena sesi permainan singkat; persistensi dibatasi pada pengaturan, kesulitan, dan rekor.",
        "Versi final prototipe menambahkan <b>tiga level</b> (dua peta baru), <b>halaman Pilih Kesulitan</b> setelah tombol Mulai Bermain, mekanik <b>Rwa Bhineda Exposure</b>, serta <b>skor, gelar, dan rekor</b> pada halaman hasil tiap level. <i>Save</i> progres tidak diimplementasikan karena permainan dapat diselesaikan dalam beberapa menit; persistensi dibatasi pada pengaturan dan rekor skor.",
        "1.2 ringkasan",
    )

    swap(
        "Pada awal permainan, Altar Penyucian yang terletak di pusat Desa Girah diselimuti segel kabut gelap. Pemain harus menjelajahi tiga sektor desa (Sektor Utara, Sektor Timur, dan Sektor Barat) untuk mengumpulkan 3 naskah Lontar Suci. Setiap Lontar yang diambil akan menyalakan indikator lontar pada HUD dan membuka kutipan kearifan lokal. Begitu ketiga Lontar terkumpul, segel Altar terbuka secara otomatis dan memancarkan cahaya emas sebagai penanda titik penyelesaian misi.",
        "Di setiap level, Altar Penyucian dikelilingi segel kabut gelap. Pemain menjelajahi peta level untuk mengumpulkan 3 naskah Lontar Suci; setiap Lontar menyalakan indikator HUD dan membuka kutipan kearifan lokal. Begitu ketiga Lontar terkumpul, segel Altar terbuka dan memancarkan cahaya emas. Menyentuh Altar menyelesaikan level dan membuka halaman hasil dengan skor serta opsi lanjut ke level berikutnya atau kembali ke menu utama.",
        "3.3 mekanik 1",
    )

    swap(
        "<p><b>Tingkat Kesulitan.</b> Tiga pilihan kesulitan mengubah laju energi, kecepatan, dan kepekaan Bayangan Wabah. Nilai dipilih di panel PENGATURAN, disimpan di <code>PlayerPrefs</code>, dan diterapkan saat misi dimulai (saat dialog pembuka ditutup).</p>",
        "<p><b>Tingkat Kesulitan.</b> Tiga pilihan kesulitan mengubah laju energi, kecepatan, dan kepekaan Bayangan Wabah. Nilai dipilih pada halaman <b>PILIH KESULITAN</b> setelah tombol Mulai Bermain, disimpan di <code>PlayerPrefs</code>, dan diterapkan ke ketiga level.</p>",
        "3.3 kesulitan",
    )

    old_results = "<p><b>Hasil Akhir, Gelar, dan Rekor.</b> Saat Victory, <code>GameManager</code> mencatat waktu tempuh, nyawa, dan sisa energi lentera. Gelar dihitung dari waktu dan nyawa; waktu terbaik disimpan di <code>PlayerPrefs</code> dan ditampilkan sebagai rekor. Save progres permainan tidak diimplementasikan karena sesi dapat diselesaikan dalam hitungan menit.</p>"
    new_results = LEVEL_TABLE + """    <p><b>Skor, Gelar, dan Rekor.</b> Saat level selesai, <code>GameManager</code> menghitung <code>skor level = (500 + bonus waktu + nyawa x 100 + sisa energi x 2) x pengali kesulitan</code>. Bonus waktu dimulai dari 600 dan berkurang 5 per detik. Skor total adalah akumulasi ketiga level; rekor skor disimpan di <code>PlayerPrefs</code> setelah level 3. Gelar level dihitung dari waktu dan nyawa: <b>Penyuci Agung</b> (waktu &le; 2:30 dan nyawa 3/3), <b>Murid Teladan</b> (waktu &le; 4:00 dan nyawa &ge; 2/3), atau <b>Pejalan Malam</b>.</p>"""
    swap(old_results, new_results, "3.3 hasil")

    swap(
        "<code>MainMenu</code> &rarr; <code>IntroDialog</code> &rarr; <code>Playing</code> &harr; <code>Paused</code> &rarr; (<code>Victory</code> / <code>GameOver</code>)",
        "<code>MainMenu</code> &rarr; <code>DifficultySelect</code> &rarr; <code>IntroDialog</code> &rarr; <code>Playing</code> &harr; <code>Paused</code> &rarr; (<code>Victory</code> / <code>GameOver</code>)",
        "FSM diagram",
    )

    swap(
        '<td rowspan="6"><b>Game Manager</b><br>(<code>GameManager.cs</code>)</td>',
        '<td rowspan="7"><b>Game Manager</b><br>(<code>GameManager.cs</code>)</td>',
        "rowspan",
    )
    swap(
        """          <td><code>MainMenu</code></td>
          <td>Kondisi awal saat scene dimuat.</td>
          <td>Menampilkan panel judul utama; input karakter dinonaktifkan.</td>
        </tr>""",
        """          <td><code>MainMenu</code></td>
          <td>Kondisi awal saat scene dimuat.</td>
          <td>Menampilkan panel judul utama; input karakter dinonaktifkan.</td>
        </tr>
        <tr>
          <td><code>DifficultySelect</code></td>
          <td>Pemain menekan tombol Mulai Bermain.</td>
          <td>Menampilkan halaman Pilih Kesulitan (Mudah/Normal/Sulit) beserta pengali skor; pilihan disimpan di <code>PlayerPrefs</code>.</td>
        </tr>""",
        "baris DifficultySelect",
    )
    swap(
        "<td>Menghentikan musuh, memutar audio kemenangan, dan menampilkan layar <i>Desa Girah Pulih</i>.</td>",
        "<td>Menghitung skor level dan skor total, memutar audio kemenangan, lalu menampilkan halaman hasil dengan tombol Level Berikutnya (level 1–2) atau Selesai (level 3).</td>",
        "Victory behavior",
    )
    swap(
        "<td>Menampilkan layar gagal beserta tombol <i>Coba Lagi</i> (reload scene).</td>",
        "<td>Menampilkan layar gagal dengan skor total, tombol Coba Lagi (mengulang level saat ini), dan Menu Utama.</td>",
        "GameOver behavior",
    )

    swap(
        """                <b style="color:#1b4d89;">Layar Main Menu</b><br>
                <span style="font-size: 9pt;">Klik tombol <i>&ldquo;Mulai Penyucian&rdquo;</i></span>""",
        """                <b style="color:#1b4d89;">Layar Main Menu</b><br>
                <span style="font-size: 9pt;">Klik <i>&ldquo;Mulai Bermain&rdquo;</i></span>""",
        "flow node 1",
    )
    swap(
        """                <b style="color:#1b4d89;">Panel Dialog Mpu Bharada</b><br>
                <span style="font-size: 9pt;">Baca misi &amp; klik <i>&ldquo;Mengerti (E)&rdquo;</i></span>""",
        """                <b style="color:#1b4d89;">Pilih Kesulitan</b><br>
                <span style="font-size: 9pt;">Mudah / Normal / Sulit + pengali skor</span>""",
        "flow node 2",
    )
    swap(
        """                <b style="color:#1b4d89;">HUD Gameplay + Jeda (ESC)</b><br>
                <span style="font-size: 9pt;">Eksplorasi, Stun, Ambil Lontar; ESC membuka Jeda</span>""",
        """                <b style="color:#1b4d89;">Level 1 &rarr; 2 &rarr; 3</b><br>
                <span style="font-size: 9pt;">3 Lontar + Altar per level; 3/4/5 musuh</span>""",
        "flow node 3",
    )
    swap(
        """                <b style="color:#1b4d89;">Layar Victory / Game Over</b><br>
                <span style="font-size: 9pt;">Gelar, waktu, nyawa, energi, rekor; <i>&ldquo;Main Lagi&rdquo;</i></span>""",
        """                <b style="color:#1b4d89;">Hasil Level (skor)</b><br>
                <span style="font-size: 9pt;">Skor level/total, gelar; lanjut level atau menu</span>""",
        "flow node 4",
    )
    swap(
        "Selain alur utama, Main Menu menyediakan <b>CARA BERMAIN</b>, <b>PENGATURAN</b> (slider BGM/SFX, layar penuh, tiga tingkat kesulitan), dan <b>KREDIT</b> (atribusi aset). Saat bermain, <code>ESC</code> membuka panel <b>JEDA</b>; dari panel tersebut pemain dapat membuka Pengaturan atau kembali ke menu utama.",
        "Setelah halaman kesulitan, dialog Mpu Bharada muncul satu kali sebelum Level 1. Level 2 dan 3 dimulai langsung dengan banner tujuan. Main Menu juga menyediakan <b>CARA BERMAIN</b>, <b>PENGATURAN</b> (slider BGM/SFX dan layar penuh), serta <b>KREDIT</b>. Saat bermain, <code>ESC</code> membuka panel <b>JEDA</b>.",
        "flow note",
    )

    swap(
        """                <b>NYAWA:</b> <span style="color: #ff5964;">&hearts; &hearts; &hearts;</span> (3/3)""",
        """                <b>NYAWA:</b> <span style="color: #ff5964;">&hearts; &hearts; &hearts;</span> (3/3)<br>
                <span style="font-size: 8.5pt; color: #ffd166;">LEVEL 2/3 &mdash; HUTAN BAMBU LEMAH TULIS</span>""",
        "wireframe nyawa",
    )
    swap(
        """                <b>LONTAR SUCI:</b> <span style="color: #ffb84d;">2 / 3</span><br>
                <span style="font-size: 8.5pt; color: #64c8ff;">WAKTU 00:42</span>""",
        """                <b>LONTAR SUCI:</b> <span style="color: #ffb84d;">2 / 3</span><br>
                <span style="font-size: 8.5pt; color: #64c8ff;">WAKTU 00:42 &nbsp;|&nbsp; SKOR: 1,986</span>""",
        "wireframe lontar",
    )

    swap(
        "<li><code>Assets/_Project/Scripts/Managers/</code> &mdash; Berisi <code>GameManager.cs</code>, <code>AudioManager.cs</code>, <code>UIManager.cs</code>, dan <code>DifficultySettings.cs</code>.</li>",
        "<li><code>Assets/_Project/Scripts/Managers/</code> &mdash; Berisi <code>GameManager.cs</code>, <code>AudioManager.cs</code>, <code>UIManager.cs</code>, <code>DifficultySettings.cs</code>, <code>LevelManager.cs</code>, dan <code>LevelController.cs</code>.</li>",
        "8.1 managers",
    )

    start = html.find('<h2 class="section-title">8.2 Peta Jalan')
    end = html.find("</ol>", start)
    if start == -1 or end == -1:
        raise SystemExit("[HTML] blok 8.2 tidak ditemukan")
    end += len("</ol>")
    new_82 = """<h2 class="section-title">8.2 Peta Jalan Ekspansi Menuju Fase Berikutnya</h2>
    <p>
      Versi final prototipe ini menyatukan fitur Tugas 2 dengan revisi tiga level, alur kesulitan, dan sistem skor:
    </p>
    <ol>
      <li><b>Fitur final:</b> tiga level (Desa Girah, Hutan Bambu Lemah Tulis, Pelataran Setra Gandamayu), halaman Pilih Kesulitan, mekanik <i>Rwa Bhineda Exposure</i>, skor/gelar/rekor, menu Pengaturan &amp; Jeda, serta layar Kredit.</li>
      <li><b>Keputusan desain &mdash; <i>Save System</i> tidak diimplementasikan:</b> seluruh permainan dapat diselesaikan dalam beberapa menit dan level dapat diulang dari halaman hasil. Persistensi dibatasi pada pengaturan dan rekor skor melalui <code>PlayerPrefs</code>.</li>
      <li><b>Ekspansi berikutnya:</b> ekspor Android dengan <i>virtual joystick</i>, penambahan level dan variasi musuh, serta <i>save</i> progres bila jumlah konten sudah cukup besar.</li>
      <li><b>Verifikasi final:</b> 74/74 assertion <i>play-mode</i> PASS; build macOS (<code>.app</code>) dan Windows (<code>.exe</code>) berhasil; build macOS dijalankan dan berjalan normal (19 November 2026).</li>
    </ol>"""
    html = html[:start] + new_82 + html[end:]

    with open(HTML_PATH, "w", encoding="utf-8") as handle:
        handle.write(html)
    print("[HTML] OK")


def apply_docx():
    doc = Document(DOCX_PATH)

    # 1.2 ringkasan
    for paragraph in doc.paragraphs:
        if paragraph.text.startswith("Versi final prototipe (Tugas 3)"):
            set_paragraph_text(
                paragraph,
                "Versi final prototipe menambahkan tiga level (dua peta baru), halaman Pilih Kesulitan setelah tombol "
                "Mulai Bermain, mekanik Rwa Bhineda Exposure, serta skor, gelar, dan rekor pada halaman hasil tiap level. "
                "Save progres tidak diimplementasikan karena permainan dapat diselesaikan dalam beberapa menit; "
                "persistensi dibatasi pada pengaturan dan rekor skor.",
            )
            break

    # 3.3 mekanik 1
    for paragraph in doc.paragraphs:
        if paragraph.text.startswith("Mekanik Utama 1:"):
            replace_in_paragraph(
                paragraph,
                "Pada awal permainan, Altar Penyucian yang terletak di pusat Desa Girah diselimuti segel kabut gelap. "
                "Pemain harus menjelajahi tiga sektor desa (Sektor Utara, Sektor Timur, dan Sektor Barat) untuk "
                "mengumpulkan 3 naskah Lontar Suci. Setiap Lontar yang diambil akan menyalakan indikator lontar pada HUD "
                "dan membuka kutipan kearifan lokal. Begitu ketiga Lontar terkumpul, segel Altar terbuka secara otomatis "
                "dan memancarkan cahaya emas sebagai penanda titik penyelesaian misi.",
                "Di setiap level, Altar Penyucian dikelilingi segel kabut gelap. Pemain menjelajahi peta level untuk "
                "mengumpulkan 3 naskah Lontar Suci; setiap Lontar menyalakan indikator HUD dan membuka kutipan kearifan "
                "lokal. Begitu ketiga Lontar terkumpul, segel Altar terbuka dan memancarkan cahaya emas. Menyentuh Altar "
                "menyelesaikan level dan membuka halaman hasil dengan skor serta opsi lanjut ke level berikutnya atau "
                "kembali ke menu utama.",
            )
            break

    # 3.3 kesulitan
    for paragraph in doc.paragraphs:
        if paragraph.text.startswith("Tingkat Kesulitan."):
            replace_in_paragraph(
                paragraph,
                "Nilai dipilih di panel PENGATURAN, disimpan di PlayerPrefs, dan diterapkan saat misi dimulai.",
                "Nilai dipilih pada halaman PILIH KESULITAN setelah tombol Mulai Bermain, disimpan di PlayerPrefs, dan diterapkan ke ketiga level.",
            )
            break

    # 3.3 hasil + struktur level
    results = None
    for paragraph in doc.paragraphs:
        if paragraph.text.startswith("Hasil Akhir, Gelar, dan Rekor."):
            results = paragraph
            break

    if results is None:
        raise SystemExit("[DOCX] paragraf hasil tidak ditemukan")

    replace_in_paragraph(
        results,
        "Saat Victory, GameManager mencatat waktu tempuh, nyawa, dan sisa energi. Gelar: Penyuci Agung "
        "(waktu <= 2:30 dan nyawa 3/3), Murid Teladan (waktu <= 4:00 dan nyawa >= 2/3), Pejalan Malam "
        "(selain kondisi tersebut). Waktu terbaik disimpan di PlayerPrefs dan ditampilkan sebagai rekor. "
        "Save progres tidak diimplementasikan karena sesi dapat diselesaikan dalam hitungan menit.",
        "Saat level selesai, GameManager menghitung skor level = (500 + bonus waktu + nyawa x 100 + sisa energi x 2) "
        "x pengali kesulitan. Bonus waktu dimulai dari 600 dan berkurang 5 per detik. Skor total adalah akumulasi "
        "ketiga level; rekor skor disimpan di PlayerPrefs setelah level 3. Gelar level: Penyuci Agung "
        "(waktu <= 2:30 dan nyawa 3/3), Murid Teladan (waktu <= 4:00 dan nyawa >= 2/3), atau Pejalan Malam.",
    )

    body_template = doc.paragraphs[25]
    insert_rich_after(
        results,
        body_template,
        [
            ("Struktur Tiga Level. ", True),
            (
                "Level 1 Desa Girah Bagian Luar (3 musuh, 3 Lontar di sektor utara/barat/timur); Level 2 Hutan Bambu "
                "Lemah Tulis (4 musuh, lorong sempit dan clearing); Level 3 Pelataran Setra Gandamayu (5 musuh, plaza "
                "dan pura). Setiap level memiliki altar, 3 Lontar, dan 3 Minyak Obor. LevelManager mengaktifkan satu "
                "level dan LevelController mereset pemain, musuh, item, dan altar saat level dimuat.",
                False,
            ),
        ],
    )

    # FSM diagram
    fsm = doc.tables[7].rows[1].cells[0].tables[0]
    for paragraph in fsm.rows[0].cells[0].paragraphs:
        replace_in_paragraph(paragraph, "MainMenu → IntroDialog", "MainMenu → DifficultySelect → IntroDialog")

    # State table: sisipkan DifficultySelect setelah MainMenu
    state_table = doc.tables[8]
    main_row = state_table.rows[1]
    new_tr = copy.deepcopy(state_table.rows[2]._tr)
    main_row._tr.addnext(new_tr)
    new_row = state_table.rows[2]
    set_cell_text(new_row.cells[1], "DifficultySelect")
    set_cell_text(new_row.cells[2], "Pemain menekan tombol Mulai Bermain.")
    set_cell_text(
        new_row.cells[3],
        "Menampilkan halaman Pilih Kesulitan (Mudah/Normal/Sulit) beserta pengali skor; pilihan disimpan di PlayerPrefs.",
    )

    # Victory & GameOver behavior
    for row in state_table.rows:
        if len(row.cells) >= 4 and row.cells[1].text.strip() == "Victory":
            set_cell_text(
                row.cells[3],
                "Menghitung skor level dan skor total, memutar audio kemenangan, lalu menampilkan halaman hasil dengan "
                "tombol Level Berikutnya (level 1-2) atau Selesai (level 3).",
            )
        if len(row.cells) >= 4 and row.cells[1].text.strip() == "GameOver":
            set_cell_text(
                row.cells[3],
                "Menampilkan layar gagal dengan skor total, tombol Coba Lagi (mengulang level saat ini), dan Menu Utama.",
            )

    # User flow
    flow = doc.tables[12].rows[1].cells[0].tables[0].rows[0]
    set_cell_text(flow.cells[0], "Layar Main Menu\nKlik “Mulai Bermain”")
    set_cell_text(flow.cells[2], "Pilih Kesulitan\nMudah / Normal / Sulit + pengali skor")
    set_cell_text(flow.cells[4], "Level 1 → 2 → 3\n3 Lontar + Altar per level; 3/4/5 musuh")
    set_cell_text(flow.cells[6], "Hasil Level (skor)\nSkor level/total, gelar; lanjut level atau menu")

    # Catatan setelah bagan user flow (cari paragraf yang dimulai “Selain alur utama”)
    for paragraph in doc.paragraphs:
        if paragraph.text.startswith("Selain alur utama"):
            set_paragraph_text(
                paragraph,
                "Setelah halaman kesulitan, dialog Mpu Bharada muncul satu kali sebelum Level 1. Level 2 dan 3 dimulai "
                "langsung dengan banner tujuan. Main Menu juga menyediakan CARA BERMAIN, PENGATURAN (slider BGM/SFX dan "
                "layar penuh), serta KREDIT. Saat bermain, ESC membuka panel JEDA.",
            )
            break

    # Wireframe
    wire = doc.tables[13].rows[0].cells[0].tables[0].rows[0]
    set_cell_text(wire.cells[0], "NYAWA: ♥ ♥ ♥ (3/3)\nLEVEL 2/3 — HUTAN BAMBU LEMAH TULIS")
    set_cell_text(wire.cells[2], "LONTAR SUCI: 2 / 3\nWAKTU 00:42  |  SKOR: 1,986")

    # 8.1
    for paragraph in doc.paragraphs:
        if paragraph.text.startswith("Assets/_Project/Scripts/Managers/"):
            replace_in_paragraph(
                paragraph,
                "Berisi GameManager.cs, AudioManager.cs, UIManager.cs, dan DifficultySettings.cs.",
                "Berisi GameManager.cs, AudioManager.cs, UIManager.cs, DifficultySettings.cs, LevelManager.cs, dan LevelController.cs.",
            )
            break

    # 8.2
    intro = next(p for p in doc.paragraphs if p.text.startswith("Versi final prototipe ini"))
    set_paragraph_text(
        intro,
        "Versi final prototipe ini menyatukan fitur Tugas 2 dengan revisi tiga level, alur kesulitan, dan sistem skor:",
    )

    item1 = next(p for p in doc.paragraphs if p.text.startswith("Fitur final yang telah diimplementasikan"))
    set_paragraph_text(
        item1,
        "Fitur final: tiga level (Desa Girah, Hutan Bambu Lemah Tulis, Pelataran Setra Gandamayu), halaman Pilih "
        "Kesulitan, mekanik Rwa Bhineda Exposure, skor/gelar/rekor, menu Pengaturan & Jeda, serta layar Kredit.",
    )

    item2 = next(p for p in doc.paragraphs if p.text.startswith("Keputusan desain"))
    set_paragraph_text(
        item2,
        "Keputusan desain — Save System tidak diimplementasikan: seluruh permainan dapat diselesaikan dalam beberapa "
        "menit dan level dapat diulang dari halaman hasil. Persistensi dibatasi pada pengaturan dan rekor skor melalui "
        "PlayerPrefs.",
    )

    item3 = next(p for p in doc.paragraphs if p.text.startswith("Ekspansi berikutnya"))
    set_paragraph_text(
        item3,
        "Ekspansi berikutnya: ekspor Android dengan virtual joystick, penambahan level dan variasi musuh, serta save "
        "progres bila jumlah konten sudah cukup besar.",
    )

    item4 = next(p for p in doc.paragraphs if p.text.startswith("Verifikasi final"))
    set_paragraph_text(
        item4,
        "Verifikasi final: 74/74 assertion play-mode PASS; build macOS (.app) dan Windows (.exe) berhasil; build macOS "
        "dijalankan dan berjalan normal (19 November 2026).",
    )

    doc.save(DOCX_PATH)
    print("[DOCX] OK")


def verify():
    with open(HTML_PATH, encoding="utf-8") as handle:
        html = handle.read()

    doc = Document(DOCX_PATH)
    chunks = [p.text for p in doc.paragraphs]

    def walk(tables):
        for table in tables:
            for row in table.rows:
                for cell in row.cells:
                    chunks.extend(p.text for p in cell.paragraphs)
                    if cell.tables:
                        walk(cell.tables)

    walk(doc.tables)
    text = "\n".join(chunks)

    for item in ["Struktur Tiga Level", "DifficultySelect", "74/74", "Hutan Bambu Lemah Tulis", "Pelataran Setra Gandamayu"]:
        if item not in html:
            raise SystemExit(f"[VERIFY] HTML tidak memuat: {item}")
        if item not in text:
            raise SystemExit(f"[VERIFY] DOCX tidak memuat: {item}")

    print(f"[VERIFY] OK; paragraf DOCX={len(doc.paragraphs)}; tabel DOCX={len(doc.tables)}")


if __name__ == "__main__":
    apply_html()
    apply_docx()
    verify()
