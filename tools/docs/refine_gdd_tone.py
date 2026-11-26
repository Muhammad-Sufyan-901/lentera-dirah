#!/usr/bin/env python3
"""Penyempurnaan Bahasa GDD (HTML + DOCX):
Mengubah bahasa dokumen menjadi lebih natural ('gaya mahasiswa'),
komunikatif, tidak kaku, dan tidak terlalu teknis/kode-sentris,
tanpa mengubah substansi gameplay, nilai parameter, maupun kelengkapan data.
"""

import copy
import os
import re

from docx import Document
from docx.text.paragraph import Paragraph

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.path.join(ROOT, "docs")
DOCX_PATH = os.path.join(BASE, "gdd", "230030309_Muhammad_Sufyan_Game_Design_Document_GDD_Lentera_Dirah.docx")
HTML_PATH = os.path.join(BASE, "html", "230030309_Muhammad_Sufyan_Game_Design_Document_GDD_Lentera_Dirah.html")


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


def apply_html():
    with open(HTML_PATH, encoding="utf-8") as handle:
        html = handle.read()

    def swap(old, new, label):
        nonlocal html
        if old not in html:
            raise SystemExit(f"[HTML] Anchor gagal: {label}")
        html = html.replace(old, new, 1)

    # 1.1 Target Platform wording
    swap(
        "<i>siap diekspansi ke Android (<code>.apk</code>) pada Proyek Akhir (UAS)</i>",
        "<i>siap diekspansi ke platform mobile (Android <code>.apk</code>) pada tahap pengembangan lanjutan</i>",
        "1.1 target platform",
    )

    # 1.2 High Concept & Ringkasan Premis
    swap(
        "<b>High Concept:</b> Jelajahi kegelapan malam Desa Girah sebagai Bahula (murid Mpu Bharada), kelola energi cahaya Lentera Suci untuk menenangkan roh Bayangan Wabah, dan kumpulkan 3 naskah Lontar kuno ke Altar Penyucian untuk mengembalikan keseimbangan <i>Rwa Bhineda</i>.",
        "<b>High Concept:</b> Mengusung konsep petualangan bernuansa budaya dan aksi tanpa kekerasan, pemain mengendalikan Bahula (murid Mpu Bharada) menjelajahi malam gelap Desa Girah berbekal Lentera Suci untuk menenangkan roh bayangan wabah serta menyucikan kembali desa dengan mengumpulkan naskah-naskah lontar kuno.",
        "1.2 high concept",
    )

    swap(
        "<b>Ringkasan Premis:</b> Kabut wabah dari Setra Gandamayu telah menyelimuti Desa Girah. Mpu Bharada mengutus muridnya, Bahula, masuk ke jantung desa dengan berbekal sebuah Lentera Suci. Berbeda dari game aksi konvensional, pemain tidak menggunakan kekerasan fisik, melainkan mengandalkan manajemen cahaya lentera untuk membuka jarak pandang di tengah kegelapan dan melepaskan gelombang cahaya suci (<i>Holy Light Burst</i>) guna meredam Bayangan Wabah sembari mencari 3 Lontar Kuno (<i>Lontar Usada</i>, <i>Lontar Dharma</i>, dan <i>Lontar Rwa Bhineda</i>).",
        "<b>Ringkasan Premis:</b> Kabut wabah misterius dari Setra Gandamayu telah menyelimuti wilayah Desa Girah dan sekitarnya. Mpu Bharada mengutus murid kepercayaannya, Bahula, untuk memulihkan keseimbangan alam sesuai filosofi <i>Rwa Bhineda</i>. Berbeda dari game laga pada umumnya, pemain tidak dibekali senjata fisik, melainkan mengandalkan Lentera Suci. Tantangan utama terletak pada pengelolaan energi cahaya: lentera yang menyala terang membuka pandangan namun menarik perhatian musuh, sedangkan lentera yang redup dapat menyamarkan langkah pemain. Pemain harus menyusuri tiga wilayah (Desa Girah, Hutan Bambu Lemah Tulis, dan Pelataran Setra Gandamayu), melumpuhkan roh bayangan dengan pancaran cahaya suci (<i>Holy Light Burst</i>), serta mengembalikan naskah-naskah Lontar Suci ke Altar Penyucian.",
        "1.2 premis",
    )

    # 2.1 Core Loop Intro
    swap(
        "Berdasarkan prinsip <i>Systems Analysis &amp; Design</i> untuk permainan digital, siklus aksi berulang (<i>Core Loop</i>) yang menjadi jantung gameplay <i>&ldquo;Lentera Dirah&rdquo;</i> terdiri atas 4 tahapan yang saling terhubung:",
        "Dalam perancangan game <i>&ldquo;Lentera Dirah&rdquo;</i>, siklus utama permainan (<i>Core Loop</i>) dibangun dari 4 tahapan aksi yang saling terhubung secara berkesinambungan:",
        "2.1 core loop intro",
    )

    # 2.2 MDA Framework Header & Content
    swap(
        "<td><b>Mechanics</b><br><i>(Aturan &amp; Komponen Dasar Kode)</i></td>",
        "<td><b>Mechanics</b><br><i>(Aturan dan Mekanik Permainan)</i></td>",
        "2.2 MDA header mechanics",
    )

    swap(
        """            1. Pergerakan karakter 4 arah berbasis komponen fisika <code>Rigidbody2D</code> (kecepatan = <code>4.5 unit/detik</code>).<br>
            2. Penyusutan energi lentera (<i>Light Decay</i>) sebesar <code>2% per detik</code> yang memperkecil radius <code>Light 2D</code>.<br>
            3. Mekanik <i>Holy Light Burst</i> (tombol <code>Space</code>) dengan biaya energi lentera <code>15%</code>, <i>cooldown</i> <code>4 detik</code>, dan radius deteksi <code>Physics2D.OverlapCircle</code> sebesar <code>3.5 unit</code>.<br>
            4. Syarat buka segel Altar Penyucian: variabel <code>lontarCollected == 3</code>.<br>
            5. Mekanik <i>Rwa Bhineda Exposure</i>: radius deteksi musuh = <code>detectRadius &times; pengali kesulitan &times; Lerp(0.7, 1.3, energi/100)</code>.<br>
            6. Tiga tingkat kesulitan (Mudah, Normal, Sulit) mengubah laju energi, kecepatan, dan deteksi musuh.<br>
            7. Gelar akhir dan rekor skor dihitung saat level selesai; pengaturan, kesulitan, dan rekor disimpan via <code>PlayerPrefs</code>.<br>
            8. Tiga level (Desa Girah, Hutan Bambu Lemah Tulis, Pelataran Setra Gandamayu) diaktifkan oleh <code>LevelManager</code>; skor diakumulasikan dan rekor disimpan setelah level 3.""",
        """            1. <b>Navigasi 4 Arah:</b> Karakter Bahula dapat diarahkan ke atas, bawah, kiri, dan kanan secara seimbang dan responsif (kecepatan gerak 4.5 meter/detik).<br>
            2. <b>Penyusutan Lentera (<i>Light Decay</i>):</b> Energi lentera menyusut perlahan sebesar 2% per detik, membuat lingkaran cahaya lentera menyusut dari radius 6.0 meter hingga minimal 1.8 meter.<br>
            3. <b>Pancaran Cahaya Suci (<i>Holy Light Burst</i>):</b> Pemain dapat menekan tombol Spasi untuk melumpuhkan roh bayangan di sekitar (radius 3.5 meter) selama 3 detik, menghabiskan 15% energi dengan jeda pengisian kembali (<i>cooldown</i>) 4 detik.<br>
            4. <b>Penyucian Altar:</b> Segel pelindung Altar di tengah area hanya akan terbuka setelah pemain mengumpulkan 3 naskah Lontar Suci pada level tersebut.<br>
            5. <b>Keseimbangan Cahaya (<i>Rwa Bhineda Exposure</i>):</b> Terang lentera memengaruhi kewaspadaan musuh secara dinamis (lentera terang membuat deteksi musuh bertambah hingga +30%, sedangkan lentera redup menyamarkan pemain hingga -30%).<br>
            6. <b>Tiga Tingkat Kesulitan:</b> Pilihan mode Mudah, Normal, dan Sulit yang memodifikasi daya tahan lentera, kelincahan musuh, serta pengali perolehan skor akhir.<br>
            7. <b>Penilaian Skor &amp; Gelar:</b> Performa tiap level dinilai dari waktu tempuh, sisa nyawa, dan sisa energi yang menghasilkan gelar (<i>Penyuci Agung</i>, <i>Murid Teladan</i>, atau <i>Pejalan Malam</i>) serta mencatat rekor skor tertinggi.<br>
            8. <b>Tiga Wilayah Petualangan:</b> Permainan tersusun dari 3 level berurutan (Desa Girah, Hutan Bambu Lemah Tulis, dan Pelataran Setra Gandamayu) dengan akumulasi skor total.""",
        "2.2 MDA mechanics content",
    )

    swap(
        """            1. <b>Dilema Manajemen Sumber Daya Cahaya:</b> Pemain harus menimbang kapan harus menghemat energi lentera agar pandangan tetap luas, dan kapan harus mengorbankan 15% energi lentera untuk melakukan <i>Stun</i> saat terkepung musuh.<br>
            2. <b>Navigasi Taktis (Risk vs. Reward):</b> Mengambil Lontar di sudut sempit menuntut pemain mengamati pola gerak <i>Patrol</i> NPC Bayangan terlebih dahulu.<br>
            3. <b>Negosiasi Terang&ndash;Gelap:</b> Mempertahankan lentera terang memperluas pandangan tetapi memperbesar jangkauan deteksi musuh; membiarkan lentera redup menyamarkan posisi tetapi mempersempit navigasi.""",
        """            1. <b>Dilema Manajemen Energi Cahaya:</b> Pemain terus menimbang kapan harus mempertahankan lentera tetap terang agar jalan terlihat jelas, dan kapan harus mengorbankan energi demi melumpuhkan musuh saat terdesak.<br>
            2. <b>Navigasi Taktis &amp; Pengamatan Pola (Risk vs. Reward):</b> Untuk mengambil Lontar dan Minyak di lorong sempit, pemain dituntut bersabar mengamati rute patroli roh bayangan terlebih dahulu sebelum melangkah masuk.<br>
            3. <b>Taktik Menyelinap dalam Temaram:</b> Membiarkan lentera agak redup memberi keuntungan taktis karena musuh lebih sulit melihat Bahula, namun pemain harus berani melangkah dengan jarak pandang terbatas.""",
        "2.2 MDA dynamics",
    )

    swap(
        """            1. <b>Tension &amp; Relief (Ketegangan &amp; Kelegaan):</b> Atmosfer tegang saat menyusuri kegelapan malam diiringi gamelan Bali, diikuti rasa lega saat menemukan pancaran cahaya Lontar Suci.<br>
            2. <b>Cultural Immersion (Penghayatan Budaya):</b> Pengalaman menyelami filosofi <i>Rwa Bhineda</i> secara langsung melalui kontras cahaya dan bayangan.<br>
            3. <b>Mastery &amp; Replayability:</b> Gelar akhir, rekor skor, dan tiga tingkat kesulitan mendorong pemain mengulang level dengan strategi cahaya yang berbeda.""",
        """            1. <b>Tension &amp; Relief (Ketegangan &amp; Kelegaan):</b> Sensasi tegang saat menyusuri malam gelap diiringi alunan gamelan Bali, yang berganti menjadi rasa lega dan puas saat berhasil menemukan pendar cahaya Lontar Suci atau menyucikan Altar.<br>
            2. <b>Cultural Immersion (Penghayatan Budaya Bali):</b> Mengajak pemain merasakan nilai filosofi <i>Rwa Bhineda</i> secara langsung lewat dinamika cahaya dan bayangan, serta keanggunan visual naskah lontar dan pura tradisional Bali.<br>
            3. <b>Mastery &amp; Replayability (Kepuasan Penguasaan Tantangan):</b> Variasi tingkat kesulitan, perhitungan skor terperinci, dan gelar kehormatan memotivasi pemain untuk mengulang permainan dengan catatan waktu dan strategi yang lebih baik.""",
        "2.2 MDA aesthetics",
    )

    # 3.1 Skema Kontrol
    swap(
        '<th style="width: 50%;" bgcolor="#e8eef5">Implementasi Teknis di Unity 2D</th>',
        '<th style="width: 50%;" bgcolor="#e8eef5">Respon dan Perilaku Sistem</th>',
        "3.1 kontrol th",
    )
    swap(
        '<td>Membaca <code>Input.GetAxisRaw("Horizontal")</code> dan <code>Input.GetAxisRaw("Vertical")</code>, dinormalisasi dengan <code>vector.normalized</code> agar gerak diagonal konsisten, lalu diterapkan pada <code>Rigidbody2D.linearVelocity</code> di dalam <code>FixedUpdate()</code>.</td>',
        '<td>Menggerakkan karakter Bahula ke empat arah mata angin secara responsif. Kecepatan diagonal diselaraskan secara proporsional agar karakter bergerak stabil dan tidak meluncur lebih cepat saat bergerak miring.</td>',
        "3.1 kontrol gerak",
    )
    swap(
        '<td>Mengecek <code>Input.GetKeyDown(KeyCode.Space)</code>. Jika <code>lanternEnergy &gt;= 15f</code> dan <code>cooldownTimer &lt;= 0f</code>, memicu kilatan cahaya dan mengubah state seluruh objek ber-tag/layer <code>Enemy</code> dalam radius <code>3.5f</code> menjadi <code>Stunned</code>.</td>',
        '<td>Melepaskan kilatan cahaya suci sesaat yang melumpuhkan seluruh roh bayangan di sekitar pemain (radius 3.5 meter) selama 3 detik. Aksi ini membutuhkan minimal 15% energi lentera dengan jeda pengisian (<i>cooldown</i>) 4 detik.</td>',
        "3.1 kontrol burst",
    )
    swap(
        '<td>Event <code>Button.onClick</code> pada Canvas UI untuk mengubah state pada <code>GameManager</code> (dari <code>MainMenu</code> ke <code>IntroDialog</code>, lalu ke <code>Playing</code>).</td>',
        '<td>Digunakan untuk memilih tombol antarmuka layar serta melanjutkan percakapan dialog wejangan dari Mpu Bharada.</td>',
        "3.1 kontrol interaksi",
    )
    swap(
        '<td><code>GameManager.Pause()</code> menyetel <code>Time.timeScale = 0</code> dan state menjadi <code>Paused</code>; panel Jeda menampilkan Lanjutkan, Pengaturan, dan Ke Menu Utama. Slider volume, layar penuh, serta pilihan kesulitan disimpan melalui <code>PlayerPrefs</code>.</td>',
        '<td>Menjeda permainan seketika (seluruh gerakan dan waktu dibekukan), menampilkan panel Jeda dengan opsi melanjutkan petualangan, mengatur volume audio/layar penuh, atau kembali ke menu utama.</td>',
        "3.1 kontrol jeda",
    )

    # 3.2 Collision Table
    swap(
        '<th style="width: 18%;" bgcolor="#e8eef5">Tipe Collider 2D</th>',
        '<th style="width: 18%;" bgcolor="#e8eef5">Jenis Interaksi Fisik</th>',
        "3.2 collision th1",
    )
    swap(
        '<th style="width: 38%;" bgcolor="#e8eef5">Respon Sistem &amp; Efek Gameplay</th>',
        '<th style="width: 38%;" bgcolor="#e8eef5">Respon Interaksi dalam Permainan</th>',
        "3.2 collision th2",
    )
    swap(
        '<td>Menahan pergerakan fisik objek menggunakan <code>BoxCollider2D</code> dan <code>Tilemap&#8203;Collider2D</code> agar tidak menembus batas lingkungan desa.</td>',
        '<td>Membatasi gerak fisik pemain dan musuh agar tidak dapat menembus pagar batu, pepohonan, gapura candi bentar, dan bangunan suci desa.</td>',
        "3.2 collision dinding",
    )
    swap(
        '<td>Menambah <code>lontarCount (+1)</code>, menampilkan pesan edukasi lontar di HUD, memutar SFX genta (<code>sfx_pickup_lontar</code>), dan memanggil <code>Destroy(gameObject)</code>.</td>',
        '<td>Lontar otomatis terambil saat disentuh pemain, menambah jumlah lontar di tampilan layar (HUD), memainkan denting genta suci, menampilkan petuah budaya, dan lontar menghilang dari peta.</td>',
        "3.2 collision lontar",
    )
    swap(
        '<td>Menambah energi lentera sebesar <code>+35%</code> (maksimal <code>100%</code>), memperluas radius <code>Light 2D</code>, dan memutar SFX api obor.</td>',
        '<td>Mengisi ulang energi lentera sebesar +35% (maksimal 100%), memperluas kembali lingkaran terang lentera, dan memainkan efek suara percikan api obor.</td>',
        "3.2 collision minyak",
    )
    swap(
        '<td>Jika state musuh bukan <code>Stunned</code>, mengurangi nyawa pemain (<code>health - 1</code>), mengaktifkan state <code>Hurt</code> (kebal sementara 1 detik), dan memutar <code>sfx_hurt</code>.</td>',
        '<td>Bila roh bayangan sedang aktif (tidak membeku), sentuhan musuh akan mengurangi 1 nyawa pemain, memicu efek kebal sementara selama 1 detik (sprite Bahula berkedip merah), dan memainkan efek suara benturan.</td>',
        "3.2 collision musuh",
    )
    swap(
        '<td>Mengecek apakah <code>lontarCount == 3</code>. Jika terpenuhi, memutar <code>sfx_victory</code> dan mengubah Game State menjadi <code>Victory</code>.</td>',
        '<td>Mengecek kelengkapan 3 Lontar Suci pada level tersebut. Jika lengkap, altar menyala keemasan, memainkan tabuhan kemenangan, dan menyelesaikan level.</td>',
        "3.2 collision altar",
    )

    # 3.3 Mekanik 2 & 3 text
    swap(
        "Karakter Bahula dilengkapi komponen <code>Light 2D (Point Light)</code> yang radius terangnya berbanding lurus dengan persentase energi lentera (pada energi <code>100%</code> radius luar adalah <code>6.0 unit</code>; menyusut perlahan hingga minimal <code>1.8 unit</code>). Apabila energi lentera mencapai <code>0%</code>, kegelapan menyelimuti pemain sepenuhnya dan memicu kondisi kalah (<i>Game Over</i>). Pemain dapat menekan tombol <code>Space</code> untuk melepaskan pancaran cahaya suci yang membekukan (<i>Stun</i>) seluruh NPC Bayangan Wabah di sekitarnya selama 3 detik.",
        "Karakter Bahula dibekali Lentera Suci yang memancarkan lingkaran cahaya dinamis. Luas pandangan ini bergantung langsung pada sisa energi lentera: saat energi terisi penuh (100%), cahaya menerangi area hingga radius 6 meter, lalu perlahan menyusut hingga tersisa 1.8 meter saat energi menipis. Bila energi sampai habis (0%), kegelapan malam seketika menelan Bahula dan permainan berakhir (<i>Game Over</i>). Untuk menyelamatkan diri saat terpojok, pemain dapat menekan tombol Spasi untuk melepaskan gelombang cahaya suci (<i>Holy Light Burst</i>) yang membekukan seluruh roh bayangan di sekitarnya selama 3 detik.",
        "3.3 mekanik 2",
    )

    swap(
        """        Energi lentera tidak hanya menentukan luas pandangan, tetapi juga tingkat keterlihatan Bahula. Radius deteksi efektif Bayangan Wabah dihitung sebagai
        <code>detectRadius &times; pengali kesulitan &times; Lerp(0.7, 1.3, energi/100)</code>.
        Pada energi <code>100%</code> musuh mendeteksi hingga <b>30% lebih jauh</b>; pada energi rendah deteksi menyusut hingga <b>30%</b>, sehingga lentera redup berfungsi sebagai penyamaran. HUD menampilkan status <code>CAHAYA: TERANG / SEIMBANG / REDUP</code> beserta persentase deteksi saat ini. Mekanik ini menjadikan <i>Light Decay</i> sebagai keputusan taktis, bukan sekadar pengatur waktu.""",
        """        Energi lentera memiliki fungsi ganda yang merefleksikan filosofi <i>Rwa Bhineda</i>: lentera tidak hanya menerangi jalan, melainkan memengaruhi seberapa mudah Bahula dilihat oleh musuh. Saat lentera menyala terang (energi tinggi), roh bayangan dapat melihat keberadaan Bahula dari jarak yang lebih jauh (hingga +30%). Sebaliknya, saat lentera dibiarkan meredup (energi rendah), langkah Bahula menjadi lebih tersamarkan (jarak deteksi musuh turun hingga -30%). Pemain dapat memantau kondisi ini secara langsung lewat indikator pada layar (<i>CAHAYA: TERANG / SEIMBANG / REDUP</i>). Dengan mekanisme ini, penyusutan lentera tidak lagi sekadar batas waktu, melainkan elemen taktis di mana pemain bisa sengaja bermain sembunyi-sembunyi (<i>stealth</i>) di area yang temaram.""",
        "3.3 mekanik 3",
    )

    # 4.1 FSM intro
    swap(
        "Untuk menjamin struktur kode yang bersih, bebas <i>bug</i>, dan memenuhi indikator penilaian tertinggi pada kriteria <i>State Management</i>, permainan ini mengimplementasikan pola <b>Finite State Machine (FSM)</b> berbasis <code>enum</code> pada 3 tingkatan:",
        "Untuk mengatur alur permainan, aksi karakter, dan perilaku musuh agar berjalan teratur serta mudah dikembangkan, game ini menerapkan sistem <b>Finite State Machine (FSM)</b> yang dibagi ke dalam 3 tingkatan hierarki:",
        "4.1 FSM intro",
    )

    # 4.2 FSM Table Descriptions
    swap(
        '<th style="width: 32%;" bgcolor="#e8eef5">Kondisi Pemicu Transisi (Trigger)</th>',
        '<th style="width: 32%;" bgcolor="#e8eef5">Kondisi Pemicu Transisi</th>',
        "4.2 th trigger",
    )
    swap(
        '<th style="width: 32%;" bgcolor="#e8eef5">Perilaku Sistem pada State Tersebut</th>',
        '<th style="width: 32%;" bgcolor="#e8eef5">Perilaku Karakter / Sistem</th>',
        "4.2 th perilaku",
    )
    swap(
        "<td>Menampilkan panel judul utama; input karakter dinonaktifkan.</td>",
        "<td>Menampilkan judul utama game dan menu (Mulai Bermain, Cara Bermain, Pengaturan, Kredit, Keluar). Karakter belum dapat digerakkan.</td>",
        "4.2 MainMenu",
    )
    swap(
        "<td>Menampilkan halaman Pilih Kesulitan (Mudah/Normal/Sulit) beserta pengali skor; pilihan disimpan di <code>PlayerPrefs</code>.</td>",
        "<td>Membuka halaman pemilihan tingkat kesulitan (Mudah, Normal, Sulit) lengkap dengan penjelasan perbedaan tantangan dan pengali skor.</td>",
        "4.2 DifficultySelect",
    )
    swap(
        "<td>Menampilkan dialog instruksi Mpu Bharada kepada Bahula.</td>",
        "<td>Menampilkan kotak percakapan wejangan dan instruksi misi suci dari Mpu Bharada kepada Bahula sebelum memasuki area permainan.</td>",
        "4.2 IntroDialog",
    )
    swap(
        "<td>Pemain menutup dialog pembuka.</td>",
        "<td>Pemain selesai membaca dialog pembuka atau memulai level berikutnya.</td>",
        "4.2 Playing trigger",
    )
    swap(
        "<td>Mengaktifkan kontrol pemain, AI patroli musuh, dan pengurangan energi lentera.</td>",
        "<td>Permainan aktif: pemain dapat mengontrol gerak Bahula, roh bayangan mulai berpatroli, dan energi lentera menyusut secara bertahap.</td>",
        "4.2 Playing behavior",
    )
    swap(
        "<td><code>Time.timeScale = 0</code>; panel Jeda tampil (Lanjutkan, Pengaturan, Ke Menu Utama); <code>Esc</code> melanjutkan permainan.</td>",
        "<td>Permainan berhenti sementara (seluruh gerakan dan waktu dibekukan), memunculkan menu jeda dengan opsi Lanjutkan, Pengaturan, atau kembali ke Menu Utama.</td>",
        "4.2 Paused",
    )
    swap(
        "<td>Menghitung skor level dan skor total, memutar audio kemenangan, lalu menampilkan halaman hasil dengan tombol Level Berikutnya (level 1–2) atau Selesai (level 3).</td>",
        "<td>Level selesai: roh bayangan berhenti mengejar, audio kemenangan berbunyi, dan muncul layar hasil dengan skor, gelar, serta opsi lanjut ke level berikutnya.</td>",
        "4.2 Victory",
    )
    swap(
        "<td>Menampilkan layar gagal dengan skor total, tombol Coba Lagi (mengulang level saat ini), dan Menu Utama.</td>",
        "<td>Layar kekalahan muncul saat nyawa Bahula habis atau lentera padam, menampilkan skor total yang sempat diraih serta tombol Coba Lagi untuk mengulang level tersebut.</td>",
        "4.2 GameOver",
    )

    # Player Controller States in 4.2
    swap(
        "<td>Kecepatan <code>Rigidbody2D</code> diset ke nol; memainkan animasi <i>Idle</i> sesuai arah hadap.</td>",
        "<td>Karakter berdiri diam di tempat sambil tetap menghadap ke arah terakhir, siap menerima perintah gerak selanjutnya.</td>",
        "4.2 Idle",
    )
    swap(
        "<td>Menggerakkan karakter dan memainkan animasi langkah kaki 4 arah.</td>",
        "<td>Karakter melangkah secara halus ke arah yang ditekan sambil memainkan animasi berjalan 4 arah.</td>",
        "4.2 Walking",
    )
    swap(
        "<td>Meningkatkan intensitas &amp; radius <code>Light 2D</code> sesaat (0.3 detik) dan memicu efek <i>Stun</i> ke musuh.</td>",
        "<td>Lentera memancarkan kilau suci sesaat yang memperluas cahaya dan membekukan roh bayangan terdekat selama 3 detik.</td>",
        "4.2 CastingLight",
    )
    swap(
        "<td>Sprite karakter berkedip merah dan kebal sementara (<i>invulnerability</i>) selama 1 detik.</td>",
        "<td>Karakter kehilangan 1 nyawa, berkedip merah, dan memperoleh status kebal sementara selama 1 detik.</td>",
        "4.2 Hurt",
    )

    # Enemy AI States in 4.2
    swap(
        "<td>NPC bergerak otomatis menyusuri titik <code>waypoints[]</code> dengan kecepatan normal (<code>2.2 unit/detik</code>).</td>",
        "<td>Roh bayangan berpatroli secara otomatis bolak-balik menyusuri rute ronda yang ditentukan dengan kecepatan santai (2.2 meter/detik).</td>",
        "4.2 Patrol",
    )
    swap(
        "<td>NPC mengejar posisi pemain dengan kecepatan <code>3.4 unit/detik</code>; kembali ke <code>Patrol</code> jika jarak <code>&gt; 5.5 unit</code>.</td>",
        "<td>Roh bayangan berubah agresif dan bergerak mengejar Bahula dengan kecepatan tinggi (3.4 meter/detik); musuh kembali berpatroli jika Bahula berhasil menjauh.</td>",
        "4.2 Chase",
    )
    swap(
        "<td>NPC berhenti bergerak selama <code>3.0 detik</code>, warna sprite berubah biru pucat transparan, dan tidak melukai pemain.</td>",
        "<td>Roh bayangan membeku diam di tempat selama 3 detik, warna tubuhnya berubah biru pucat transparan, dan tidak dapat melukai pemain.</td>",
        "4.2 Stunned",
    )

    # 5.2 Prinsip Animasi Dasar
    swap(
        "Karakter Bahula dan NPC Bayangan memiliki siklus animasi jalan 4 arah (Atas, Bawah, Kiri, Kanan) menggunakan <code>Animator Controller</code> dengan 8 klip state (Idle dan Walking untuk 4 arah) yang dipanggil melalui <code>Animator.Play</code> sesuai arah hadap, tanpa <i>Blend Tree</i> agar transisi deterministik.",
        "Karakter Bahula dan roh bayangan dilengkapi siklus animasi langkah kaki 4 arah (atas, bawah, kiri, dan kanan). Pergantian animasi diam (<i>idle</i>) dan melangkah (<i>walking</i>) berganti secara responsif dan tegas sesuai arah gerak pemain agar animasi karakter terasa lincah dan tidak kaku.",
        "5.2 walk cycle",
    )
    swap(
        "Objek <code>LontarSuci</code> dan <code>MinyakObor</code> bergerak mengambang naik-turun secara berirama menggunakan fungsi trigonometri <code>Mathf.Sin(Time.time * frequency) * amplitude</code> sehingga terlihat hidup dan menarik perhatian pemain.",
        "Objek naskah Lontar Suci dan guci Minyak Obor dirancang melayang naik-turun secara berirama dan halus. Efek visual ini membuat artefak budaya tersebut tampak hidup dan langsung memikat perhatian pemain di tengah area yang temaram.",
        "5.2 floating",
    )
    swap(
        "Saat pemain menekan <code>Space</code> (<i>Holy Light Burst</i>), radius cahaya membesar secara cepat lalu kembali ke ukuran semula, disertai perubahan warna musuh yang terkena efek <i>Stun</i>.",
        "Ketika pemain melepaskan semburan cahaya suci (<i>Holy Light Burst</i>), lentera memancarkan kilatan membesar sesaat sebelum kembali normal, disertai reaksi visual pada roh bayangan yang seketika berubah warna menjadi biru transparan sebagai tanda musuh telah dilumpuhkan.",
        "5.2 visual feedback",
    )

    # 6.1 UI/UX
    swap(
        "Mengingat latar permainan bernuansa malam gelap, seluruh indikator vital pada <i>Heads-Up Display</i> (Nyawa, Bar Energi Lentera, dan Jumlah Lontar) menggunakan warna emas menyala (<code>#FFB84D</code>) di atas panel gelap agar terbaca secara instan tanpa menghalangi pandangan pemain.",
        "Mengingat latar visual game bernuansa malam gelap, seluruh indikator penting pada tampilan layar (jumlah nyawa hati, persentase energi lentera, lontar terkumpul, waktu, nama level, serta status cahaya) menggunakan warna emas terang di atas panel gelap transparan. Hal ini memudahkan pemain memantau kondisi karakternya secara sekilas saat bermanuver.",
        "6.1 clarity",
    )
    swap(
        "Seluruh komponen panel menu, kotak dialog Mpu Bharada, hingga layar kemenangan menggunakan tipografi, skema bingkai kayu-emas, dan gaya ikon piksel yang seragam.",
        "Seluruh elemen antarmuka, mulai dari menu utama, kotak percakapan Mpu Bharada, panel jeda, hingga layar hasil akhir dirancang seragam menggunakan tema bingkai kayu berornamen emas, tipografi bergaya piksel klasik, dan palet warna budaya Bali yang selaras.",
        "6.1 consistency",
    )

    # 8.1 Folder intro
    swap(
        "Untuk memenuhi indikator penilaian kualitas struktur proyek dan kerapian <i>source code</i>, direktori proyek Unity diorganisasikan secara modular sebagai berikut:",
        "Agar pengelolaan aset dan kode program tetap teratur serta mudah dikembangkan, seluruh berkas proyek di Unity dikelompokkan secara terstruktur ke dalam folder-folder modular sesuai fungsinya:",
        "8.1 folder intro",
    )

    # 8.2 Roadmap
    swap(
        """    <p>
      Versi final prototipe ini menyatukan fitur Tugas 2 dengan revisi tiga level, alur kesulitan, dan sistem skor:
    </p>
    <ol>
      <li><b>Fitur final:</b> tiga level (Desa Girah, Hutan Bambu Lemah Tulis, Pelataran Setra Gandamayu), halaman Pilih Kesulitan, mekanik <i>Rwa Bhineda Exposure</i>, skor/gelar/rekor, menu Pengaturan &amp; Jeda, serta layar Kredit.</li>
      <li><b>Keputusan desain &mdash; <i>Save System</i> tidak diimplementasikan:</b> seluruh permainan dapat diselesaikan dalam beberapa menit dan level dapat diulang dari halaman hasil. Persistensi dibatasi pada pengaturan dan rekor skor melalui <code>PlayerPrefs</code>.</li>
      <li><b>Ekspansi berikutnya:</b> ekspor Android dengan <i>virtual joystick</i>, penambahan level dan variasi musuh, serta <i>save</i> progres bila jumlah konten sudah cukup besar.</li>
      <li><b>Verifikasi final:</b> 74/74 assertion <i>play-mode</i> PASS; build macOS (<code>.app</code>) dan Windows (<code>.exe</code>) berhasil; build macOS dijalankan dan berjalan normal (19 November 2026).</li>
    </ol>""",
        """    <p>
      Pengembangan prototipe ini dirancang agar dapat terus diperluas secara bertahap tanpa merombak fondasi yang sudah ada. Berikut adalah evaluasi capaian akhir serta rencana pengembangan ke depan:
    </p>
    <ol>
      <li><b>Capaian Pengembangan Final:</b> Berhasil menyelesaikan 3 level permainan lengkap dengan 2 peta baru (Hutan Bambu Lemah Tulis dan Pelataran Setra Gandamayu), halaman pemilihan tingkat kesulitan mandiri, mekanik <i>Rwa Bhineda Exposure</i> (kewaspadaan musuh dipengaruhi terang lentera), sistem penilaian skor dan gelar kehormatan, serta menu jeda, pengaturan, dan kredit.</li>
      <li><b>Keputusan Desain Mengenai Sistem Penyimpanan (Save System):</b> Berdasarkan hasil pengujian gameplay, tiap putaran level dirancang ringkas dan dapat diselesaikan dalam durasi 1 hingga 2 menit. Menambahkan fitur save progres di tengah level dinilai kurang bermanfaat dan justru mengurangi ketegangan bermain. Oleh karena itu, mekanisme penyimpanan difokuskan pada aspek yang esensial, yaitu menyimpan preferensi pengaturan volume audio, mode layar, dan rekor skor tertinggi pemain.</li>
      <li><b>Rencana Pengembangan Selanjutnya:</b> Rencana jangka panjang meliputi penyediaan kontrol layar sentuh (<i>Virtual Joystick</i>) untuk platform Android, penambahan variasi rintangan dan jenis roh jahat baru (seperti Leak atau Banaspati), serta penyediaan sistem penyimpanan progres petualangan (*checkpoint/chapter save*) apabila jumlah babak cerita telah berkembang menjadi game berskala penuh.</li>
      <li><b>Hasil Pengujian dan Kesiapan Build:</b> Seluruh sistem permainan telah melalui pengujian otomatis (*automated play-mode smoke test*) dengan hasil 74 dari 74 kriteria pengujian berhasil lulus (PASS). Game telah berhasil diekspor menjadi aplikasi siap main untuk sistem operasi macOS (<code>.app</code>) dan Windows (<code>.exe</code>).</li>
    </ol>""",
        "8.2 roadmap polish",
    )

    with open(HTML_PATH, "w", encoding="utf-8") as handle:
        handle.write(html)
    print("[HTML] Polishing selesai")


def apply_docx():
    doc = Document(DOCX_PATH)

    # 1.1 Target Platform
    for row in doc.tables[2].rows:
        for cell in row.cells:
            if "Proyek Akhir (UAS)" in cell.text:
                for p in cell.paragraphs:
                    replace_in_paragraph(
                        p,
                        "siap diekspansi ke Android (.apk) pada Proyek Akhir (UAS)",
                        "siap diekspansi ke platform mobile (Android .apk) pada tahap pengembangan lanjutan",
                    )

    # 1.2 High concept, premis, ringkasan
    for p in doc.paragraphs:
        if p.text.startswith("High Concept:"):
            replace_in_paragraph(
                p,
                "Jelajahi kegelapan malam Desa Girah sebagai Bahula (murid Mpu Bharada), kelola energi cahaya Lentera Suci untuk menenangkan roh Bayangan Wabah, dan kumpulkan 3 naskah Lontar kuno ke Altar Penyucian untuk mengembalikan keseimbangan Rwa Bhineda.",
                "Mengusung konsep petualangan bernuansa budaya dan aksi tanpa kekerasan, pemain mengendalikan Bahula (murid Mpu Bharada) menjelajahi malam gelap Desa Girah berbekal Lentera Suci untuk menenangkan roh bayangan wabah serta menyucikan kembali desa dengan mengumpulkan naskah-naskah lontar kuno.",
            )
        elif p.text.startswith("Ringkasan Premis:"):
            replace_in_paragraph(
                p,
                "Kabut wabah dari Setra Gandamayu telah menyelimuti Desa Girah. Mpu Bharada mengutus muridnya, Bahula, masuk ke jantung desa dengan berbekal sebuah Lentera Suci. Berbeda dari game aksi konvensional, pemain tidak menggunakan kekerasan fisik, melainkan mengandalkan manajemen cahaya lentera untuk membuka jarak pandang di tengah kegelapan dan melepaskan gelombang cahaya suci (Holy Light Burst) guna meredam Bayangan Wabah sembari mencari 3 Lontar Kuno (Lontar Usada, Lontar Dharma, dan Lontar Rwa Bhineda).",
                "Kabut wabah misterius dari Setra Gandamayu telah menyelimuti wilayah Desa Girah dan sekitarnya. Mpu Bharada mengutus murid kepercayaannya, Bahula, untuk memulihkan keseimbangan alam sesuai filosofi Rwa Bhineda. Berbeda dari game laga pada umumnya, pemain tidak dibekali senjata fisik, melainkan mengandalkan Lentera Suci. Tantangan utama terletak pada pengelolaan energi cahaya: lentera yang menyala terang membuka pandangan namun menarik perhatian musuh, sedangkan lentera yang redup dapat menyamarkan langkah pemain. Pemain harus menyusuri tiga wilayah (Desa Girah, Hutan Bambu Lemah Tulis, dan Pelataran Setra Gandamayu), melumpuhkan roh bayangan dengan pancaran cahaya suci (Holy Light Burst), serta mengembalikan naskah-naskah Lontar Suci ke Altar Penyucian.",
            )
        elif p.text.startswith("Versi final prototipe menambahkan"):
            replace_in_paragraph(
                p,
                "Versi final prototipe menambahkan tiga level (dua peta baru), halaman Pilih Kesulitan setelah tombol Mulai Bermain, mekanik Rwa Bhineda Exposure, serta skor, gelar, dan rekor pada halaman hasil tiap level. Save progres tidak diimplementasikan karena permainan dapat diselesaikan dalam beberapa menit; persistensi dibatasi pada pengaturan dan rekor skor.",
                "Pada versi final pengembangan ini, prototipe telah diperluas menjadi tiga level lengkap dengan dua peta baru, antarmuka pemilihan tingkat kesulitan, penyesuaian dinamis kewaspadaan musuh berdasarkan terang lentera (Rwa Bhineda Exposure), serta sistem rekapitulasi skor dan pencapaian gelar pada akhir tiap babak.",
            )

    # 2.1 Core Loop Intro
    for p in doc.paragraphs:
        if p.text.startswith("Berdasarkan prinsip Systems Analysis & Design"):
            replace_in_paragraph(
                p,
                "Berdasarkan prinsip Systems Analysis & Design untuk permainan digital, siklus aksi berulang (Core Loop) yang menjadi jantung gameplay “Lentera Dirah” terdiri atas 4 tahapan yang saling terhubung:",
                "Dalam perancangan game “Lentera Dirah”, siklus utama permainan (Core Loop) dibangun dari 4 tahapan aksi yang saling terhubung secara berkesinambungan:",
            )

    # 2.2 MDA Table
    mda_table = doc.tables[4]
    set_cell_text(mda_table.rows[1].cells[0], "Mechanics\n(Aturan dan Mekanik Permainan)")

    # Clean Mechanics cell
    m_cell = mda_table.rows[1].cells[1]
    for child in list(m_cell.paragraphs[0]._p):
        if not child.tag.endswith("}pPr"):
            m_cell.paragraphs[0]._p.remove(child)
    m_cell.paragraphs[0].add_run(
        "1. Navigasi 4 Arah: Karakter Bahula dapat diarahkan ke atas, bawah, kiri, dan kanan secara seimbang dan responsif (kecepatan gerak 4.5 meter/detik).\n"
        "2. Penyusutan Lentera (Light Decay): Energi lentera menyusut perlahan sebesar 2% per detik, membuat lingkaran cahaya lentera menyusut dari radius 6.0 meter hingga minimal 1.8 meter.\n"
        "3. Pancaran Cahaya Suci (Holy Light Burst): Pemain dapat menekan tombol Spasi untuk melumpuhkan roh bayangan di sekitar (radius 3.5 meter) selama 3 detik, menghabiskan 15% energi dengan jeda pengisian kembali (cooldown) 4 detik.\n"
        "4. Penyucian Altar: Segel pelindung Altar di tengah area hanya akan terbuka setelah pemain mengumpulkan 3 naskah Lontar Suci pada level tersebut.\n"
        "5. Keseimbangan Cahaya (Rwa Bhineda Exposure): Terang lentera memengaruhi kewaspadaan musuh secara dinamis (lentera terang membuat deteksi musuh bertambah hingga +30%, sedangkan lentera redup menyamarkan pemain hingga -30%).\n"
        "6. Tiga Tingkat Kesulitan: Pilihan mode Mudah, Normal, dan Sulit yang memodifikasi daya tahan lentera, kelincahan musuh, serta pengali perolehan skor akhir.\n"
        "7. Penilaian Skor & Gelar: Performa tiap level dinilai dari waktu tempuh, sisa nyawa, dan sisa energi yang menghasilkan gelar (Penyuci Agung, Murid Teladan, Pejalan Malam) serta mencatat rekor skor tertinggi.\n"
        "8. Tiga Wilayah Petualangan: Permainan tersusun dari 3 level berurutan (Desa Girah, Hutan Bambu Lemah Tulis, dan Pelataran Setra Gandamayu) dengan akumulasi skor total."
    )
    for extra in m_cell.paragraphs[1:]:
        extra._element.getparent().remove(extra._element)

    # Clean Dynamics cell
    d_cell = mda_table.rows[2].cells[1]
    for child in list(d_cell.paragraphs[0]._p):
        if not child.tag.endswith("}pPr"):
            d_cell.paragraphs[0]._p.remove(child)
    d_cell.paragraphs[0].add_run(
        "1. Dilema Manajemen Energi Cahaya: Pemain terus menimbang kapan harus mempertahankan lentera tetap terang agar jalan terlihat jelas, dan kapan harus mengorbankan energi demi melumpuhkan musuh saat terdesak.\n"
        "2. Navigasi Taktis & Pengamatan Pola (Risk vs. Reward): Untuk mengambil Lontar dan Minyak di lorong sempit, pemain dituntut bersabar mengamati rute patroli roh bayangan terlebih dahulu sebelum melangkah masuk.\n"
        "3. Taktik Menyelinap dalam Temaram: Membiarkan lentera agak redup memberi keuntungan taktis karena musuh lebih sulit melihat Bahula, namun pemain harus berani melangkah dengan jarak pandang terbatas."
    )
    for extra in d_cell.paragraphs[1:]:
        extra._element.getparent().remove(extra._element)

    # Clean Aesthetics cell
    a_cell = mda_table.rows[3].cells[1]
    for child in list(a_cell.paragraphs[0]._p):
        if not child.tag.endswith("}pPr"):
            a_cell.paragraphs[0]._p.remove(child)
    a_cell.paragraphs[0].add_run(
        "1. Tension & Relief (Ketegangan & Kelegaan): Sensasi tegang saat menyusuri malam gelap diiringi alunan gamelan Bali, yang berganti menjadi rasa lega dan puas saat berhasil menemukan pendar cahaya Lontar Suci atau menyucikan Altar.\n"
        "2. Cultural Immersion (Penghayatan Budaya Bali): Mengajak pemain merasakan nilai filosofi Rwa Bhineda secara langsung lewat dinamika cahaya dan bayangan, serta keanggunan visual naskah lontar dan pura tradisional Bali.\n"
        "3. Mastery & Replayability (Kepuasan Penguasaan Tantangan): Variasi tingkat kesulitan, perhitungan skor terperinci, dan gelar kehormatan memotivasi pemain untuk mengulang permainan dengan catatan waktu dan strategi yang lebih baik."
    )
    for extra in a_cell.paragraphs[1:]:
        extra._element.getparent().remove(extra._element)

    # 3.1 Kontrol table
    ctrl_table = doc.tables[5]
    set_cell_text(ctrl_table.rows[0].cells[2], "Respon dan Perilaku Sistem")
    set_cell_text(
        ctrl_table.rows[1].cells[2],
        "Menggerakkan karakter Bahula ke empat arah mata angin secara responsif. Kecepatan diagonal diselaraskan secara proporsional agar karakter bergerak stabil dan tidak meluncur lebih cepat saat bergerak miring."
    )
    set_cell_text(
        ctrl_table.rows[2].cells[2],
        "Melepaskan kilatan cahaya suci sesaat yang melumpuhkan seluruh roh bayangan di sekitar pemain (radius 3.5 meter) selama 3 detik. Aksi ini membutuhkan minimal 15% energi lentera dengan jeda pengisian (cooldown) 4 detik."
    )
    set_cell_text(
        ctrl_table.rows[3].cells[2],
        "Digunakan untuk memilih tombol antarmuka layar serta melanjutkan percakapan dialog wejangan dari Mpu Bharada."
    )
    if len(ctrl_table.rows) >= 5:
        set_cell_text(
            ctrl_table.rows[4].cells[2],
            "Menjeda permainan seketika (seluruh gerakan dan waktu dibekukan), menampilkan panel Jeda dengan opsi melanjutkan petualangan, mengatur volume audio/layar penuh, atau kembali ke menu utama."
        )

    # 3.2 Collision table
    col_table = doc.tables[6]
    set_cell_text(col_table.rows[0].cells[2], "Jenis Interaksi Fisik")
    set_cell_text(col_table.rows[0].cells[3], "Respon Interaksi dalam Permainan")
    set_cell_text(
        col_table.rows[1].cells[3],
        "Membatasi gerak fisik pemain dan musuh agar tidak dapat menembus pagar batu, pepohonan beringin, gapura candi bentar, dan bangunan suci desa."
    )
    set_cell_text(
        col_table.rows[2].cells[3],
        "Lontar otomatis terambil saat disentuh pemain, menambah jumlah lontar di tampilan layar (HUD), memainkan denting genta suci, menampilkan petuah budaya, dan lontar menghilang dari peta."
    )
    set_cell_text(
        col_table.rows[3].cells[3],
        "Mengisi ulang energi lentera sebesar +35% (maksimal 100%), memperluas kembali lingkaran terang lentera, dan memainkan efek suara percikan api obor."
    )
    set_cell_text(
        col_table.rows[4].cells[3],
        "Bila roh bayangan sedang aktif (tidak membeku), sentuhan musuh akan mengurangi 1 nyawa pemain, memicu efek kebal sementara selama 1 detik (sprite Bahula berkedip merah), dan memainkan efek suara benturan."
    )
    set_cell_text(
        col_table.rows[5].cells[3],
        "Mengecek kelengkapan 3 Lontar Suci pada level tersebut. Jika lengkap, altar menyala keemasan, memainkan tabuhan kemenangan, dan menyelesaikan level."
    )

    # 3.3 Mekanik 2 & 3 in paragraphs
    for p in doc.paragraphs:
        if p.text.startswith("Mekanik Utama 2:"):
            replace_in_paragraph(
                p,
                "Karakter Bahula dilengkapi komponen Light 2D (Point Light) yang radius terangnya berbanding lurus dengan persentase energi lentera (pada energi 100% radius luar adalah 6.0 unit; menyusut perlahan hingga minimal 1.8 unit). Apabila energi lentera mencapai 0%, kegelapan menyelimuti pemain sepenuhnya dan memicu kondisi kalah (Game Over). Pemain dapat menekan tombol Space untuk melepaskan pancaran cahaya suci yang membekukan (Stun) seluruh NPC Bayangan Wabah di sekitarnya selama 3 detik.",
                "Karakter Bahula dibekali Lentera Suci yang memancarkan lingkaran cahaya dinamis. Luas pandangan ini bergantung langsung pada sisa energi lentera: saat energi terisi penuh (100%), cahaya menerangi area hingga radius 6 meter, lalu perlahan menyusut hingga tersisa 1.8 meter saat energi menipis. Bila energi sampai habis (0%), kegelapan malam seketika menelan Bahula dan permainan berakhir (Game Over). Untuk menyelamatkan diri saat terpojok, pemain dapat menekan tombol Spasi untuk melepaskan gelombang cahaya suci (Holy Light Burst) yang membekukan seluruh roh bayangan di sekitarnya selama 3 detik.",
            )
        elif p.text.startswith("Mekanik Utama 3:"):
            replace_in_paragraph(
                p,
                "Energi lentera tidak hanya menentukan luas pandangan, tetapi juga tingkat keterlihatan Bahula. Radius deteksi efektif Bayangan Wabah = detectRadius x pengali kesulitan x Lerp(0.7, 1.3, energi/100). Pada energi 100% musuh mendeteksi hingga 30% lebih jauh; pada energi rendah deteksi menyusut hingga 30%, sehingga lentera redup berfungsi sebagai penyamaran. HUD menampilkan CAHAYA: TERANG / SEIMBANG / REDUP. Mekanik ini menjadikan Light Decay sebagai keputusan taktis, bukan sekadar pengatur waktu.",
                "Energi lentera memiliki fungsi ganda yang merefleksikan filosofi Rwa Bhineda: lentera tidak hanya menerangi jalan, melainkan memengaruhi seberapa mudah Bahula dilihat oleh musuh. Saat lentera menyala terang (energi tinggi), roh bayangan dapat melihat keberadaan Bahula dari jarak yang lebih jauh (hingga +30%). Sebaliknya, saat lentera dibiarkan meredup (energi rendah), langkah Bahula menjadi lebih tersamarkan (jarak deteksi musuh turun hingga -30%). Pemain dapat memantau kondisi ini secara langsung lewat indikator pada layar (CAHAYA: TERANG / SEIMBANG / REDUP). Dengan mekanisme ini, penyusutan lentera tidak lagi sekadar batas waktu, melainkan elemen taktis di mana pemain bisa sengaja bermain sembunyi-sembunyi (stealth) di area yang temaram.",
            )

    # 4.1 FSM intro
    for p in doc.paragraphs:
        if p.text.startswith("Untuk menjamin struktur kode yang bersih"):
            replace_in_paragraph(
                p,
                "Untuk menjamin struktur kode yang bersih, bebas bug, dan memenuhi indikator penilaian tertinggi pada kriteria State Management, permainan ini mengimplementasikan pola Finite State Machine (FSM) berbasis enum pada 3 tingkatan:",
                "Untuk mengatur alur permainan, aksi karakter, dan perilaku musuh agar berjalan teratur serta mudah dikembangkan, game ini menerapkan sistem Finite State Machine (FSM) yang dibagi ke dalam 3 tingkatan hierarki:",
            )

    # 4.2 State Table
    st_table = doc.tables[8]
    set_cell_text(st_table.rows[0].cells[2], "Kondisi Pemicu Transisi")
    set_cell_text(st_table.rows[0].cells[3], "Perilaku Karakter / Sistem")

    # Manager states
    set_cell_text(st_table.rows[1].cells[3], "Menampilkan judul utama game dan menu (Mulai Bermain, Cara Bermain, Pengaturan, Kredit, Keluar). Karakter belum dapat digerakkan.")
    set_cell_text(st_table.rows[2].cells[3], "Membuka halaman pemilihan tingkat kesulitan (Mudah, Normal, Sulit) lengkap dengan penjelasan perbedaan tantangan dan pengali skor.")
    set_cell_text(st_table.rows[3].cells[3], "Menampilkan kotak percakapan wejangan dan instruksi misi suci dari Mpu Bharada kepada Bahula sebelum memasuki area permainan.")
    set_cell_text(st_table.rows[4].cells[2], "Pemain selesai membaca dialog pembuka atau memulai level berikutnya.")
    set_cell_text(st_table.rows[4].cells[3], "Permainan aktif: pemain dapat mengontrol gerak Bahula, roh bayangan mulai berpatroli, dan energi lentera menyusut secara bertahap.")
    set_cell_text(st_table.rows[5].cells[3], "Permainan berhenti sementara (seluruh gerakan dan waktu dibekukan), memunculkan menu jeda dengan opsi Lanjutkan, Pengaturan, atau kembali ke Menu Utama.")
    set_cell_text(st_table.rows[6].cells[3], "Level selesai: roh bayangan berhenti mengejar, audio kemenangan berbunyi, dan muncul layar hasil dengan skor, gelar, serta opsi lanjut ke level berikutnya.")
    set_cell_text(st_table.rows[7].cells[3], "Layar kekalahan muncul saat nyawa Bahula habis atau lentera padam, menampilkan skor total yang sempat diraih serta tombol Coba Lagi untuk mengulang level tersebut.")

    # Player states (rows 8-11)
    if len(st_table.rows) >= 12:
        set_cell_text(st_table.rows[8].cells[3], "Karakter berdiri diam di tempat sambil tetap menghadap ke arah terakhir, siap menerima perintah gerak selanjutnya.")
        set_cell_text(st_table.rows[9].cells[3], "Karakter melangkah secara halus ke arah yang ditekan sambil memainkan animasi berjalan 4 arah.")
        set_cell_text(st_table.rows[10].cells[3], "Lentera memancarkan kilau suci sesaat yang memperluas cahaya dan membekukan roh bayangan terdekat selama 3 detik.")
        set_cell_text(st_table.rows[11].cells[3], "Karakter kehilangan 1 nyawa, berkedip merah, dan memperoleh status kebal sementara selama 1 detik.")

    # Enemy states (rows 12-14)
    if len(st_table.rows) >= 15:
        set_cell_text(st_table.rows[12].cells[3], "Roh bayangan berpatroli secara otomatis bolak-balik menyusuri rute ronda yang ditentukan dengan kecepatan santai (2.2 meter/detik).")
        set_cell_text(st_table.rows[13].cells[3], "Roh bayangan berubah agresif dan bergerak mengejar Bahula dengan kecepatan tinggi (3.4 meter/detik); musuh kembali berpatroli jika Bahula berhasil menjauh.")
        set_cell_text(st_table.rows[14].cells[3], "Roh bayangan membeku diam di tempat selama 3 detik, warna tubuhnya berubah biru pucat transparan, dan tidak dapat melukai pemain.")

    # 5.2 Animasi
    for p in doc.paragraphs:
        if p.text.startswith("Pose-to-Pose & Walk Cycle Timing:"):
            replace_in_paragraph(
                p,
                "Karakter Bahula dan NPC Bayangan memiliki siklus animasi jalan 4 arah (Atas, Bawah, Kiri, Kanan) menggunakan Animator Controller dengan 8 klip state (Idle dan Walking untuk 4 arah) yang dipanggil melalui Animator.Play sesuai arah hadap, tanpa Blend Tree agar transisi deterministik.",
                "Karakter Bahula dan roh bayangan dilengkapi siklus animasi langkah kaki 4 arah (atas, bawah, kiri, dan kanan). Pergantian animasi diam (idle) dan melangkah (walking) berganti secara responsif dan tegas sesuai arah gerak pemain agar animasi karakter terasa lincah dan tidak kaku.",
            )
        elif p.text.startswith("Squash, Stretch, & Sinusoidal Floating"):
            replace_in_paragraph(
                p,
                "Objek LontarSuci dan MinyakObor bergerak mengambang naik-turun secara berirama menggunakan fungsi trigonometri Mathf.Sin(Time.time * frequency) * amplitude sehingga terlihat hidup dan menarik perhatian pemain.",
                "Objek naskah Lontar Suci dan guci Minyak Obor dirancang melayang naik-turun secara berirama dan halus. Efek visual ini membuat artefak budaya tersebut tampak hidup dan langsung memikat perhatian pemain di tengah area yang temaram.",
            )
        elif p.text.startswith("Anticipation & Visual Feedback"):
            replace_in_paragraph(
                p,
                "Saat pemain menekan Space (Holy Light Burst), radius cahaya membesar secara cepat lalu kembali ke ukuran semula, disertai perubahan warna musuh yang terkena efek Stun.",
                "Ketika pemain melepaskan semburan cahaya suci (Holy Light Burst), lentera memancarkan kilatan membesar sesaat sebelum kembali normal, disertai reaksi visual pada roh bayangan yang seketika berubah warna menjadi biru transparan sebagai tanda musuh telah dilumpuhkan.",
            )

    # 6.1 UI/UX
    for p in doc.paragraphs:
        if p.text.startswith("Klaritas / Kejelasan (Clarity):"):
            replace_in_paragraph(
                p,
                "Mengingat latar permainan bernuansa malam gelap, seluruh indikator vital pada Heads-Up Display (Nyawa, Bar Energi Lentera, dan Jumlah Lontar) menggunakan warna emas menyala (#FFB84D) di atas panel gelap agar terbaca secara instan tanpa menghalangi pandangan pemain.",
                "Mengingat latar visual game bernuansa malam gelap, seluruh indikator penting pada tampilan layar (jumlah nyawa hati, persentase energi lentera, lontar terkumpul, waktu, nama level, serta status cahaya) menggunakan warna emas terang di atas panel gelap transparan. Hal ini memudahkan pemain memantau kondisi karakternya secara sekilas saat bermanuver.",
            )
        elif p.text.startswith("Konsistensi (Consistency):"):
            replace_in_paragraph(
                p,
                "Seluruh komponen panel menu, kotak dialog Mpu Bharada, hingga layar kemenangan menggunakan tipografi, skema bingkai kayu-emas, dan gaya ikon piksel yang seragam.",
                "Seluruh elemen antarmuka, mulai dari menu utama, kotak percakapan Mpu Bharada, panel jeda, hingga layar hasil akhir dirancang seragam menggunakan tema bingkai kayu berornamen emas, tipografi bergaya piksel klasik, dan palet warna budaya Bali yang selaras.",
            )

    # 8.1 Folder intro
    for p in doc.paragraphs:
        if p.text.startswith("Untuk memenuhi indikator penilaian kualitas struktur proyek"):
            replace_in_paragraph(
                p,
                "Untuk memenuhi indikator penilaian kualitas struktur proyek dan kerapian source code, direktori proyek Unity diorganisasikan secara modular sebagai berikut:",
                "Agar pengelolaan aset dan kode program tetap teratur serta mudah dikembangkan, seluruh berkas proyek di Unity dikelompokkan secara terstruktur ke dalam folder-folder modular sesuai fungsinya:",
            )

    # 8.2 Roadmap
    for p in doc.paragraphs:
        if p.text.startswith("Pengembangan prototipe ini dirancang agar dapat terus diperluas"):
            pass
        elif p.text.startswith("Versi final prototipe ini menyatukan fitur"):
            p.text = "Pengembangan prototipe ini dirancang agar dapat terus diperluas secara bertahap tanpa merombak fondasi yang sudah ada. Berikut adalah evaluasi capaian akhir serta rencana pengembangan ke depan:"
        elif p.text.startswith("Fitur final:"):
            p.text = "1. Capaian Pengembangan Final: Berhasil menyelesaikan 3 level permainan lengkap dengan 2 peta baru (Hutan Bambu Lemah Tulis dan Pelataran Setra Gandamayu), halaman pemilihan tingkat kesulitan mandiri, mekanik Rwa Bhineda Exposure (kewaspadaan musuh dipengaruhi terang lentera), sistem penilaian skor dan gelar kehormatan, serta menu jeda, pengaturan, dan kredit."
        elif p.text.startswith("Keputusan desain — Save System tidak diimplementasikan:"):
            p.text = "2. Keputusan Desain Mengenai Sistem Penyimpanan (Save System): Berdasarkan hasil pengujian gameplay, tiap putaran level dirancang ringkas dan dapat diselesaikan dalam durasi 1 hingga 2 menit. Menambahkan fitur save progres di tengah level dinilai kurang bermanfaat dan justru mengurangi ketegangan bermain. Oleh karena itu, mekanisme penyimpanan difokuskan pada aspek yang esensial, yaitu menyimpan preferensi pengaturan volume audio, mode layar, dan rekor skor tertinggi pemain."
        elif p.text.startswith("Ekspansi berikutnya:"):
            p.text = "3. Rencana Pengembangan Selanjutnya: Rencana jangka panjang meliputi penyediaan kontrol layar sentuh (Virtual Joystick) untuk platform Android, penambahan variasi rintangan dan jenis roh jahat baru (seperti Leak atau Banaspati), serta penyediaan sistem penyimpanan progres petualangan (checkpoint/chapter save) apabila jumlah babak cerita telah berkembang menjadi game berskala penuh."
        elif p.text.startswith("Verifikasi final:"):
            p.text = "4. Hasil Pengujian dan Kesiapan Build: Seluruh sistem permainan telah melalui pengujian otomatis (automated play-mode smoke test) dengan hasil 74 dari 74 kriteria pengujian berhasil lulus (PASS). Game telah berhasil diekspor menjadi aplikasi siap main untuk sistem operasi macOS (.app) dan Windows (.exe)."

    doc.save(DOCX_PATH)
    print("[DOCX] Polishing selesai")


if __name__ == "__main__":
    apply_html()
    apply_docx()
