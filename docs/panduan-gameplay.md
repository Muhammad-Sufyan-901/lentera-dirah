# Lentera Dirah: Lontar Mpu Bharada — Panduan Menjalankan, Menguji, & Build

Prototipe 2D Top-Down bertema budaya Bali (Calonarang / Rwa Bhineda).
Unity **6000.6.9f1** · URP **17.6** (2D Lights) · C#
Seluruh source code & executable ada di folder **`Game/`**.

---

## 1. Menjalankan di Unity Editor (macOS)

1. Buka **Unity Hub** → `Add` → pilih folder `Game/` (yang berisi `Assets`, `Packages`, `ProjectSettings`).
2. Buka dengan Unity **6000.6.9f1**. Tunggu impor pertama selesai (Library dibuat otomatis).
3. Di menu bar Unity, jalankan berurutan:
   - **`Tools → Lentera Dirah → 1. Configure Pixel Art Assets & Tags`**
     Mengatur tag `Player/Enemy/Obstacle`, layer, impor pixel-art (PPU **16**, Filter **Point**, Compression **None**), pemotongan sprite 16×16, material `Sprite-Lit-Default`, dan Animator 4 arah.
   - **`Tools → Lentera Dirah → 2. Build Complete Prototype Scene`**
     Merakit seluruh scene: Global Light 2D, Tilemap desa, Player + Lentera, 3 musuh, 3 Lontar, 3 Minyak, Altar, kamera, dan seluruh Canvas UI beserta binding referensinya. Scene tersimpan di `Assets/_Project/Scenes/LenteraDirah_Girah.unity` dan otomatis masuk *Build Settings*.
   - (opsional) **`Tools → Lentera Dirah → Run Full Setup (1 then 2)`** untuk sekali klik.
4. Tekan **Play**.

### Alur uji (User Flow)
`Main Menu` → klik **MULAI BERMAIN** → **PILIH KESULITAN** (Mudah/Normal/Sulit)
→ dialog Mpu Bharada → `Level 1: Desa Girah` → `Level 2: Hutan Bambu Lemah Tulis` → `Level 3: Pelataran Setra Gandamayu`
→ setiap level selesai dengan mengumpulkan 3 Lontar lalu menyentuh Altar → **halaman hasil** menampilkan skor level, skor total, dan gelar
→ **LEVEL BERIKUTNYA** atau **MENU UTAMA**; pada level 3 tombol menjadi **SELESAI**.

Jika nyawa habis atau energi 0%, muncul **Game Over** dengan skor total dan tombol **COBA LAGI** (mengulang level saat ini) atau **MENU UTAMA**.

Dari Main Menu: **CARA BERMAIN** membuka panduan, **PENGATURAN** membuka slider BGM/SFX + layar penuh, **KREDIT** menampilkan atribusi aset, **KELUAR** menutup game.
Saat bermain, `Esc` membuka **JEDA** (Lanjutkan / Pengaturan / Ke Menu Utama); `Esc` lagi melanjutkan permainan.

### Tiga Level (baru)

| Level | Peta | Tema | Musuh | Objektif |
|---|---|---|---|---|
| 1 | Desa Girah Bagian Luar | desa & alun-alun | 3 | 3 Lontar di sektor utara/barat/timur |
| 2 | Hutan Bambu Lemah Tulis | lorong bambu & clearing | 4 | 3 Lontar di clearing utara/barat/timur |
| 3 | Pelataran Setra Gandamayu | plaza setra & pura | 5 | 3 Lontar di pura utara & sayap barat/timur |

Setiap level memiliki altar sendiri, 3 Minyak Obor, dan reset penuh untuk energi/nyawa saat dimulai. Skor dan total diakumulasikan; rekor skor disimpan setelah level 3.

### Tingkat Kesulitan (halaman terpisah)

| Kesulitan | Laju energi | Kecepatan musuh | Deteksi musuh | Pengali skor |
|---|---|---|---|---|
| Mudah | 1.5%/dtk (×0.75) | ×0.85 | ×0.80 | ×1.00 |
| Normal | 2.0%/dtk (×1.00) | ×1.00 | ×1.00 | ×1.25 |
| Sulit | 2.7%/dtk (×1.35) | ×1.15 | ×1.25 | ×1.50 |

Pilihan dilakukan setelah **MULAI BERMAIN**, diterapkan ke seluruh level, dan disimpan di `PlayerPrefs`.

### Mekanik 3 — Rwa Bhineda Exposure (baru)
Radius deteksi efektif musuh = `detectRadius × pengali kesulitan × Lerp(0.7, 1.3, energi/100)`.
Lentera penuh membuat musuh mendeteksi hingga **+30%** lebih jauh; lentera redup menyamarkan hingga **-30%**.
HUD menampilkan status `CAHAYA: TERANG / SEIMBANG / REDUP` beserta persentase deteksi saat ini.

### Hasil Akhir, Skor, & Gelar

Skor level = `(500 + bonus waktu + nyawa×100 + energi×2) × pengali kesulitan`.
Bonus waktu dimulai dari 600 dan berkurang 5 per detik. Skor total adalah akumulasi ketiga level; rekor skor disimpan di `PlayerPrefs` setelah level 3.

| Gelar | Syarat |
|---|---|
| **Penyuci Agung** | waktu level ≤ 2:30 dan nyawa tetap 3 |
| **Murid Teladan** | waktu level ≤ 4:00 dan nyawa ≥ 2 |
| **Pejalan Malam** | selain kondisi di atas |

Panel hasil menampilkan skor level, skor total, gelar, dan rekor (pada level 3).

---

## 2. Kontrol

| Aksi | Input |
|---|---|
| Bergerak 4 arah | `W A S D` atau panah |
| Holy Light Burst (stun 3 dtk) | `SPACE` |
| Lanjut dialog | `E` atau klik tombol |
| Jeda / lanjut | `ESC` |
| Mulai bermain | **MULAI BERMAIN** → pilih kesulitan |
| Buka pengaturan | **PENGATURAN** di Main Menu atau di panel Jeda |
| Buka panduan | Tombol **CARA BERMAIN** di Main Menu |
| Buka kredit | Tombol **KREDIT** di Main Menu |
| Keluar dari game | Tombol **KELUAR** di Main Menu |

Parameter (sesuai GDD): kecepatan **4.5**, decay lentera **2%/dtk** (Normal), radius cahaya **6.0 → 1.8**, burst **-15%** energi, cooldown **4 dtk**, radius stun **3.5**, nyawa **3**, invulnerability **1 dtk**, patroli **2.2**, kejar **3.4**, deteksi **4.0**, lepas **5.5**, exposure **×0.7–×1.3**.

---

## 3. Checklist Verifikasi Rubrik

| Kriteria | Cara memastikan | Status |
|---|---|---|
| **Input & Movement** | `WASD`/panah menggerakkan Bahula; diagonal tidak lebih cepat (dinormalisasi); animasi jalan 4 arah | ✅ |
| **Solid Collision** | Menabrak dinding/pohon desa (TilemapCollider2D, layer `Obstacle`) tidak menembus | ✅ |
| **Trigger Collision** | Menyentuh Lontar → counter HUD naik + SFX + kutipan; Minyak → energi +35%; Altar → cek 3 Lontar | ✅ |
| **FSM Level 1 (Game)** | `MainMenu → DifficultySelect → IntroDialog → Playing ⇄ Paused → Victory/GameOver`; input & AI berhenti di luar `Playing` | ✅ |
| **FSM Level 2 (Player)** | `Idle / Walking / CastingLight (0.3 dtk) / Hurt (1 dtk, kedip merah)` | ✅ |
| **FSM Level 3 (Enemy)** | `Patrol → Chase` (≤4.0) `→ Stunned` (3 dtk, tint sian transparan, berhenti melukai) | ✅ |
| **Mekanik 1 — Lontar & Segel Altar** | Kumpulkan 3 Lontar (Usada, Dharma, Rwa Bhineda) → segel terbuka (cahaya emas) → Victory | ✅ |
| **Mekanik 2 — Lentera Dinamis & Stun Burst** | Bar energi turun 2%/dtk, radius `Light 2D` menyusut; `SPACE` memotong 15% & menstun musuh radius 3.5 | ✅ |
| **Mekanik 3 — Rwa Bhineda Exposure** | Deteksi musuh membesar saat energi tinggi dan mengecil saat energi rendah; status tampil di HUD | ✅ |
| **Alur Pilih Kesulitan** | `MULAI BERMAIN` membuka halaman kesulitan; pilihan berlaku untuk 3 level | ✅ |
| **Tiga Level** | Desa Girah, Hutan Bambu Lemah Tulis, Pelataran Setra Gandamayu; masing-masing 3 Lontar + altar | ✅ |
| **Hasil & Progres Level** | Panel hasil menampilkan skor level/total/gelar; tombol level berikutnya atau menu | ✅ |
| **Menu Pengaturan & Jeda** | Slider BGM/SFX, layar penuh; `Esc` membuka Jeda dan `Esc` lagi melanjutkan | ✅ |
| **Skor, Gelar, & Rekor** | Skor dihitung dari waktu/nyawa/energi × kesulitan; rekor tersimpan setelah level 3 | ✅ |
| **Game Over** | Menampilkan skor total, **COBA LAGI** (ulang level) dan **MENU UTAMA** | ✅ |
| **Layar Kredit** | Atribusi Ninja Adventure, Wikimedia, aset orisinal, dan URP | ✅ |
| **Animasi** | Walk cycle 4 arah (Animator Controller), Lontar/Minyak mengambang `Mathf.Sin`, kilatan cahaya saat burst | ✅ |
| **Audio** | BGM gamelan/malam looping, 5 SFX event (ambil Lontar, burst, isi minyak, hurt, victory) | ✅ |
| **UI/UX & Budaya** | HUD hati/energi/Lontar, panel dialog berpotret Mpu Bharada, palet Dirah Midnight–Sacred Gold–Gering Violet–Stun Cyan | ✅ |

Cek cepat di Editor: buka scene → pilih `Player (Bahula)` (lihat `PlayerController`: 4 state), `EnemyBayangan_*` (`EnemyShadowAI`: 3 state), `_Managers` (`GameManager`: 5 state).

---

## 4. Build Executable macOS (`.app`)

### A. Otomatis dari menu Unity
`Tools → Lentera Dirah → 3. Build macOS App`
Hasil: `Game/Builds/macOS/LenteraDirah.app` (scene langsung dipakai, tanpa setting manual).

### B. Manual lewat Build Settings
1. `File → Build Settings…` (Unity 6: `File → Build Profiles`).
2. Platform **macOS**, Target Architecture **Intel 64-bit + Apple silicon**.
3. Pastikan scene `Assets/_Project/Scenes/LenteraDirah_Girah.unity` tercentang.
4. `Build` → simpan ke `Game/Builds/macOS/LenteraDirah.app`.
5. Jalankan: `open Game/Builds/macOS/LenteraDirah.app` (jika Gatekeeper menolak: klik kanan → *Open*, atau `xattr -dr com.apple.quarantine <path>`).

### C. Build via CLI (tanpa membuka Editor)
```bash
"/Applications/Unity/Hub/Editor/6000.6.9f1/Unity.app/Contents/MacOS/Unity" \
  -batchmode -quit \
  -projectPath "$(pwd)/Game" \
  -executeMethod LenteraDirah.Editor.LenteraDirahSceneBuilder.BuildMacApp \
  -logFile -
```

### D. Build Executable Windows (`.exe`)

Prasyarat: modul **Windows Build Support (Mono)** terpasang di Editor
(Unity Hub → *Installs* → ⚙️ pada 6000.6.9f1 → *Add modules*).

`Tools → Lentera Dirah → 3. Build Windows EXE`
Hasil: `Game/Builds/Windows/LenteraDirah.exe` (arsitektur **x64**, diset eksplisit di
`BuildWindowsApp()` agar tidak mengikuti arsitektur host macOS ARM).

Via CLI:

```bash
"/Applications/Unity/Hub/Editor/6000.6.9f1/Unity.app/Contents/MacOS/Unity" \
  -batchmode -quit \
  -projectPath "$(pwd)/Game" \
  -executeMethod LenteraDirah.Editor.LenteraDirahSceneBuilder.BuildWindowsApp \
  -logFile -
```

Folder `Game/Builds/Windows/` harus disalin **utuh** ke mesin Windows — `LenteraDirah.exe`
tidak bisa dipisahkan dari `LenteraDirah_Data/`, `UnityPlayer.dll`, dan `MonoBleedingEdge/`.
Build bersifat unsigned, jadi Windows SmartScreen dapat menampilkan peringatan saat pertama
dijalankan (*More info → Run anyway*).

---

## 5. Skenario Rekaman Video Demo (3–4 menit)

| Waktu | Aksi yang direkam |
|---|---|
| 0:00–0:08 | Main Menu: judul **LENTERA DIRAH**, tunjukkan tombol Mulai, Cara Bermain, Pengaturan, Kredit, Keluar |
| 0:08–0:18 | Klik **MULAI BERMAIN** → halaman **PILIH KESULITAN** → pilih **NORMAL** |
| 0:18–0:28 | Dialog Mpu Bharada → **MENGERTI (E)** |
| 0:28–0:55 | **Level 1 — Desa Girah**: jelajah, status TERANG, musuh mendekat, `SPACE` stun, ambil Minyak + Lontar |
| 0:55–1:10 | Ambil Lontar sisanya → Altar terbuka → sentuh Altar → **hasil level 1** (skor, gelar) → **LEVEL BERIKUTNYA** |
| 1:10–1:40 | **Level 2 — Hutan Bambu Lemah Tulis**: lorong sempit, 4 musuh, ambil 3 Lontar → Altar → hasil level 2 |
| 1:40–2:10 | **Level 3 — Pelataran Setra Gandamayu**: plaza & pura, 5 musuh, status REDUP, ambil 3 Lontar → Altar |
| 2:10–2:25 | **Hasil akhir**: SEMUA LEVEL SELESAI, skor level/total, rekor, tombol **SELESAI** → Menu |
| 2:25–2:40 | (Opsional) `ESC` → panel **JEDA** → **PENGATURAN** → kembali; atau Game Over lalu **COBA LAGI** |
| 2:40–2:55 | (Opsional) **KREDIT** dan **CARA BERMAIN** |

Tips rekaman: `Cmd+Shift+5` (QuickTime screen recording), resolusi jendela 1920×1080, aktifkan suara sistem agar BGM/SFX terdengar. Untuk build macOS, jalankan `Game/Builds/macOS/LenteraDirah.app`.

---

## 6. Struktur Proyek

```
.
├── Game/                          # proyek Unity (dibuka lewat Unity Hub)
│   ├── Assets/
│   │   ├── Settings/              # URP + Input System
│   │   └── _Project/
│   │       ├── Animation/         # 2 AnimatorController + 9 klip
│   │       ├── Art/               # Characters, Monsters, Environment, Items, Tilesets, UI, Materials
│   │       ├── Audio/             # BGM, SFX
│   │       ├── Prefabs/           # LontarSuci, MinyakObor, AltarPenyucian
│   │       ├── Scenes/            # LenteraDirah_Girah.unity
│   │       └── Scripts/           # Managers, Player, Enemies, Interactables, Editor (+ asmdef)
│   ├── Docs/                      # screenshot hasil render
│   ├── Builds/                    # macOS/LenteraDirah.app, Windows/ (tidak di-commit)
│   └── Packages/  ProjectSettings/
├── docs/                          # gdd/, laporan/, html/, plan/, panduan-gameplay.md
├── tools/                         # assets/ (generator aset), docs/ (generator dokumen)
├── media/gameplay/                # rekaman demo (.mp4 tidak di-commit)
└── dist/                          # arsip zip distribusi (tidak di-commit)
```

## 7. Troubleshooting

| Gejala | Penyebab & solusi |
|---|---|
| Sprite tampak pink/magenta | Material belum `Sprite-Lit-Default` → jalankan menu **1**, lalu menu **2** |
| Peta terang tanpa efek lentera | URP asset belum aktif → menu **1** sudah mengeset `GraphicsSettings`/`QualitySettings`; pastikan paket URP terpasang |
| `Input.GetAxisRaw` error / karakter diam | `Project Settings → Player → Active Input Handling` harus **Both** atau **Input Manager (Old)** |
| Dialog tidak muncul | `GameManager` di `_Managers` belum punya referensi `uiManager` → jalankan menu **2** ulang |
| Animasi diam | `Animation/Bahula.controller` belum ada → menu **1** |
| Build gagal karena lisensi | Buka Unity Editor sekali (login lisensi), lalu build dari menu |

---

## 8. Kredit Aset

- **Ninja Adventure Asset Pack** — Pixel-Boy & AAA, **CC0 1.0** (sprite karakter, monster, item, tileset, UI, font, SFX). Lisensi lengkap: `Assets/_Project/LICENSE_NinjaAdventure_CC0.txt`.
- **BGM Gamelan Gender Wayang** — rekaman *Gendér Wayang* (1928), **Public Domain**, Wikimedia Commons; rincian di `Assets/_Project/Audio/BGM/LICENSE_BGM.md`.
- **Karakter Bahula** — restyle CC0 dari sprite Monk (baju putih + udeng coklat + sabuk emas) via `tools/assets/restyle_bahula_balinese.py`; catatan di `Assets/_Project/Art/Characters/LICENSE_Bahula_Restyle.md`.
- **Universal Render Pipeline 2D Lights** — Unity Technologies (Unity Companion License).

---

## 9. Dokumentasi Visual & Uji Otomatis

Screenshot hasil render nyata (play mode) tersimpan di `Game/Docs/`:

| File | Isi |
|---|---|
| `preview_menu.png` | Layar Main Menu "LENTERA DIRAH" + gapura, beringin, penjor di latar |
| `preview_howto.png` | Panel **CARA BERMAIN** (tujuan, kontrol, energi, musuh, tips) |
| `preview_dialog.png` | Dialog Mpu Bharada dengan potret + naskah GDD |
| `preview_gameplay.png` | HUD gameplay: 3 nyawa, bar energi 98%, counter Lontar, radius lentera di kegelapan |
| `preview_world.png` | Peta Desa Girah: 2 gapura, pura meru, bale kulkul, beringin, pelinggih, penjor |
| `preview_difficulty.png` | Halaman **PILIH KESULITAN** (Mudah/Normal/Sulit + pengali skor) |
| `preview_level2.png` | Gameplay **Level 2 — Hutan Bambu Lemah Tulis** |
| `preview_level2_world.png` | Peta Hutan Bambu Lemah Tulis (lorong + clearing) |
| `preview_level3.png` | Gameplay **Level 3 — Pelataran Setra Gandamayu** |
| `preview_level3_world.png` | Peta Pelataran Setra Gandamayu (plaza, pura, pelinggih) |
| `preview_settings.png` | Panel **PENGATURAN**: slider BGM/SFX, layar penuh |
| `preview_credits.png` | Layar **KREDIT**: atribusi aset dan lisensi |
| `preview_pause.png` | Panel **JEDA** di atas gameplay |
| `preview_victory.png` | Hasil level: skor level/total, gelar, tombol level berikutnya |
| `preview_victory3.png` | Hasil akhir setelah level 3: rekor skor, tombol SELESAI |
| `preview_gameover.png` | Game Over: skor total, COBA LAGI / MENU UTAMA |

### Unsur Budaya Bali di Dunia

| Objek | Lokasi | Peran |
|---|---|---|
| **Gapura Candi Bentar (keluar)** | spawn selatan `(21.5, 9)` | pengganti portal keluar desa, tiang solid dan tengah bisa dilewati |
| **Gapura Candi Bentar (utara)** | `(21.5, 24.2)` | penanda gerbang sektor utara |
| **Pohon Beringin** | 4 sudut alun-alun + 3 sektor | naungan & penanda ruang, collider hanya di batang |
| **Pura Meru** | sektor barat & timur | bangunan suci bertingkat, collider di dasar |
| **Bale Kulkul** | alun-alun & sektor utara | menara kentongan |
| **Pelinggih** | 4 sudut alun-alun | altar kecil |
| **Penjor** | tepi alun-alun | dekorasi bambu berhias, tanpa collider |

Uji otomatis (play mode, 74 assertion) dapat dijalankan ulang dengan:

```bash
"/Applications/Unity/Hub/Editor/6000.6.9f1/Unity.app/Contents/MacOS/Unity" \
  -batchmode -projectPath "$(pwd)/Game" \
  -executeMethod LenteraDirah.Editor.PlayModeSmokeTest.Run \
  -logFile -
```

Hasil terakhir: **74/74 PASS** (alur menu → kesulitan → 3 level → hasil, FSM + Paused, light decay 2%, radius 6.0→1.8, burst 15%, stun 3 dtk, exposure ±30%, 3 Lontar/altar per level, skor & rekor, panel Pengaturan/Kredit/Jeda, Game Over + retry).
