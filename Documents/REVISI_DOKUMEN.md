# Revisi Dokumen — Sinkronisasi GDD & Referensi Aset dengan Build Final

Tanggal: 13 November 2026
Branch: `docs/gdd-audit`

Dokumen yang disesuaikan:

- `Documents/GDD/…GDD….docx`
- `Documents/GDD/…GDD….pdf`
- `Documents/HTML Artifacts/…GDD….html`
- `Documents/HTML Artifacts/…Daftar_Referensi_Assets….html`

Laporan Studi Literatur **tidak diubah** karena tidak memuat klaim teknis implementasi.

---

## Prinsip kerja

Hanya bagian yang **tidak lagi sesuai** dengan game yang diubah. Seluruh nilai mekanik, palet warna, naskah dialog, FSM, collision, dan pencahayaan yang sudah sesuai **dibiarkan apa adanya**.

## Tabel audit GDD vs game

| # | Lokasi | Isi dokumen sebelumnya | Kondisi implementasi | Tindakan |
|---|---|---|---|---|
| 1 | §1.1 Engine | Unity 2D (URP 2D Lights) | Unity **6000.6.9f1**, URP **17.6** | Ditambahkan versi |
| 2 | §1.1 Platform | Windows .exe / macOS .app | Build terverifikasi **macOS .app** | Ditambahkan keterangan build terverifikasi |
| 3 | §3.2 Solid Collision | Pohon Bambu, Pagar Batu, Bangunan Desa | Ada gapura, pura meru, bale kulkul, pelinggih (BoxCollider2D) | Daftar objek dilengkapi |
| 4 | §5.2 Animasi | Animator Controller + **Blend Tree** | Animator Controller **8 state clip** + `Animator.Play`, tanpa Blend Tree | Kalimat diperbaiki |
| 5 | §5.3 BGM | `bgm_gender_girah.ogg`, gender wayang + suling | **`bgm_gamelan_girah.ogg`**, rekaman Gendér Wayang 1928, Public Domain, tanpa suling | Nama file & deskripsi diperbaiki |
| 6 | §7 pembuka | Tautan diperiksa 12 Nov 2026 | Diperiksa 13 Nov 2026 | Tanggal diperbarui |
| 7 | §7.1 lisensi #2 | Pixabay/Freesound | Tidak dipakai; BGM dari Wikimedia (Public Domain) | Diganti butir Public Domain |
| 8 | §7.1 lisensi #3 | Menyebut TextMeshPro | UI memakai uGUI Text | Penyebutan TMP dihapus |
| 9 | Tabel 7.1 | 6 sumber (Ninja, Kenney, Pixabay, Freesound, OGA, URP) | 4 sumber nyata (Ninja, Wikimedia, aset orisinal, URP) | Tabel direstrukturisasi |
| 10 | Tabel 7.2 Bahula | `Monk/SpriteSheet.png` | `Monk/SeparateAnim/Walk.png` (64×64) + restyle | Path, resolusi, deskripsi diperbaiki |
| 11 | Tabel 7.2 Musuh | `Monsters/Spirit/SpriteSheet.png` | `Monsters/Spirit/Spirit.png` (64×64) | Path & resolusi diperbaiki |
| 12 | Tabel 7.3 Lontar | ScrollEmpty / ScrollThunder | `Lontar.png`; varian `Lontar_RwaBhineda.png` | Path diperjelas |
| 13 | Tabel 7.3 Minyak | MilkPot / Lantern | `MilkPot.png` → `OilJar.png` | Path diperjelas |
| 14 | Tabel 7.3 Altar | TilesetElement | Tile **(7,2)**, skala 2.2 | Detail tile ditambahkan |
| 15 | Tabel 7.4 Dinding | TilesetNature **& TilesetHouse** | Hanya `TilesetNature.png` | TilesetHouse dihapus |
| 16 | Tabel 7.5 Panel | DialogBoxSimple & NinePathRect | **FacesetBox** (bingkai) & **DialogueBubble** (tombol) | Path diperbaiki |
| 17 | Tabel 7.5 Font | NormalFont → TextMeshPro | **Font bawaan Unity (LegacyRuntime) + uGUI Text**; NormalFont diarsipkan | Path & deskripsi diperbaiki |
| 18 | Tabel 7.6 BGM | Pixabay / `Musics/2 - The Cave.ogg` | Wikimedia — Gendér Wayang (1928), PD | Path diperbaiki |
| 19 | §8.1 Struktur | Tanpa folder Editor | Ada `Scripts/Editor` + `Art/Environment`, `Animations`, `Materials` | Bullet ditambahkan |
| 20 | §7.3 | — | **Aset lingkungan Bali orisinal CC0** (8 berkas) | Subbagian baru (paragraf + bullet) |
| 21 | §5.1 | — | **Kostum Bahula**: putih `#F4EFE6`, udeng `#6B4A2F`, sabuk `#FFB84D` | Paragraf baru |
| 22 | Referensi Aset | Sumber pihak ketiga yang tidak dipakai | Sumber nyata + aset orisinal | Tabel 2.1, 3.1–3.3, 4.1–4.2 diperbarui; **§4.4 baru** |

## Perubahan per dokumen

### GDD
- 33 penggantian teks pada HTML dan padanannya di DOCX (termasuk penghapusan 2 baris tabel 7.1 dan penomoran ulang).
- 2 paragraf/subbagian baru: kostum Bahula (§5.1) dan aset lingkungan Bali (akhir §7.3).
- 1 bullet baru pada §8.1 (folder `Scripts/Editor`).
- PDF diregenerasi dari HTML yang sama.

### Daftar Referensi Aset
- 27 penggantian + 1 subbagian baru **§4.4 Aset Lingkungan Budaya Bali & Kostum Bahula**, termasuk entri daftar isi.
- Tabel master repositori menjadi 4 sumber nyata (Ninja Adventure, Wikimedia Commons, aset orisinal, URP).
- Panduan unduh §2.2 diganti: panduan BGM Wikimedia + catatan generator aset orisinal.

## Verifikasi

| Pemeriksaan | Hasil |
|---|---|
| DOCX dibuka ulang (python-docx) | valid, 20 tabel, tanpa error |
| String baru ada di DOCX | `bgm_gamelan_girah.ogg`, `SeparateAnim/Walk.png`, `Spirit/Spirit.png`, `FacesetBox`, `LegacyRuntime`, `Scripts/Editor`, `Gapura_CandiBentar.png`, `udeng coklat`, `6000.6.9f1`, `13 November 2026` — semua **OK** |
| String lama hilang | `DialogBoxSimple`, `TilesetHouse`, `bgm_gender_girah`, `TextMeshPro`, `Kenney`, `Freesound`, `OpenGameArt` (pada tabel sumber), `2 - The Cave`, `12 November 2026` — **hilang** |
| Tabel 7.1 | 5 baris (1 header + 4 sumber), penomoran 1–4 |
| Bullet baru (DOCX) | memakai `numPr` yang sama dengan bullet lama |
| PDF | 16 halaman, teks baru terverifikasi, latar tabel/palet tetap tercetak |
| Visual PDF | Halaman Bab V, VII, VIII diperiksa: tabel tidak rusak, bullet tampil |
| HTML Referensi Aset | 9 halaman saat dicetak, §4.4 tampil rapi, TOC diperbarui |

## Reproduksi

Skrip perubahan disimpan agar dapat diaudit/diulang:

- `Documents/tools/update_gdd.py`
- `Documents/tools/update_assets_doc.py`

Skrip bersifat sekali-jalan terhadap dokumen asli (mengandalkan teks lama sebagai anchor), sehingga untuk regenerasi gunakan dokumen versi sebelum revisi.
