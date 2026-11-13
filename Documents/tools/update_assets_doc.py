#!/usr/bin/env python3
"""Synchronise the asset reference document (HTML) with the final build."""

import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_PATH = os.path.join(
    BASE, "HTML Artifacts", "230030309_Muhammad_Sufyan_Daftar_Referensi_Assets_Lentera_Dirah.html"
)

REPLACEMENTS = [
    # 1.2 licence list: Pixabay/Freesound -> Public Domain
    (
        """      <li>
        <b>Pixabay Content License / Freesound CC0 (Royalty-Free Audio):</b> Lisensi audio bebas royalti yang mengizinkan penggunaan musik latar (BGM) dan efek suara (SFX) secara gratis di dalam proyek permainan digital dan video demonstrasi gameplay.<br>
        Tautan Resmi Lisensi Audio: <a class="ref-link" href="https://pixabay.com/service/license-summary/" target="_blank">https://pixabay.com/service/license-summary/</a>
      </li>""",
        """      <li>
        <b>Public Domain (Wikimedia Commons):</b> Rekaman historis yang telah menjadi milik publik, bebas digunakan tanpa atribusi wajib, termasuk untuk musik latar (BGM) dan video demonstrasi gameplay.<br>
        Tautan Lisensi Commons: <a class="ref-link" href="https://commons.wikimedia.org/wiki/Commons:Licensing" target="_blank">https://commons.wikimedia.org/wiki/Commons:Licensing</a>
      </li>""",
    ),
    (
        "(seperti <i>Universal Render Pipeline 2D Lights</i> dan <i>TextMeshPro</i>) pada lisensi <i>Unity Personal</i>.",
        "(seperti <i>Universal Render Pipeline 2D Lights</i>) pada lisensi <i>Unity Personal</i>.",
    ),
    # pipeline diagram node
    (
        "Unduh paket aset CC0 (Ninja Adventure, Kenney UI, &amp; Audio Gamelan)",
        "Unduh paket CC0 (Ninja Adventure, BGM Public Domain Wikimedia, &amp; aset orisinal)",
    ),
    # 2.1 table
    (
        "<td>Karakter, Monster/Roh, Gulungan Lontar, Tilemap Desa, UI Hati, BGM, &amp; SFX</td>",
        "<td>Karakter, Monster/Roh, Gulungan Lontar, Tilemap Desa, UI Hati, &amp; SFX</td>",
    ),
    (
        """        <tr>
          <td style="text-align: center;">2</td>
          <td><b>Kenney Game Assets All-in-1</b><br>(<i>Tiny Town</i>, <i>Tiny Dungeon</i>, &amp; <i>UI Pack RPG</i>)</td>
          <td>Kenney Vleugels (Kenney.nl)</td>
          <td>Tilemap Tambahan, Ikon Lentera/Obor, Panel Menu, &amp; Tombol UI</td>
          <td><b>CC0 1.0</b><br>(Public Domain)</td>
          <td>
            &bull; <b>Katalog Utama:</b> <a class="ref-link" href="https://kenney.nl/assets" target="_blank">https://kenney.nl/assets</a><br>
            &bull; <b>Tiny Town 2D:</b> <a class="ref-link" href="https://kenney.nl/assets/tiny-town" target="_blank">https://kenney.nl/assets/tiny-town</a><br>
            &bull; <b>RPG UI Pack:</b> <a class="ref-link" href="https://kenney.nl/assets/ui-pack-rpg-expansion" target="_blank">https://kenney.nl/assets/ui-pack-rpg-expansion</a>
          </td>
        </tr>""",
        """        <tr>
          <td style="text-align: center;">2</td>
          <td><b>Wikimedia Commons</b><br>(<i>Gend&eacute;r Wayang</i> 1928)</td>
          <td>Gamelan Gender Wayang, Bali (rekaman 1928)</td>
          <td>Musik Latar (BGM Gamelan Gender Wayang, loop)</td>
          <td><b>Public Domain</b><br>(tanpa atribusi wajib)</td>
          <td>
            &bull; <b>Berkas Asli:</b> <a class="ref-link" href="https://commons.wikimedia.org/wiki/File:Gend%C3%A9r_Wayang_(1928).ogg" target="_blank">https://commons.wikimedia.org/wiki/File:Gend%C3%A9r_Wayang_(1928).ogg</a><br>
            &bull; <b>Ketentuan Lisensi:</b> <a class="ref-link" href="https://commons.wikimedia.org/wiki/Commons:Licensing" target="_blank">https://commons.wikimedia.org/wiki/Commons:Licensing</a>
          </td>
        </tr>""",
    ),
    (
        """        <tr>
          <td style="text-align: center;">3</td>
          <td><b>Pixabay Royalty-Free Music</b><br>(<i>Gamelan &amp; Bamboo Flute</i>)</td>
          <td>Komunitas Musisi Pixabay</td>
          <td>Musik Latar Tradisional (BGM Gamelan &amp; Suling Bambu)</td>
          <td><b>Pixabay License</b><br>(Free / No Attribution Required)</td>
          <td>
            &bull; <b>Koleksi Gamelan:</b> <a class="ref-link" href="https://pixabay.com/music/search/gamelan/" target="_blank">https://pixabay.com/music/search/gamelan/</a><br>
            &bull; <b>Koleksi Suling:</b> <a class="ref-link" href="https://pixabay.com/music/search/bamboo%20flute/" target="_blank">https://pixabay.com/music/search/bamboo%20flute/</a>
          </td>
        </tr>""",
        """        <tr>
          <td style="text-align: center;">3</td>
          <td><b>Aset Orisinal Lentera Dirah</b><br>(Lingkungan Bali &amp; Kostum Bahula)</td>
          <td>Muhammad Sufyan (proyek ini)</td>
          <td>Gapura, beringin, pura meru, bale kulkul, pelinggih, penjor, backdrop menu, restyle Bahula</td>
          <td><b>CC0 1.0</b><br>(Public Domain)</td>
          <td>
            &bull; <b>Generator:</b> <code>Game/Tools/generate_balinese_assets.py</code><br>
            &bull; <b>Lisensi:</b> <code>Game/Assets/_Project/Art/Environment/LICENSE_CC0.md</code>
          </td>
        </tr>""",
    ),
    (
        """        <tr>
          <td style="text-align: center;">4</td>
          <td><b>Freesound CC0 Traditional Chimes &amp; Gamelan</b></td>
          <td>Freesound Community</td>
          <td>Suara Denting Genta Suci (<i>Bajra</i>), Gong Kemenangan, &amp; Efek Api Obor</td>
          <td><b>CC0 1.0 / CC-BY</b></td>
          <td>
            &bull; <b>Portal Freesound:</b> <a class="ref-link" href="https://freesound.org/search/?q=gamelan" target="_blank">https://freesound.org/search/?q=gamelan</a><br>
            &bull; <b>Pixabay SFX:</b> <a class="ref-link" href="https://pixabay.com/sound-effects/search/bell%20chime/" target="_blank">https://pixabay.com/sound-effects/search/bell%20chime/</a>
          </td>
        </tr>
""",
        "",
    ),
    (
        """        <tr>
          <td style="text-align: center;">5</td>
          <td><b>OpenGameArt 2D Top-Down Collection</b></td>
          <td>Komunitas OpenGameArt</td>
          <td>Referensi Cadangan Sprite Obor, Gulungan Kuno, &amp; Efek Partikel Cahaya</td>
          <td><b>CC0 1.0</b><br>(Public Domain)</td>
          <td>
            &bull; <b>Portal Utama:</b> <a class="ref-link" href="https://opengameart.org/" target="_blank">https://opengameart.org/</a>
          </td>
        </tr>
""",
        "",
    ),
    (
        """          <td style="text-align: center;">6</td>
          <td><b>Unity Universal Render Pipeline (URP) 2D Lights</b></td>""",
        """          <td style="text-align: center;">4</td>
          <td><b>Unity Universal Render Pipeline (URP) 2D Lights</b></td>""",
    ),
    # 2.2 download guide
    (
        """      <li><b>Cara Mengunduh Aset Kenney.nl Secara Gratis:</b> Buka tautan paket di Kenney.nl (misalnya <a class="ref-link" href="https://kenney.nl/assets/tiny-town" target="_blank">https://kenney.nl/assets/tiny-town</a>), lalu klik tombol biru <b>&ldquo;Download (Free)&rdquo;</b> untuk langsung mendapatkan arsip <code>.zip</code> tanpa perlu membuat akun.</li>""",
        """      <li><b>Cara Mengunduh BGM Gamelan (Public Domain):</b> Buka halaman berkas <a class="ref-link" href="https://commons.wikimedia.org/wiki/File:Gend%C3%A9r_Wayang_(1928).ogg" target="_blank">Gend&eacute;r Wayang (1928)</a> di Wikimedia Commons, lalu klik tautan <b>&ldquo;Original file&rdquo;</b> untuk mengunduh <code>Gend&eacute;r Wayang (1928).ogg</code> tanpa biaya dan tanpa atribusi wajib.</li>
      <li><b>Aset Lingkungan Bali:</b> tidak diunduh dari pihak ketiga, melainkan dibuat dengan skrip <code>Game/Tools/generate_balinese_assets.py</code> (Python standard library) dan dilepas sebagai CC0 1.0.</li>""",
    ),
    # 3.1 Bahula
    (
        "<td><code>Actor/Characters/Monk/SpriteSheet.png</code><br><i>(Alternatif: <code>Villager/SpriteSheet.png</code>)</i></td>",
        "<td><code>Actor/Characters/Monk/SeparateAnim/Walk.png</code><br><i>(Disimpan sebagai <code>Art/Characters/Bahula_SpriteSheet.png</code>)</i></td>",
    ),
    (
        "<td><code>16 x 16 px</code> per frame (Grid 4 Arah)</td>",
        "<td><code>16 x 16 px</code> per frame (64&times;64, 4 Arah &times; 4 Frame)</td>",
    ),
    (
        "<td>Merepresentasikan murid padepokan Mpu Bharada. Digunakan pada komponen <code>SpriteRenderer</code> dan <code>Animator</code> untuk state <code>Idle</code> dan <code>Walking</code> 4 arah.</td>",
        "<td>Merepresentasikan murid padepokan Mpu Bharada. Sprite di-<i>restyle</i> menjadi pakaian/kamen putih, udeng coklat, dan sabuk emas. Digunakan pada komponen <code>SpriteRenderer</code> dan <code>Animator</code> untuk state <code>Idle</code> dan <code>Walking</code> 4 arah.</td>",
    ),
    # 3.1 spirit
    (
        "<td><code>Actor/Monsters/Spirit/SpriteSheet.png</code><br><i>(Alternatif: <code>Ghost/SpriteSheet.png</code>)</i></td>",
        "<td><code>Actor/Monsters/Spirit/Spirit.png</code><br><i>(Disimpan sebagai <code>Art/Monsters/ShadowSpirit_SpriteSheet.png</code>)</i></td>",
    ),
    (
        "<td><code>16 x 16 px</code> per frame</td>",
        "<td><code>16 x 16 px</code> per frame (64&times;64)</td>",
    ),
    # 3.2 items
    (
        "<td><code>Items/Scroll/ScrollEmpty.png</code> atau <code>Items/Scroll/ScrollThunder.png</code></td>",
        "<td><code>Items/Scroll/ScrollEmpty.png</code> (Disimpan sebagai <code>Art/Items/Lontar.png</code>); varian <code>ScrollThunder.png</code> disimpan sebagai <code>Lontar_RwaBhineda.png</code></td>",
    ),
    (
        "<td><code>Items/Potion/MilkPot.png</code> atau <code>Items/Object/Lantern.png</code></td>",
        "<td><code>Items/Potion/MilkPot.png</code> (Disimpan sebagai <code>Art/Items/OilJar.png</code>)</td>",
    ),
    (
        "<td><code>Backgrounds/Tilesets/TilesetElement.png</code> (Sprite Altar Batu / Patung Kuil)</td>",
        "<td><code>Backgrounds/Tilesets/TilesetElement.png</code> &mdash; <i>tile</i> (7,2), Sprite Altar Batu / Patung Kuil (Disimpan sebagai <code>Art/Tilesets/TilesetElement.png</code>)</td>",
    ),
    # 3.3 walls
    (
        "<td><code>Backgrounds/Tilesets/TilesetNature.png</code> &amp; <code>TilesetHouse.png</code></td>",
        "<td><code>Backgrounds/Tilesets/TilesetNature.png</code> (Kanopi pepohonan; disimpan sebagai <code>Art/Tilesets/TilesetNature.png</code>)</td>",
    ),
    (
        "<td>Menyusun rumpun pohon bambu, pagar batu desa, dan rumah tradisional sebagai pembatas lorong labirin desa.</td>",
        "<td>Menyusun rumpun pohon bambu/pepohonan dan pagar batu desa sebagai pembatas lorong labirin desa.</td>",
    ),
    # 4.1 UI
    (
        "<td><code>HUD/Dialog/DialogBoxSimple.png</code> &amp; <code>HUD/NinePathRect/</code></td>",
        "<td><code>HUD/NinePathRect/FacesetBox.png</code> (bingkai dialog) &amp; <code>HUD/NinePathRect/DialogueBubble.png</code> (tombol)</td>",
    ),
    ("<td><b>Font Pixel Tradisional</b></td>", "<td><b>Font UI</b></td>"),
    (
        "<td><code>HUD/Font/NormalFont.ttf</code></td>",
        "<td><code>HUD/Font/NormalFont.ttf</code> (diarsipkan); UI memakai font bawaan Unity (<code>LegacyRuntime.ttf</code>)</td>",
    ),
    (
        "<td>Diimpor ke dalam <code>TextMeshPro Font Asset</code> untuk memastikan keterbacaan (<i>Clarity</i>) dan konsistensi visual (<i>Consistency</i>).</td>",
        "<td>Komponen uGUI <code>Text</code> memakai font bawaan Unity karena metrik <i>glyph</i> <code>NormalFont.ttf</code> tidak konsisten (spasi dan lebar huruf) sehingga keterbacaan (<i>Clarity</i>) lebih terjaga.</td>",
    ),
    # 4.2 audio header + BGM
    (
        "<th style=\"width: 33%;\" bgcolor=\"#e8eef5\">Path File di Paket <code>NinjaAdventure</code> / Pixabay</th>",
        "<th style=\"width: 33%;\" bgcolor=\"#e8eef5\">Path File Sumber Aset</th>",
    ),
    (
        "<td>Pixabay Gamelan/Flute MP3 <i>atau</i> <code>Musics/2 - The Cave.ogg</code> / <code>16 - Dark Cave.ogg</code></td>",
        "<td><code>Wikimedia Commons</code> &mdash; <i>Gend&eacute;r Wayang</i> (1928), <i>Public Domain</i> (disimpan sebagai <code>Audio/BGM/bgm_gamelan_girah.ogg</code>)</td>",
    ),
]

ENVIRONMENT_SECTION = """    <h2 class="section-title" id="ast-4-4">4.4 Aset Lingkungan Budaya Bali &amp; Kostum Bahula (Orisinal, CC0)</h2>
    <p>
      Untuk memperkuat identitas budaya Bali, prototipe ini menambahkan aset lingkungan orisinal yang digambar khusus (bukan aset pihak ketiga) melalui <code>Game/Tools/generate_balinese_assets.py</code>. Seluruh berkas dilepas dengan lisensi <b>CC0 1.0</b> (<code>Game/Assets/_Project/Art/Environment/LICENSE_CC0.md</code>).
    </p>
    <table class="data-table">
      <thead>
        <tr>
          <th style="width: 30%;" bgcolor="#e8eef5">Berkas</th>
          <th style="width: 14%;" bgcolor="#e8eef5">Ukuran</th>
          <th style="width: 56%;" bgcolor="#e8eef5">Pemakaian di Game</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>Gapura_CandiBentar.png</code></td>
          <td>96 &times; 80 px</td>
          <td>Gapura keluar desa di spawn dan gerbang sektor utara; collider hanya pada dua tiang agar tengah tetap dapat dilewati.</td>
        </tr>
        <tr>
          <td><code>Gapura_Menu.png</code></td>
          <td>192 &times; 160 px</td>
          <td>Latar panel <i>Main Menu</i> (opasitas rendah) bersama siluet beringin dan penjor.</td>
        </tr>
        <tr>
          <td><code>PohonBeringin_Besar.png</code></td>
          <td>64 &times; 80 px</td>
          <td>Empat sudut alun-alun serta sektor barat dan timur (collider pada batang).</td>
        </tr>
        <tr>
          <td><code>PohonBeringin_Kecil.png</code></td>
          <td>40 &times; 56 px</td>
          <td>Pohon beringin di sektor utara.</td>
        </tr>
        <tr>
          <td><code>PuraMeru.png</code></td>
          <td>48 &times; 96 px</td>
          <td>Pura meru bertingkat di sektor barat dan timur.</td>
        </tr>
        <tr>
          <td><code>BaleKulkul.png</code></td>
          <td>48 &times; 48 px</td>
          <td>Bale kulkul di alun-alun dan sektor utara.</td>
        </tr>
        <tr>
          <td><code>Pelinggih.png</code></td>
          <td>24 &times; 32 px</td>
          <td>Pelinggih di empat sudut alun-alun.</td>
        </tr>
        <tr>
          <td><code>Penjor.png</code></td>
          <td>16 &times; 64 px</td>
          <td>Enam penjor bambu berhias di tepi alun-alun (tanpa collider).</td>
        </tr>
      </tbody>
    </table>
    <p>
      <b>Kostum Bahula.</b> Sprite Bahula dari paket Ninja Adventure di-<i>restyle</i> melalui <code>Game/Tools/restyle_bahula_balinese.py</code> menjadi kemeja dan kamen putih (<code>#F4EFE6</code>), udeng coklat (<code>#6B4A2F</code>), serta sabuk emas (<code>#FFB84D</code>). Karena asal sprite adalah CC0, hasil modifikasi juga dilepas CC0 (<code>Game/Assets/_Project/Art/Characters/LICENSE_Bahula_Restyle.md</code>).
    </p>

"""


def main():
    with open(HTML_PATH, encoding="utf-8") as handle:
        text = handle.read()

    for old, new in REPLACEMENTS:
        count = text.count(old)
        if count != 1:
            raise SystemExit(f"Anchor muncul {count}x: {old[:90]!r}")
        text = text.replace(old, new)

    anchor = '    <h2 class="section-title" id="ast-4-3">4.3 Spesifikasi Aset Pencahayaan Dinamis (Unity URP 2D Lights)</h2>'
    if text.count(anchor) != 1:
        raise SystemExit("Anchor 4.3 tidak unik")

    # insert section 4.4 after the lighting section (before BAB V)
    bab5 = '    <!-- ==================== BAB V: KONFIGURASI TEKNIS UNITY ==================== -->'
    if text.count(bab5) != 1:
        raise SystemExit("Anchor BAB V tidak unik")
    text = text.replace(bab5, ENVIRONMENT_SECTION + bab5)

    with open(HTML_PATH, "w", encoding="utf-8") as handle:
        handle.write(text)

    print(f"Asset reference updated: {len(REPLACEMENTS) + 1} edits")


if __name__ == "__main__":
    main()
