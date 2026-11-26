#!/usr/bin/env python3
"""Sinkronisasi GDD final Tugas 3 (HTML + DOCX).

Mengubah hanya bagian yang terdampak pengembangan final:
- TOC 3.3 (Dua -> Tiga Mekanik)
- 3.1 kontrol: Jeda/Pengaturan
- 3.3 Mekanik 3, tingkat kesulitan, hasil/gelar/rekor
- MDA: mechanics/dynamics/aesthetics tambahan
- 4.1 diagram FSM: Playing <-> Paused
- 4.2 tabel state: baris Paused
- 6.2 user flow + catatan panel menu
- 6.3 wireframe HUD: timer + status cahaya + ESC
- 8.1 struktur folder
- 8.2 roadmap final + verifikasi
"""

import copy
import os
import sys

from docx import Document
from docx.text.paragraph import Paragraph

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.path.join(ROOT, "docs")
DOCX_PATH = os.path.join(BASE, "gdd", "230030309_Muhammad_Sufyan_Game_Design_Document_GDD_Lentera_Dirah.docx")
HTML_PATH = os.path.join(BASE, "html", "230030309_Muhammad_Sufyan_Game_Design_Document_GDD_Lentera_Dirah.html")

NEW_333_TITLE = "3.3 Spesifikasi Tiga Mekanik Gameplay Utama"


def apply_html():
    with open(HTML_PATH, encoding="utf-8") as handle:
        html = handle.read()

    def must_replace(old, new, label):
        nonlocal html
        if old not in html:
            raise SystemExit(f"[HTML] Anchor tidak ditemukan: {label}")
        html = html.replace(old, new, 1)

    # TOC
    must_replace(
        "3.3 Spesifikasi Dua Mekanik Gameplay Utama",
        NEW_333_TITLE,
        "TOC 3.3",
    )

    # 3.1 kontrol
    must_replace(
        """        <tr>
          <td><b>Interaksi UI / Lanjut Dialog / Restart</b></td>
          <td>Klik Kiri Mouse / Tombol <code>E</code></td>
          <td>Event <code>Button.onClick</code> pada Canvas UI untuk mengubah state pada <code>GameManager</code> (dari <code>MainMenu</code> ke <code>IntroDialog</code>, lalu ke <code>Playing</code>).</td>
        </tr>
      </tbody>""",
        """        <tr>
          <td><b>Interaksi UI / Lanjut Dialog / Restart</b></td>
          <td>Klik Kiri Mouse / Tombol <code>E</code></td>
          <td>Event <code>Button.onClick</code> pada Canvas UI untuk mengubah state pada <code>GameManager</code> (dari <code>MainMenu</code> ke <code>IntroDialog</code>, lalu ke <code>Playing</code>).</td>
        </tr>
        <tr>
          <td><b>Jeda &amp; Pengaturan</b></td>
          <td>Tombol <code>ESC</code> / tombol <b>PENGATURAN</b></td>
          <td><code>GameManager.Pause()</code> menyetel <code>Time.timeScale = 0</code> dan state menjadi <code>Paused</code>; panel Jeda menampilkan Lanjutkan, Pengaturan, dan Ke Menu Utama. Slider volume, layar penuh, serta pilihan kesulitan disimpan melalui <code>PlayerPrefs</code>.</td>
        </tr>
      </tbody>""",
        "3.1 kontrol",
    )

    # 3.3 blok baru
    start = html.find('<h2 class="section-title" id="gdd-3-3">')
    end = html.find("</ol>", start)
    if start == -1 or end == -1:
        raise SystemExit("[HTML] Blok 3.3 tidak ditemukan")
    end += len("</ol>")

    new_333 = """<h2 class="section-title" id="gdd-3-3">3.3 Spesifikasi Tiga Mekanik Gameplay Utama</h2>
    <ol>
      <li>
        <b>Mekanik Utama 1: <i>Sacred Lontar Collection &amp; Altar Seal System</i></b><br>
        Pada awal permainan, Altar Penyucian yang terletak di pusat Desa Girah diselimuti segel kabut gelap. Pemain harus menjelajahi tiga sektor desa (Sektor Utara, Sektor Timur, dan Sektor Barat) untuk mengumpulkan 3 naskah Lontar Suci. Setiap Lontar yang diambil akan menyalakan indikator lontar pada HUD dan membuka kutipan kearifan lokal. Begitu ketiga Lontar terkumpul, segel Altar terbuka secara otomatis dan memancarkan cahaya emas sebagai penanda titik penyelesaian misi.
      </li>
      <li>
        <b>Mekanik Utama 2: <i>Dynamic Lantern Light &amp; Rwa Bhineda Stun Burst</i></b><br>
        Karakter Bahula dilengkapi komponen <code>Light 2D (Point Light)</code> yang radius terangnya berbanding lurus dengan persentase energi lentera (pada energi <code>100%</code> radius luar adalah <code>6.0 unit</code>; menyusut perlahan hingga minimal <code>1.8 unit</code>). Apabila energi lentera mencapai <code>0%</code>, kegelapan menyelimuti pemain sepenuhnya dan memicu kondisi kalah (<i>Game Over</i>). Pemain dapat menekan tombol <code>Space</code> untuk melepaskan pancaran cahaya suci yang membekukan (<i>Stun</i>) seluruh NPC Bayangan Wabah di sekitarnya selama 3 detik.
      </li>
      <li>
        <b>Mekanik Utama 3: <i>Rwa Bhineda Exposure</i></b><br>
        Energi lentera tidak hanya menentukan luas pandangan, tetapi juga tingkat keterlihatan Bahula. Radius deteksi efektif Bayangan Wabah dihitung sebagai
        <code>detectRadius &times; pengali kesulitan &times; Lerp(0.7, 1.3, energi/100)</code>.
        Pada energi <code>100%</code> musuh mendeteksi hingga <b>30% lebih jauh</b>; pada energi rendah deteksi menyusut hingga <b>30%</b>, sehingga lentera redup berfungsi sebagai penyamaran. HUD menampilkan status <code>CAHAYA: TERANG / SEIMBANG / REDUP</code> beserta persentase deteksi saat ini. Mekanik ini menjadikan <i>Light Decay</i> sebagai keputusan taktis, bukan sekadar pengatur waktu.
      </li>
    </ol>

    <p><b>Tingkat Kesulitan.</b> Tiga pilihan kesulitan mengubah laju energi, kecepatan, dan kepekaan Bayangan Wabah. Nilai dipilih di panel PENGATURAN, disimpan di <code>PlayerPrefs</code>, dan diterapkan saat misi dimulai (saat dialog pembuka ditutup).</p>
    <table class="data-table">
      <thead>
        <tr>
          <th style="width: 20%;" bgcolor="#e8eef5">Kesulitan</th>
          <th style="width: 24%;" bgcolor="#e8eef5">Laju Energi</th>
          <th style="width: 28%;" bgcolor="#e8eef5">Kecepatan Musuh</th>
          <th style="width: 28%;" bgcolor="#e8eef5">Deteksi Musuh</th>
        </tr>
      </thead>
      <tbody>
        <tr><td><b>Mudah</b></td><td>1.5%/detik (x0.75)</td><td>x0.85</td><td>x0.80</td></tr>
        <tr><td><b>Normal</b></td><td>2.0%/detik (x1.00)</td><td>x1.00</td><td>x1.00</td></tr>
        <tr><td><b>Sulit</b></td><td>2.7%/detik (x1.35)</td><td>x1.15</td><td>x1.25</td></tr>
      </tbody>
    </table>

    <p><b>Hasil Akhir, Gelar, dan Rekor.</b> Saat Victory, <code>GameManager</code> mencatat waktu tempuh, nyawa, dan sisa energi lentera. Gelar dihitung dari waktu dan nyawa; waktu terbaik disimpan di <code>PlayerPrefs</code> dan ditampilkan sebagai rekor. Save progres permainan tidak diimplementasikan karena sesi dapat diselesaikan dalam hitungan menit.</p>
    <table class="data-table">
      <thead>
        <tr>
          <th style="width: 30%;" bgcolor="#e8eef5">Gelar</th>
          <th style="width: 70%;" bgcolor="#e8eef5">Syarat</th>
        </tr>
      </thead>
      <tbody>
        <tr><td><b>Penyuci Agung</b></td><td>Waktu &le; 2:30 dan nyawa tetap 3/3.</td></tr>
        <tr><td><b>Murid Teladan</b></td><td>Waktu &le; 4:00 dan nyawa &ge; 2/3.</td></tr>
        <tr><td><b>Pejalan Malam</b></td><td>Selain kondisi di atas.</td></tr>
      </tbody>
    </table>"""

    html = html[:start] + new_333 + html[end:]

    # MDA
    must_replace(
        """            4. Syarat buka segel Altar Penyucian: variabel <code>lontarCollected == 3</code>.""",
        """            4. Syarat buka segel Altar Penyucian: variabel <code>lontarCollected == 3</code>.<br>
            5. Mekanik <i>Rwa Bhineda Exposure</i>: radius deteksi musuh = <code>detectRadius &times; pengali kesulitan &times; Lerp(0.7, 1.3, energi/100)</code>.<br>
            6. Tiga tingkat kesulitan (Mudah, Normal, Sulit) mengubah laju energi, kecepatan, dan deteksi musuh.<br>
            7. Gelar akhir dan rekor waktu dihitung saat Victory; pengaturan, kesulitan, dan rekor disimpan via <code>PlayerPrefs</code>.""",
        "MDA mechanics",
    )
    must_replace(
        """            2. <b>Navigasi Taktis (Risk vs. Reward):</b> Mengambil Lontar di sudut sempit menuntut pemain mengamati pola gerak <i>Patrol</i> NPC Bayangan terlebih dahulu.""",
        """            2. <b>Navigasi Taktis (Risk vs. Reward):</b> Mengambil Lontar di sudut sempit menuntut pemain mengamati pola gerak <i>Patrol</i> NPC Bayangan terlebih dahulu.<br>
            3. <b>Negosiasi Terang&ndash;Gelap:</b> Mempertahankan lentera terang memperluas pandangan tetapi memperbesar jangkauan deteksi musuh; membiarkan lentera redup menyamarkan posisi tetapi mempersempit navigasi.""",
        "MDA dynamics",
    )
    must_replace(
        """            2. <b>Cultural Immersion (Penghayatan Budaya):</b> Pengalaman menyelami filosofi <i>Rwa Bhineda</i> secara langsung melalui kontras cahaya dan bayangan.""",
        """            2. <b>Cultural Immersion (Penghayatan Budaya):</b> Pengalaman menyelami filosofi <i>Rwa Bhineda</i> secara langsung melalui kontras cahaya dan bayangan.<br>
            3. <b>Mastery &amp; Replayability:</b> Gelar akhir, rekor waktu, dan tiga tingkat kesulitan mendorong pemain mengulang misi dengan strategi cahaya yang berbeda.""",
        "MDA aesthetics",
    )

    # 4.1 diagram
    must_replace(
        "<code>MainMenu</code> &rarr; <code>IntroDialog</code> &rarr; <code>Playing</code> &rarr; (<code>Victory</code> / <code>GameOver</code>)",
        "<code>MainMenu</code> &rarr; <code>IntroDialog</code> &rarr; <code>Playing</code> &harr; <code>Paused</code> &rarr; (<code>Victory</code> / <code>GameOver</code>)",
        "FSM diagram",
    )

    # 4.2 tabel state
    must_replace(
        '<td rowspan="5"><b>Game Manager</b><br>(<code>GameManager.cs</code>)</td>',
        '<td rowspan="6"><b>Game Manager</b><br>(<code>GameManager.cs</code>)</td>',
        "rowspan FSM",
    )
    must_replace(
        """        <tr>
          <td><code>Playing</code></td>
          <td>Pemain menutup dialog pembuka.</td>
          <td>Mengaktifkan kontrol pemain, AI patroli musuh, dan pengurangan energi lentera.</td>
        </tr>""",
        """        <tr>
          <td><code>Playing</code></td>
          <td>Pemain menutup dialog pembuka.</td>
          <td>Mengaktifkan kontrol pemain, AI patroli musuh, dan pengurangan energi lentera.</td>
        </tr>
        <tr>
          <td><code>Paused</code></td>
          <td>Pemain menekan <code>Esc</code> saat <code>Playing</code>.</td>
          <td><code>Time.timeScale = 0</code>; panel Jeda tampil (Lanjutkan, Pengaturan, Ke Menu Utama); <code>Esc</code> melanjutkan permainan.</td>
        </tr>""",
        "baris Paused",
    )

    # 6.2 user flow
    must_replace(
        """                <b style="color:#1b4d89;">HUD Gameplay Aktif</b><br>
                <span style="font-size: 9pt;">Eksplorasi, Stun Bayangan, &amp; Ambil 3 Lontar</span>""",
        """                <b style="color:#1b4d89;">HUD Gameplay + Jeda (ESC)</b><br>
                <span style="font-size: 9pt;">Eksplorasi, Stun, Ambil Lontar; ESC membuka Jeda</span>""",
        "user flow node 3",
    )
    must_replace(
        """                <b style="color:#1b4d89;">Layar Victory / Game Over</b><br>
                <span style="font-size: 9pt;">Tombol <i>&ldquo;Main Lagi&rdquo;</i></span>""",
        """                <b style="color:#1b4d89;">Layar Victory / Game Over</b><br>
                <span style="font-size: 9pt;">Gelar, waktu, nyawa, energi, rekor; <i>&ldquo;Main Lagi&rdquo;</i></span>""",
        "user flow node 4",
    )
    must_replace(
        """      </tr>
    </table>

    <h2 class="section-title" id="gdd-6-3">""",
        """      </tr>
    </table>

    <p>
      Selain alur utama, Main Menu menyediakan <b>CARA BERMAIN</b>, <b>PENGATURAN</b> (slider BGM/SFX, layar penuh, tiga tingkat kesulitan), dan <b>KREDIT</b> (atribusi aset). Saat bermain, <code>ESC</code> membuka panel <b>JEDA</b>; dari panel tersebut pemain dapat membuka Pengaturan atau kembali ke menu utama.
    </p>

    <h2 class="section-title" id="gdd-6-3">""",
        "catatan user flow",
    )

    # 6.3 wireframe
    must_replace(
        """                <b>ENERGI LENTERA:</b> <span style="color: #ffb84d;">[████████░░] 80%</span>""",
        """                <b>ENERGI LENTERA:</b> <span style="color: #ffb84d;">[████████░░] 80%</span><br>
                <span style="font-size: 8.5pt; color: #ffd166;">CAHAYA: TERANG &middot; deteksi musuh +30%</span>""",
        "wireframe energi",
    )
    must_replace(
        """                <b>LONTAR SUCI:</b> <span style="color: #ffb84d;">2 / 3</span>""",
        """                <b>LONTAR SUCI:</b> <span style="color: #ffb84d;">2 / 3</span><br>
                <span style="font-size: 8.5pt; color: #64c8ff;">WAKTU 00:42</span>""",
        "wireframe lontar",
    )
    must_replace(
        """<b>KONTROL:</b> [WASD] Bergerak &nbsp;|&nbsp; [SPACE] Pancaran Cahaya Suci (Siap!)""",
        """<b>KONTROL:</b> [WASD] Bergerak &nbsp;|&nbsp; [SPACE] Pancaran Cahaya Suci (Siap!) &nbsp;|&nbsp; [ESC] Jeda""",
        "wireframe kontrol",
    )

    # 8.1 struktur folder
    must_replace(
        "<li><code>Assets/_Project/Scripts/Managers/</code> &mdash; Berisi <code>GameManager.cs</code> dan <code>AudioManager.cs</code>.</li>",
        "<li><code>Assets/_Project/Scripts/Managers/</code> &mdash; Berisi <code>GameManager.cs</code>, <code>AudioManager.cs</code>, <code>UIManager.cs</code>, dan <code>DifficultySettings.cs</code>.</li>",
        "8.1 managers",
    )

    # 8.2 roadmap
    start = html.find("<h2 class=\"section-title\">8.2 Peta Jalan")
    end = html.find("</ol>", start)
    if start == -1 or end == -1:
        raise SystemExit("[HTML] Blok 8.2 tidak ditemukan")
    end += len("</ol>")

    new_82 = """<h2 class="section-title">8.2 Peta Jalan Ekspansi Menuju Fase Berikutnya</h2>
    <p>
      Versi final prototipe ini menyatukan seluruh fitur Tugas 2 dengan lima pengembangan Tugas 3, sekaligus menetapkan arah ekspansi berikutnya:
    </p>
    <ol>
      <li><b>Fitur final yang telah diimplementasikan:</b> menu Pengaturan &amp; Jeda (volume BGM/SFX, layar penuh, tiga tingkat kesulitan), layar Kredit, Mekanik <i>Rwa Bhineda Exposure</i>, serta hasil akhir dengan gelar dan rekor waktu.</li>
      <li><b>Keputusan desain &mdash; <i>Save System</i> tidak diimplementasikan:</b> sesi permainan dapat diselesaikan dalam &plusmn;2 menit sehingga penyimpanan progres tidak memberi nilai tambah. Persistensi dibatasi pada pengaturan, kesulitan, dan rekor waktu melalui <code>PlayerPrefs</code>.</li>
      <li><b>Ekspansi berikutnya:</b> Level 2 (<i>Hutan Bambu Lemah Tulis</i>) dan Level 3 (<i>Pelataran Setra Gandamayu</i>) dengan kurva kesulitan progresif; <i>save</i> progres menjadi relevan setelah jumlah level bertambah; serta ekspor Android dengan <i>virtual joystick</i>.</li>
      <li><b>Verifikasi final:</b> 40/40 assertion <i>play-mode</i> PASS; build macOS (<code>.app</code>) dan Windows (<code>.exe</code>) berhasil; build macOS dijalankan dan berjalan normal (19 November 2026).</li>
    </ol>"""

    html = html[:start] + new_82 + html[end:]

    with open(HTML_PATH, "w", encoding="utf-8") as handle:
        handle.write(html)

    print("[HTML] OK")


# ---------------------------------------------------------------------------
# DOCX
# ---------------------------------------------------------------------------

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


def clear_runs(paragraph):
    for child in list(paragraph._p):
        if child.tag.endswith("}pPr"):
            continue
        paragraph._p.remove(child)


def insert_rich_after(anchor, template, parts):
    new_p = copy.deepcopy(template._p)
    anchor._p.addnext(new_p)
    paragraph = Paragraph(new_p, anchor._parent)
    clear_runs(paragraph)

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


def apply_docx():
    doc = Document(DOCX_PATH)

    # TOC (tabel 1) — teks TOC berada di dalam hyperlink, jadi set sel langsung
    for row in doc.tables[1].rows:
        for cell in row.cells:
            if "3.3 Spesifikasi Dua Mekanik Gameplay Utama" in cell.text:
                set_cell_text(cell, "3.3 Spesifikasi Tiga Mekanik Gameplay Utama")

    # 3.3 heading
    for paragraph in doc.paragraphs:
        if paragraph.text.strip() == "3.3 Spesifikasi Dua Mekanik Gameplay Utama":
            replace_in_paragraph(paragraph, "Dua Mekanik", "Tiga Mekanik")

    # 3.1 tabel kontrol: tambah baris
    control_table = doc.tables[5]
    row = control_table.add_row()
    set_cell_text(row.cells[0], "Jeda & Pengaturan")
    set_cell_text(row.cells[1], "Tombol ESC / tombol PENGATURAN")
    set_cell_text(
        row.cells[2],
        "GameManager.Pause() menyetel Time.timeScale = 0 dan state menjadi Paused; panel Jeda "
        "menampilkan Lanjutkan, Pengaturan, dan Ke Menu Utama. Slider volume, layar penuh, serta "
        "pilihan kesulitan disimpan melalui PlayerPrefs.",
    )

    # 3.3 tambahan paragraf
    anchor = None
    for paragraph in doc.paragraphs:
        if paragraph.text.startswith("Mekanik Utama 2:"):
            anchor = paragraph
            break

    if anchor is None:
        raise SystemExit("[DOCX] Paragraf Mekanik Utama 2 tidak ditemukan")

    body_template = doc.paragraphs[22]
    mechanic3 = insert_rich_after(
        anchor,
        anchor,
        [
            ("Mekanik Utama 3: ", True),
            ("Rwa Bhineda Exposure", True),
            (
                "\nEnergi lentera tidak hanya menentukan luas pandangan, tetapi juga tingkat keterlihatan Bahula. "
                "Radius deteksi efektif Bayangan Wabah = detectRadius x pengali kesulitan x Lerp(0.7, 1.3, energi/100). "
                "Pada energi 100% musuh mendeteksi hingga 30% lebih jauh; pada energi rendah deteksi menyusut hingga 30%, "
                "sehingga lentera redup berfungsi sebagai penyamaran. HUD menampilkan CAHAYA: TERANG / SEIMBANG / REDUP. "
                "Mekanik ini menjadikan Light Decay sebagai keputusan taktis, bukan sekadar pengatur waktu.",
                False,
            ),
        ],
    )

    difficulty = insert_rich_after(
        mechanic3,
        body_template,
        [
            ("Tingkat Kesulitan. ", True),
            (
                "Tiga pilihan kesulitan mengubah laju energi, kecepatan, dan kepekaan Bayangan Wabah: "
                "Mudah (energi 1.5%/detik, kecepatan x0.85, deteksi x0.80), Normal (2.0%/detik, x1.00, x1.00), "
                "dan Sulit (2.7%/detik, x1.15, x1.25). Nilai dipilih di panel PENGATURAN, disimpan di PlayerPrefs, "
                "dan diterapkan saat misi dimulai.",
                False,
            ),
        ],
    )

    insert_rich_after(
        difficulty,
        body_template,
        [
            ("Hasil Akhir, Gelar, dan Rekor. ", True),
            (
                "Saat Victory, GameManager mencatat waktu tempuh, nyawa, dan sisa energi. Gelar: Penyuci Agung "
                "(waktu <= 2:30 dan nyawa 3/3), Murid Teladan (waktu <= 4:00 dan nyawa >= 2/3), Pejalan Malam "
                "(selain kondisi tersebut). Waktu terbaik disimpan di PlayerPrefs dan ditampilkan sebagai rekor. "
                "Save progres tidak diimplementasikan karena sesi dapat diselesaikan dalam hitungan menit.",
                False,
            ),
        ],
    )

    # MDA
    mda = doc.tables[4]
    mechanics_cell = mda.rows[1].cells[1]
    p = mechanics_cell.add_paragraph(
        "5. Mekanik Rwa Bhineda Exposure: radius deteksi musuh = detectRadius x pengali kesulitan x Lerp(0.7, 1.3, energi/100). "
        "6. Tiga tingkat kesulitan mengubah laju energi, kecepatan, dan deteksi musuh. "
        "7. Gelar akhir dan rekor waktu dihitung saat Victory; pengaturan, kesulitan, dan rekor disimpan via PlayerPrefs."
    )
    p.paragraph_format.space_before = 0

    dynamics_cell = mda.rows[2].cells[1]
    dynamics_cell.add_paragraph(
        "3. Negosiasi Terang-Gelap: mempertahankan lentera terang memperluas pandangan tetapi memperbesar "
        "jangkauan deteksi musuh; membiarkan lentera redup menyamarkan posisi tetapi mempersempit navigasi."
    )

    aesthetics_cell = mda.rows[3].cells[1]
    aesthetics_cell.add_paragraph(
        "3. Mastery & Replayability: gelar akhir, rekor waktu, dan tiga tingkat kesulitan mendorong pemain "
        "mengulang misi dengan strategi cahaya yang berbeda."
    )

    # 4.1 diagram (tabel bersarang)
    fsm_diagram = doc.tables[7].rows[1].cells[0].tables[0]
    for paragraph in fsm_diagram.rows[0].cells[0].paragraphs:
        replace_in_paragraph(paragraph, "Playing", "Playing ↔ Paused")

    # 4.2 tabel state: sisipkan Paused setelah Playing
    state_table = doc.tables[8]
    playing_row = state_table.rows[3]
    new_tr = copy.deepcopy(playing_row._tr)
    playing_row._tr.addnext(new_tr)
    new_row = state_table.rows[4]
    set_cell_text(new_row.cells[1], "Paused")
    set_cell_text(new_row.cells[2], "Pemain menekan Esc saat Playing.")
    set_cell_text(
        new_row.cells[3],
        "Time.timeScale = 0; panel Jeda tampil (Lanjutkan, Pengaturan, Ke Menu Utama); "
        "Esc melanjutkan permainan.",
    )

    # 6.2 user flow (tabel bersarang)
    flow = doc.tables[12].rows[1].cells[0].tables[0].rows[0]
    for paragraph in flow.cells[2].paragraphs:
        replace_in_paragraph(paragraph, "HUD Gameplay Aktif", "HUD Gameplay + Jeda (ESC)")
        replace_in_paragraph(paragraph, "Eksplorasi, Stun Bayangan, & Ambil 3 Lontar", "Eksplorasi, Stun, Ambil Lontar; ESC membuka Jeda")
    for paragraph in flow.cells[4].paragraphs:
        replace_in_paragraph(paragraph, "Layar Victory / Game Over", "Layar Victory / Game Over + Gelar")
        replace_in_paragraph(paragraph, "Tombol “Main Lagi”", "Waktu, nyawa, energi, rekor; Main Lagi")

    # Catatan setelah bagan user flow
    note_template = doc.paragraphs[34]
    note = copy.deepcopy(note_template._p)
    doc.tables[12]._tbl.addnext(note)
    note_p = Paragraph(note, note_template._parent)
    clear_runs(note_p)
    note_p.add_run(
        "Selain alur utama, Main Menu menyediakan CARA BERMAIN, PENGATURAN (slider BGM/SFX, layar penuh, "
        "tiga tingkat kesulitan), dan KREDIT (atribusi aset). Saat bermain, ESC membuka panel JEDA; dari panel "
        "tersebut pemain dapat membuka Pengaturan atau kembali ke menu utama."
    )

    # 6.3 wireframe
    wire = doc.tables[13].rows[0].cells[0].tables[0].rows[0]
    for paragraph in wire.cells[1].paragraphs:
        replace_in_paragraph(paragraph, "ENERGI LENTERA:", "ENERGI LENTERA:")
        if "CAHAYA:" not in paragraph.text:
            run = paragraph.add_run("  |  CAHAYA: TERANG (+30%)")
            run.bold = True
    for paragraph in wire.cells[2].paragraphs:
        if "WAKTU" not in paragraph.text:
            run = paragraph.add_run("  |  WAKTU 00:42")
            run.bold = True
    bottom = doc.tables[13].rows[2].cells[0].tables[0].rows[0]
    for paragraph in bottom.cells[0].paragraphs:
        replace_in_paragraph(
            paragraph,
            "[SPACE] Pancaran Cahaya Suci (Siap!)",
            "[SPACE] Pancaran Cahaya Suci (Siap!)  |  [ESC] Jeda",
        )

    # 8.1 managers
    for paragraph in doc.paragraphs:
        if paragraph.text.startswith("Assets/_Project/Scripts/Managers/"):
            replace_in_paragraph(
                paragraph,
                "Berisi GameManager.cs dan AudioManager.cs.",
                "Berisi GameManager.cs, AudioManager.cs, UIManager.cs, dan DifficultySettings.cs.",
            )

    # 8.2 roadmap
    paragraphs = doc.paragraphs
    intro = next(p for p in paragraphs if p.text.startswith("Prototipe ini dirancang agar dapat langsung"))
    set_text = "Versi final prototipe ini menyatukan seluruh fitur Tugas 2 dengan lima pengembangan Tugas 3, sekaligus menetapkan arah ekspansi berikutnya:"
    replace_in_paragraph(intro, intro.text, set_text)

    item1 = next(p for p in doc.paragraphs if p.text.startswith("Penambahan 3 Level Berbeda"))
    replace_in_paragraph(
        item1,
        item1.text,
        "Fitur final yang telah diimplementasikan: menu Pengaturan & Jeda (volume BGM/SFX, layar penuh, "
        "tiga tingkat kesulitan), layar Kredit, Mekanik Rwa Bhineda Exposure, serta hasil akhir dengan gelar "
        "dan rekor waktu.",
    )

    item2 = next(p for p in doc.paragraphs if p.text.startswith("Implementasi Fitur Lanjutan"))
    replace_in_paragraph(
        item2,
        item2.text,
        "Keputusan desain — Save System tidak diimplementasikan: sesi permainan dapat diselesaikan dalam "
        "±2 menit sehingga penyimpanan progres tidak memberi nilai tambah. Persistensi dibatasi pada pengaturan, "
        "kesulitan, dan rekor waktu melalui PlayerPrefs.",
    )

    item3 = next(p for p in doc.paragraphs if p.text.startswith("Ekspor Lintas Platform"))
    replace_in_paragraph(
        item3,
        item3.text,
        "Ekspansi berikutnya: Level 2 (Hutan Bambu Lemah Tulis) dan Level 3 (Pelataran Setra Gandamayu) dengan "
        "kurva kesulitan progresif; save progres relevan setelah jumlah level bertambah; serta ekspor Android "
        "dengan virtual joystick.",
    )

    insert_rich_after(
        item3,
        item3,
        [
            ("Verifikasi final: ", True),
            (
                "40/40 assertion play-mode PASS; build macOS (.app) dan Windows (.exe) berhasil; build macOS "
                "dijalankan dan berjalan normal (19 November 2026).",
                False,
            ),
        ],
    )

    doc.save(DOCX_PATH)
    print("[DOCX] OK")


def verify():
    with open(HTML_PATH, encoding="utf-8") as handle:
        html = handle.read()

    doc = Document(DOCX_PATH)

    def all_text():
        chunks = [p.text for p in doc.paragraphs]

        def walk(tables):
            for table in tables:
                for row in table.rows:
                    for cell in row.cells:
                        chunks.extend(p.text for p in cell.paragraphs)
                        if cell.tables:
                            walk(cell.tables)

        walk(doc.tables)
        return "\n".join(chunks)

    text = all_text()

    required_html = ["Spesifikasi Tiga Mekanik", "Rwa Bhineda Exposure", "Penyuci Agung", "Paused", "40/40"]
    required_docx = ["Spesifikasi Tiga Mekanik", "Rwa Bhineda Exposure", "Penyuci Agung", "Paused", "40/40"]

    for item in required_html:
        if item not in html:
            raise SystemExit(f"[VERIFY] HTML tidak memuat: {item}")

    for item in required_docx:
        if item not in text:
            raise SystemExit(f"[VERIFY] DOCX tidak memuat: {item}")

    if "Spesifikasi Dua Mekanik" in html or "Spesifikasi Dua Mekanik" in text:
        raise SystemExit("[VERIFY] Judul lama masih ada")

    print(f"[VERIFY] HTML/DOCX OK; paragraf DOCX={len(doc.paragraphs)}; tabel DOCX={len(doc.tables)}")


if __name__ == "__main__":
    apply_html()
    apply_docx()
    verify()
