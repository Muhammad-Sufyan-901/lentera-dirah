#!/usr/bin/env python3
"""Synchronise the GDD (DOCX + HTML) with the final game build.

Only the parts that no longer match the implemented game are touched:
engine version, platform, collision props, animation approach, BGM, asset
paths, UI frames/font, master asset table, folder structure, plus new
sections for the Balinese environment art and Bahula's restyled costume.
"""

import copy
import os
import sys

from docx import Document

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCX_PATH = os.path.join(BASE, "GDD", "230030309_Muhammad_Sufyan_Game_Design_Document_GDD_Lentera_Dirah.docx")
HTML_PATH = os.path.join(BASE, "HTML Artifacts", "230030309_Muhammad_Sufyan_Game_Design_Document_GDD_Lentera_Dirah.html")

# --------------------------------------------------------------------------
# HTML: exact replacements (each anchor must appear exactly once)
# --------------------------------------------------------------------------
HTML_REPLACEMENTS = [
    # 1.1 engine + platform
    (
        "<td>Unity 2D (Universal Render Pipeline / URP 2D Lights) dengan bahasa pemrograman C#</td>",
        "<td>Unity 6000.6.9f1 &mdash; 2D (Universal Render Pipeline 17.6 / URP 2D Lights) dengan bahasa pemrograman C#</td>",
    ),
    (
        "<td>PC Executable Build (Windows <code>.exe</code> / macOS <code>.app</code>) &mdash; <i>Siap diekspansi ke Android (<code>.apk</code>) pada Proyek Akhir (UAS)</i></td>",
        "<td>PC Executable Build (Windows <code>.exe</code> / macOS <code>.app</code>) &mdash; build terverifikasi: <b>macOS <code>.app</code></b>; <i>siap diekspansi ke Android (<code>.apk</code>) pada Proyek Akhir (UAS)</i></td>",
    ),
    # 3.2 solid collision props
    (
        "<td>Pohon Bambu, Pagar Batu, Bangunan Desa</td>",
        "<td>Pohon Bambu, Pagar Batu, Gapura, Pura, Bale, Pelinggih, dan Bangunan Desa</td>",
    ),
    # 5.2 animation approach
    (
        "menggunakan <code>Animator Controller</code> dan <i>Blend Tree</i> di Unity.",
        "menggunakan <code>Animator Controller</code> dengan 8 klip state (Idle dan Walking untuk 4 arah) yang dipanggil melalui <code>Animator.Play</code> sesuai arah hadap, tanpa <i>Blend Tree</i> agar transisi deterministik.",
    ),
    # 5.3 BGM
    (
        "<td><code>bgm_gender_girah.ogg</code></td>",
        "<td><code>bgm_gamelan_girah.ogg</code></td>",
    ),
    (
        "<td>Alunan instrumen tradisional Bali <i>Gamelan Gender Wayang</i> dan <i>Suling Bambu</i> yang diputar berulang selama permainan berlangsung.</td>",
        "<td>Rekaman otentik <i>Gend&eacute;r Wayang</i> (1928) dari ensambel <i>Gamelan Gender Wayang</i> Bali, berstatus <i>Public Domain</i> (Wikimedia Commons), diputar berulang selama permainan berlangsung.</td>",
    ),
    # 7 intro date
    ("Seluruh tautan repositori diperiksa pada 12 November 2026.",
     "Seluruh tautan repositori diperiksa pada 13 November 2026."),
    # 7.1 licence list: replace Pixabay/Freesound with Public Domain
    (
        '<li><b>Pixabay Content License / Freesound CC0 (Royalty-Free Audio):</b> mengizinkan penggunaan BGM dan SFX secara gratis di dalam permainan dan video demonstrasi <i>gameplay</i>. <a class="ref-link" href="https://pixabay.com/service/license-summary/" target="_blank">https://pixabay.com/service/license-summary/</a></li>',
        '<li><b>Public Domain (Wikimedia Commons):</b> rekaman historis yang telah menjadi milik publik, bebas digunakan tanpa atribusi wajib, termasuk untuk BGM dan video demonstrasi <i>gameplay</i>. <a class="ref-link" href="https://commons.wikimedia.org/wiki/Commons:Licensing" target="_blank">https://commons.wikimedia.org/wiki/Commons:Licensing</a></li>',
    ),
    (
        "seperti <i>Universal Render Pipeline 2D Lights</i> dan <i>TextMeshPro</i> pada lisensi <i>Unity Personal</i>.",
        "seperti <i>Universal Render Pipeline 2D Lights</i> pada lisensi <i>Unity Personal</i>.",
    ),
    # Table 7.1 row 1 coverage
    (
        "<td>Karakter, monster/roh, lontar, <i>tilemap</i> desa, UI, BGM, dan SFX</td>",
        "<td>Karakter, monster/roh, lontar, <i>tilemap</i> desa, UI, dan SFX</td>",
    ),
    # Table 7.1: Kenney -> Wikimedia Commons
    (
        """        <tr>
          <td style="text-align: center;">2</td>
          <td><b>Kenney Game Assets All-in-1</b> (<i>Tiny Town</i>, <i>Tiny Dungeon</i>, &amp; <i>UI Pack RPG</i>)</td>
          <td>Kenney Vleugels (Kenney.nl)</td>
          <td><i>Tilemap</i>, ikon lentera/obor, panel menu, dan tombol UI</td>
          <td><b>CC0 1.0</b></td>
          <td>
            &bull; <b>Katalog:</b> <a class="ref-link" href="https://kenney.nl/assets" target="_blank">buka</a><br>
            &bull; <b>Tiny Town:</b> <a class="ref-link" href="https://kenney.nl/assets/tiny-town" target="_blank">buka</a><br>
            &bull; <b>RPG UI:</b> <a class="ref-link" href="https://kenney.nl/assets/ui-pack-rpg-expansion" target="_blank">buka</a>
          </td>
        </tr>""",
        """        <tr>
          <td style="text-align: center;">2</td>
          <td><b>Wikimedia Commons</b> &mdash; <i>Gend&eacute;r Wayang</i> (1928)</td>
          <td>Gamelan Gender Wayang, Bali (rekaman 1928)</td>
          <td>BGM gamelan Bali (loop)</td>
          <td><b>Public Domain</b></td>
          <td>
            &bull; <b>Berkas:</b> <a class="ref-link" href="https://commons.wikimedia.org/wiki/File:Gend%C3%A9r_Wayang_(1928).ogg" target="_blank">buka</a><br>
            &bull; <b>Lisensi:</b> <a class="ref-link" href="https://commons.wikimedia.org/wiki/Commons:Licensing" target="_blank">buka</a>
          </td>
        </tr>""",
    ),
    # Table 7.1: Pixabay -> original CC0 art
    (
        """        <tr>
          <td style="text-align: center;">3</td>
          <td><b>Pixabay Royalty-Free Music</b> (gamelan &amp; suling bambu)</td>
          <td>Komunitas musisi Pixabay</td>
          <td>BGM gamelan dan suling bambu</td>
          <td><b>Pixabay License</b> (free)</td>
          <td>
            &bull; <b>Gamelan:</b> <a class="ref-link" href="https://pixabay.com/music/search/gamelan/" target="_blank">buka</a><br>
            &bull; <b>Suling:</b> <a class="ref-link" href="https://pixabay.com/music/search/bamboo%20flute/" target="_blank">buka</a>
          </td>
        </tr>""",
        """        <tr>
          <td style="text-align: center;">3</td>
          <td><b>Aset Orisinal Lentera Dirah</b> (lingkungan Bali &amp; kostum Bahula)</td>
          <td>Muhammad Sufyan (proyek ini)</td>
          <td>Gapura, beringin, meru, bale kulkul, pelinggih, penjor, backdrop menu, restyle Bahula</td>
          <td><b>CC0 1.0</b></td>
          <td>
            &bull; <b>Generator:</b> <code>Game/Tools/generate_balinese_assets.py</code><br>
            &bull; <b>Lisensi:</b> <code>Art/Environment/LICENSE_CC0.md</code>
          </td>
        </tr>""",
    ),
    # Table 7.1: remove Freesound row
    (
        """        <tr>
          <td style="text-align: center;">4</td>
          <td><b>Freesound CC0 Traditional Chimes &amp; Gamelan</b></td>
          <td>Komunitas Freesound</td>
          <td>SFX genta suci, gong, dan api obor</td>
          <td><b>CC0 / CC-BY</b></td>
          <td>
            &bull; <b>Freesound:</b> <a class="ref-link" href="https://freesound.org/search/?q=gamelan" target="_blank">buka</a><br>
            &bull; <b>Pixabay SFX:</b> <a class="ref-link" href="https://pixabay.com/sound-effects/search/bell%20chime/" target="_blank">buka</a>
          </td>
        </tr>
""",
        "",
    ),
    # Table 7.1: remove OpenGameArt row
    (
        """        <tr>
          <td style="text-align: center;">5</td>
          <td><b>OpenGameArt 2D Top-Down Collection</b></td>
          <td>Komunitas OpenGameArt</td>
          <td>Cadangan sprite obor, lontar, dan partikel cahaya</td>
          <td><b>CC0 1.0</b></td>
          <td><b>Portal:</b> <a class="ref-link" href="https://opengameart.org/" target="_blank">OpenGameArt</a></td>
        </tr>
""",
        "",
    ),
    # Table 7.1: renumber URP row
    (
        """          <td style="text-align: center;">6</td>
          <td><b>Unity URP 2D Lights</b></td>""",
        """          <td style="text-align: center;">4</td>
          <td><b>Unity URP 2D Lights</b></td>""",
    ),
    # Table 7.2 Bahula
    (
        "<td><code>Actor/Characters/Monk/SpriteSheet.png</code><br><i>(alternatif: <code>Villager/SpriteSheet.png</code>)</i></td>",
        "<td><code>Actor/Characters/Monk/SeparateAnim/Walk.png</code><br><i>(disimpan sebagai <code>Art/Characters/Bahula_SpriteSheet.png</code>)</i></td>",
    ),
    (
        "<td><code>16 x 16 px</code> per frame (grid 4 arah)</td>",
        "<td><code>16 x 16 px</code> per frame (64&times;64, 4 arah &times; 4 frame)</td>",
    ),
    (
        "<td>Murid padepokan Mpu Bharada; digunakan pada komponen <code>SpriteRenderer</code> dan <code>Animator</code> untuk state <code>Idle</code> dan <code>Walking</code> 4 arah.</td>",
        "<td>Murid padepokan Mpu Bharada; sprite di-<i>restyle</i> menjadi pakaian/kamen putih, udeng coklat, dan sabuk emas; digunakan pada komponen <code>SpriteRenderer</code> dan <code>Animator</code> untuk state <code>Idle</code> dan <code>Walking</code> 4 arah.</td>",
    ),
    # Table 7.2 spirit
    (
        "<td><code>Actor/Monsters/Spirit/SpriteSheet.png</code><br><i>(alternatif: <code>Ghost/SpriteSheet.png</code>)</i></td>",
        "<td><code>Actor/Monsters/Spirit/Spirit.png</code><br><i>(disimpan sebagai <code>Art/Monsters/ShadowSpirit_SpriteSheet.png</code>)</i></td>",
    ),
    (
        "<td><code>16 x 16 px</code> per frame</td>",
        "<td><code>16 x 16 px</code> per frame (64&times;64)</td>",
    ),
    # Table 7.3 items
    (
        "<td><code>Items/Scroll/ScrollEmpty.png</code> atau <code>Items/Scroll/ScrollThunder.png</code></td>",
        "<td><code>Items/Scroll/ScrollEmpty.png</code> (disimpan sebagai <code>Art/Items/Lontar.png</code>); varian <code>ScrollThunder.png</code> disimpan sebagai <code>Lontar_RwaBhineda.png</code></td>",
    ),
    (
        "<td><code>Items/Potion/MilkPot.png</code> atau <code>Items/Object/Lantern.png</code></td>",
        "<td><code>Items/Potion/MilkPot.png</code> (disimpan sebagai <code>Art/Items/OilJar.png</code>)</td>",
    ),
    (
        "<td><code>Backgrounds/Tilesets/TilesetElement.png</code> (sprite altar batu/patung kuil)</td>",
        "<td><code>Backgrounds/Tilesets/TilesetElement.png</code> &mdash; <i>tile</i> (7,2), sprite altar batu/patung kuil (disimpan sebagai <code>Art/Tilesets/TilesetElement.png</code>)</td>",
    ),
    # Table 7.4 walls
    (
        "<td><code>Backgrounds/Tilesets/TilesetNature.png</code> &amp; <code>TilesetHouse.png</code></td>",
        "<td><code>Backgrounds/Tilesets/TilesetNature.png</code> (kanopi pepohonan; disimpan sebagai <code>Art/Tilesets/TilesetNature.png</code>)</td>",
    ),
    (
        "<td>Rumpun pohon bambu, pagar batu desa, dan rumah tradisional sebagai pembatas lorong labirin desa.</td>",
        "<td>Rumpun pohon bambu/pepohonan dan pagar batu desa sebagai pembatas lorong labirin desa.</td>",
    ),
    # Table 7.5 UI
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
        "<td>Diimpor ke <code>TextMeshPro Font Asset</code> untuk keterbacaan (<i>clarity</i>) dan konsistensi visual.</td>",
        "<td>Komponen uGUI <code>Text</code> memakai font bawaan Unity karena metrik <i>glyph</i> <code>NormalFont.ttf</code> tidak konsisten (spasi dan lebar huruf), sehingga keterbacaan (<i>clarity</i>) lebih terjaga.</td>",
    ),
    # Table 7.6 BGM
    (
        "<td>Pixabay MP3 <i>atau</i> <code>Musics/2 - The Cave.ogg</code></td>",
        "<td><code>Wikimedia Commons</code> &mdash; <i>Gend&eacute;r Wayang</i> (1928), <i>Public Domain</i> (disimpan sebagai <code>Audio/BGM/bgm_gamelan_girah.ogg</code>)</td>",
    ),
    # 8.1 folder structure
    (
        "<li><code>Assets/_Project/Art/</code>, <code>Assets/_Project/Audio/</code>, dan <code>Assets/_Project/Scenes/</code> &mdash; Menyimpan sprite, tilemap, audio, dan scene utama.</li>",
        "<li><code>Assets/_Project/Art/</code> (<i>Characters</i>, <i>Monsters</i>, <i>Items</i>, <i>Tilesets</i>, <i>Environment</i>, <i>UI</i>, <i>Animations</i>, <i>Materials</i>), <code>Assets/_Project/Audio/</code> (<i>BGM</i>, <i>SFX</i>), dan <code>Assets/_Project/Scenes/</code> &mdash; Menyimpan sprite, tilemap, audio, dan scene utama.</li>\n      <li><code>Assets/_Project/Scripts/Editor/</code> &mdash; Berisi <code>LenteraDirahSceneBuilder.cs</code>, <code>ProjectConfigurator.cs</code>, <code>PlayModeSmokeTest.cs</code>, dan <code>PlayModePreviewCapture.cs</code> (otomasi konfigurasi aset, perakitan scene, build macOS, serta pengujian).</li>",
    ),
]

COSTUME_PARAGRAPH = """    <p>
      Kostum Bahula di-<i>restyle</i> agar merefleksikan busana adat Bali: kemeja dan kamen putih (<code>#F4EFE6</code>), udeng coklat (<code>#6B4A2F</code>), serta sabuk emas (<code>#FFB84D</code>), dengan kulit dan garis mata dipertahankan agar tetap terbaca pada ukuran 16&times;16 piksel.
    </p>

"""

ENVIRONMENT_PARAGRAPH = """    <p>
      <b>Aset lingkungan budaya Bali (orisinal, CC0 1.0).</b> Selain aset paket Ninja Adventure, prototipe ini memakai aset lingkungan yang digambar khusus melalui <code>Game/Tools/generate_balinese_assets.py</code> dan dilepas dengan lisensi CC0:
    </p>
    <ul>
      <li><code>Gapura_CandiBentar.png</code> (96&times;80) dan <code>Gapura_Menu.png</code> (192&times;160) &mdash; gapura keluar desa, gerbang sektor utara, serta latar panel Main Menu.</li>
      <li><code>PohonBeringin_Besar.png</code> (64&times;80) dan <code>PohonBeringin_Kecil.png</code> (40&times;56) &mdash; pohon beringin berakar gantung di alun-alun dan sektor desa.</li>
      <li><code>PuraMeru.png</code> (48&times;96) &mdash; pura meru bertingkat di sektor barat dan timur.</li>
      <li><code>BaleKulkul.png</code> (48&times;48) &mdash; bale kulkul di alun-alun dan sektor utara.</li>
      <li><code>Pelinggih.png</code> (24&times;32) &mdash; pelinggih di empat sudut alun-alun.</li>
      <li><code>Penjor.png</code> (16&times;64) &mdash; penjor bambu berhias di tepi alun-alun.</li>
    </ul>
    <p>
      Peta final memakai 2 gapura, 7 pohon beringin, 2 pura meru, 2 bale kulkul, 4 pelinggih, dan 6 penjor. Collider hanya dipasang pada bagian solid (tiang, batang, dasar bangunan) sehingga seluruh koridor tetap dapat dilewati.
    </p>

"""


def apply_html():
    with open(HTML_PATH, encoding="utf-8") as handle:
        text = handle.read()

    for old, new in HTML_REPLACEMENTS:
        count = text.count(old)
        if count != 1:
            raise SystemExit(f"HTML anchor muncul {count}x: {old[:90]!r}")
        text = text.replace(old, new)

    costume_anchor = '    <h2 class="section-title" id="gdd-5-2">5.2 Penerapan Prinsip Animasi Dasar (Basic Animation Principles)</h2>'
    if text.count(costume_anchor) != 1:
        raise SystemExit("Anchor 5.2 tidak unik")
    text = text.replace(costume_anchor, COSTUME_PARAGRAPH + costume_anchor)

    env_anchor = '    <h2 class="section-title" id="gdd-7-4">7.4 Aset UI/HUD dan Audio</h2>'
    if text.count(env_anchor) != 1:
        raise SystemExit("Anchor 7.4 tidak unik")
    text = text.replace(env_anchor, ENVIRONMENT_PARAGRAPH + env_anchor)

    with open(HTML_PATH, "w", encoding="utf-8") as handle:
        handle.write(text)

    print(f"HTML updated: {len(HTML_REPLACEMENTS) + 2} edits")


# --------------------------------------------------------------------------
# DOCX helpers
# --------------------------------------------------------------------------
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
    italic = template.italic if template is not None else None
    size = template.font.size if template is not None else None
    name = template.font.name if template is not None else None

    for child in list(paragraph._p):
        if child.tag.endswith("}pPr"):
            continue
        paragraph._p.remove(child)

    run = paragraph.add_run(text)
    run.bold = bold
    run.italic = italic
    if size is not None:
        run.font.size = size
    if name is not None:
        run.font.name = name


def set_cell_text(cell, text):
    paragraph = cell.paragraphs[0]
    template = paragraph.runs[0] if paragraph.runs else None
    bold = template.bold if template is not None else None
    italic = template.italic if template is not None else None
    size = template.font.size if template is not None else None
    name = template.font.name if template is not None else None

    for child in list(paragraph._p):
        if child.tag.endswith("}pPr"):
            continue
        paragraph._p.remove(child)

    run = paragraph.add_run(text)
    run.bold = bold
    run.italic = italic
    if size is not None:
        run.font.size = size
    if name is not None:
        run.font.name = name

    for extra in cell.paragraphs[1:]:
        extra._element.getparent().remove(extra._element)


def find_paragraph(doc, needle):
    for paragraph in doc.paragraphs:
        if needle in paragraph.text:
            return paragraph
    raise SystemExit(f"Paragraf tidak ditemukan: {needle[:80]!r}")


def find_heading(doc, prefix):
    for paragraph in doc.paragraphs:
        if paragraph.text.strip().startswith(prefix):
            return paragraph
    raise SystemExit(f"Heading tidak ditemukan: {prefix!r}")


def delete_row(table, index):
    row = table.rows[index]._tr
    row.getparent().remove(row)


def copy_paragraph_formatting(target, source):
    """Give an inserted paragraph the same list/indent formatting as a bullet."""
    source_pPr = source._p.pPr
    if source_pPr is None:
        return

    target_p = target._p
    existing = target_p.pPr
    if existing is not None:
        target_p.remove(existing)

    target_p.insert(0, copy.deepcopy(source_pPr))


def apply_docx():
    doc = Document(DOCX_PATH)
    tables = doc.tables

    # --- paragraphs -------------------------------------------------------
    paragraph = find_paragraph(doc, "12 November 2026")
    replace_in_paragraph(paragraph, "12 November 2026", "13 November 2026")

    paragraph = find_paragraph(doc, "Blend Tree")
    replace_in_paragraph(
        paragraph,
        "menggunakan Animator Controller dan Blend Tree di Unity.",
        "menggunakan Animator Controller dengan 8 klip state (Idle dan Walking untuk 4 arah) yang dipanggil melalui Animator.Play sesuai arah hadap, tanpa Blend Tree agar transisi deterministik.",
    )

    paragraph = find_paragraph(doc, "Pixabay Content License / Freesound CC0")
    set_paragraph_text(
        paragraph,
        "Public Domain (Wikimedia Commons): rekaman historis yang telah menjadi milik publik, bebas digunakan tanpa atribusi wajib, termasuk untuk BGM dan video demonstrasi gameplay. https://commons.wikimedia.org/wiki/Commons:Licensing",
    )

    paragraph = find_paragraph(doc, "Unity Companion License")
    replace_in_paragraph(
        paragraph,
        "Universal Render Pipeline 2D Lights dan TextMeshPro pada lisensi Unity Personal",
        "Universal Render Pipeline 2D Lights pada lisensi Unity Personal",
    )

    art_bullet = find_paragraph(doc, "Assets/_Project/Art/, Assets/_Project/Audio/")
    set_paragraph_text(
        art_bullet,
        "Assets/_Project/Art/ (Characters, Monsters, Items, Tilesets, Environment, UI, Animations, Materials), Assets/_Project/Audio/ (BGM, SFX), dan Assets/_Project/Scenes/ — Menyimpan sprite, tilemap, audio, dan scene utama.",
    )

    # --- tables -----------------------------------------------------------
    set_cell_text(tables[2].rows[4].cells[1],
                  "Unity 6000.6.9f1 — 2D (Universal Render Pipeline 17.6 / URP 2D Lights) dengan bahasa pemrograman C#")
    set_cell_text(tables[2].rows[5].cells[1],
                  "PC Executable Build (Windows .exe / macOS .app) — build terverifikasi: macOS .app; siap diekspansi ke Android (.apk) pada Proyek Akhir (UAS)")

    set_cell_text(tables[6].rows[1].cells[1],
                  "Pohon Bambu, Pagar Batu, Gapura, Pura, Bale, Pelinggih, dan Bangunan Desa")

    set_cell_text(tables[10].rows[1].cells[0], "bgm_gamelan_girah.ogg")
    set_cell_text(tables[10].rows[1].cells[2],
                  "Rekaman otentik Gendér Wayang (1928) dari ensambel Gamelan Gender Wayang Bali, berstatus Public Domain (Wikimedia Commons), diputar berulang selama permainan berlangsung.")

    # Table 7.1 master repositories: 6 data rows -> 4
    repo = tables[14]
    set_cell_text(repo.rows[1].cells[3],
                  "Karakter, monster/roh, lontar, tilemap desa, UI, dan SFX")
    set_cell_text(repo.rows[2].cells[0], "2")
    set_cell_text(repo.rows[2].cells[1], "Wikimedia Commons — Gendér Wayang (1928)")
    set_cell_text(repo.rows[2].cells[2], "Gamelan Gender Wayang, Bali (rekaman 1928)")
    set_cell_text(repo.rows[2].cells[3], "BGM gamelan Bali (loop)")
    set_cell_text(repo.rows[2].cells[4], "Public Domain")
    set_cell_text(repo.rows[2].cells[5],
                  "• Berkas: https://commons.wikimedia.org/wiki/File:Gend%C3%A9r_Wayang_(1928).ogg\n• Lisensi: https://commons.wikimedia.org/wiki/Commons:Licensing")
    set_cell_text(repo.rows[3].cells[0], "3")
    set_cell_text(repo.rows[3].cells[1], "Aset Orisinal Lentera Dirah (lingkungan Bali & kostum Bahula)")
    set_cell_text(repo.rows[3].cells[2], "Muhammad Sufyan (proyek ini)")
    set_cell_text(repo.rows[3].cells[3],
                  "Gapura, beringin, meru, bale kulkul, pelinggih, penjor, backdrop menu, restyle Bahula")
    set_cell_text(repo.rows[3].cells[4], "CC0 1.0")
    set_cell_text(repo.rows[3].cells[5],
                  "• Generator: Game/Tools/generate_balinese_assets.py\n• Lisensi: Art/Environment/LICENSE_CC0.md")
    delete_row(repo, 5)
    delete_row(repo, 4)
    set_cell_text(repo.rows[4].cells[0], "4")

    # Table 7.2 characters
    characters = tables[15]
    set_cell_text(characters.rows[1].cells[1],
                  "Actor/Characters/Monk/SeparateAnim/Walk.png\n(disimpan sebagai Art/Characters/Bahula_SpriteSheet.png)")
    set_cell_text(characters.rows[1].cells[2], "16 x 16 px per frame (64x64, 4 arah x 4 frame)")
    set_cell_text(characters.rows[1].cells[3],
                  "Murid padepokan Mpu Bharada; sprite di-restyle menjadi pakaian/kamen putih, udeng coklat, dan sabuk emas; digunakan pada komponen SpriteRenderer dan Animator untuk state Idle dan Walking 4 arah.")
    set_cell_text(characters.rows[3].cells[1],
                  "Actor/Monsters/Spirit/Spirit.png\n(disimpan sebagai Art/Monsters/ShadowSpirit_SpriteSheet.png)")
    set_cell_text(characters.rows[3].cells[2], "16 x 16 px per frame (64x64)")

    # Table 7.3 artefacts
    items = tables[16]
    set_cell_text(items.rows[1].cells[1],
                  "Items/Scroll/ScrollEmpty.png\n(disimpan sebagai Art/Items/Lontar.png); varian ScrollThunder.png disimpan sebagai Lontar_RwaBhineda.png")
    set_cell_text(items.rows[2].cells[1],
                  "Items/Potion/MilkPot.png\n(disimpan sebagai Art/Items/OilJar.png)")
    set_cell_text(items.rows[3].cells[1],
                  "Backgrounds/Tilesets/TilesetElement.png — tile (7,2), sprite altar batu/patung kuil (disimpan sebagai Art/Tilesets/TilesetElement.png)")

    # Table 7.4 tilesets
    tilesets = tables[17]
    set_cell_text(tilesets.rows[2].cells[1],
                  "Backgrounds/Tilesets/TilesetNature.png (kanopi pepohonan; disimpan sebagai Art/Tilesets/TilesetNature.png)")
    set_cell_text(tilesets.rows[2].cells[3],
                  "Rumpun pohon bambu/pepohonan dan pagar batu desa sebagai pembatas lorong labirin desa.")

    # Table 7.5 UI
    ui = tables[18]
    set_cell_text(ui.rows[2].cells[1],
                  "HUD/NinePathRect/FacesetBox.png (bingkai dialog) & HUD/NinePathRect/DialogueBubble.png (tombol)")
    set_cell_text(ui.rows[3].cells[0], "Font UI")
    set_cell_text(ui.rows[3].cells[1],
                  "HUD/Font/NormalFont.ttf (diarsipkan); UI memakai font bawaan Unity (LegacyRuntime.ttf)")
    set_cell_text(ui.rows[3].cells[2],
                  "Komponen uGUI Text memakai font bawaan Unity karena metrik glyph NormalFont.ttf tidak konsisten (spasi dan lebar huruf), sehingga keterbacaan (clarity) lebih terjaga.")

    # Table 7.6 audio sources
    audio = tables[19]
    set_cell_text(audio.rows[1].cells[1],
                  "Wikimedia Commons — Gendér Wayang (1928), Public Domain\n(disimpan sebagai Audio/BGM/bgm_gamelan_girah.ogg)")
    set_cell_text(audio.rows[1].cells[2],
                  "Diputar berulang sejak permainan dimulai (loop, volume 0.35).")

    # --- insert new sections ---------------------------------------------
    body_style = find_paragraph(doc, "Gaya visual menggunakan pendekatan").style
    bullet_template = find_paragraph(doc, "Assets/_Project/Scripts/Managers/")

    costume_heading = find_heading(doc, "5.2 Penerapan Prinsip Animasi Dasar")
    costume = costume_heading.insert_paragraph_before()
    if body_style is not None:
        costume.style = body_style
    costume.add_run(
        "Kostum Bahula di-restyle agar merefleksikan busana adat Bali: kemeja dan kamen putih (#F4EFE6), "
        "udeng coklat (#6B4A2F), serta sabuk emas (#FFB84D), dengan kulit dan garis mata dipertahankan agar "
        "tetap terbaca pada ukuran 16x16 piksel."
    )

    env_heading = find_heading(doc, "7.4 Aset UI/HUD dan Audio")

    intro = env_heading.insert_paragraph_before()
    if body_style is not None:
        intro.style = body_style
    bold_run = intro.add_run("Aset lingkungan budaya Bali (orisinal, CC0 1.0). ")
    bold_run.bold = True
    intro.add_run(
        "Selain aset paket Ninja Adventure, prototipe ini memakai aset lingkungan yang digambar khusus "
        "melalui Game/Tools/generate_balinese_assets.py dan dilepas dengan lisensi CC0:"
    )

    bullets = [
        "Gapura_CandiBentar.png (96x80) dan Gapura_Menu.png (192x160) — gapura keluar desa, gerbang sektor utara, serta latar panel Main Menu.",
        "PohonBeringin_Besar.png (64x80) dan PohonBeringin_Kecil.png (40x56) — pohon beringin berakar gantung di alun-alun dan sektor desa.",
        "PuraMeru.png (48x96) — pura meru bertingkat di sektor barat dan timur.",
        "BaleKulkul.png (48x48) — bale kulkul di alun-alun dan sektor utara.",
        "Pelinggih.png (24x32) — pelinggih di empat sudut alun-alun.",
        "Penjor.png (16x64) — penjor bambu berhias di tepi alun-alun.",
    ]

    for bullet in bullets:
        paragraph = env_heading.insert_paragraph_before()
        paragraph.add_run(bullet)
        copy_paragraph_formatting(paragraph, bullet_template)

    closing = env_heading.insert_paragraph_before()
    if body_style is not None:
        closing.style = body_style
    closing.add_run(
        "Peta final memakai 2 gapura, 7 pohon beringin, 2 pura meru, 2 bale kulkul, 4 pelinggih, dan 6 penjor. "
        "Collider hanya dipasang pada bagian solid (tiang, batang, dasar bangunan) sehingga seluruh koridor tetap dapat dilewati."
    )

    editor_bullet = find_heading(doc, "8.2 Peta Jalan Ekspansi")
    new_bullet = editor_bullet.insert_paragraph_before()
    new_bullet.add_run(
        "Assets/_Project/Scripts/Editor/ — Berisi LenteraDirahSceneBuilder.cs, ProjectConfigurator.cs, "
        "PlayModeSmokeTest.cs, dan PlayModePreviewCapture.cs (otomasi konfigurasi aset, perakitan scene, build macOS, serta pengujian)."
    )
    copy_paragraph_formatting(new_bullet, bullet_template)

    doc.save(DOCX_PATH)
    print("DOCX updated")


if __name__ == "__main__":
    apply_html()
    apply_docx()
    print("Done.")
