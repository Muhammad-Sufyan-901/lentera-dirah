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
`Main Menu` → klik **MULAI PENYUCIAN** → dialog Mpu Bharada → klik **MENGERTI (E)** atau tekan `E`
→ `Gameplay` (jelajah, hindari/stun bayangan, ambil 3 Lontar & Minyak)
→ sentuh **Altar Penyucian** setelah 3 Lontar → `Victory` (Desa Girah Pulih)
atau nyawa habis / energi 0% → `Game Over` → **COBA LAGI**.

Dari Main Menu, tombol **KELUAR** menutup game (di Unity Editor, tombol ini menghentikan Play Mode).

---

## 2. Kontrol

| Aksi | Input |
|---|---|
| Bergerak 4 arah | `W A S D` atau panah |
| Holy Light Burst (stun 3 dtk) | `SPACE` |
| Lanjut dialog | `E` atau klik tombol |
| Keluar dari game | Tombol **KELUAR** di Main Menu |

Parameter (sesuai GDD): kecepatan **4.5**, decay lentera **2%/dtk**, radius cahaya **6.0 → 1.8**, burst **-15%** energi, cooldown **4 dtk**, radius stun **3.5**, nyawa **3**, invulnerability **1 dtk**, patroli **2.2**, kejar **3.4**, deteksi **4.0**, lepas **5.5**.

---

## 3. Checklist Verifikasi Rubrik

| Kriteria | Cara memastikan | Status |
|---|---|---|
| **Input & Movement** | `WASD`/panah menggerakkan Bahula; diagonal tidak lebih cepat (dinormalisasi); animasi jalan 4 arah | ✅ |
| **Solid Collision** | Menabrak dinding/pohon desa (TilemapCollider2D, layer `Obstacle`) tidak menembus | ✅ |
| **Trigger Collision** | Menyentuh Lontar → counter HUD naik + SFX + kutipan; Minyak → energi +35%; Altar → cek 3 Lontar | ✅ |
| **FSM Level 1 (Game)** | `MainMenu → IntroDialog → Playing → Victory/GameOver`; input & AI berhenti di luar `Playing` | ✅ |
| **FSM Level 2 (Player)** | `Idle / Walking / CastingLight (0.3 dtk) / Hurt (1 dtk, kedip merah)` | ✅ |
| **FSM Level 3 (Enemy)** | `Patrol → Chase` (≤4.0) `→ Stunned` (3 dtk, tint sian transparan, berhenti melukai) | ✅ |
| **Mekanik 1 — Lontar & Segel Altar** | Kumpulkan 3 Lontar (Usada, Dharma, Rwa Bhineda) → segel terbuka (cahaya emas) → Victory | ✅ |
| **Mekanik 2 — Lentera Dinamis & Stun Burst** | Bar energi turun 2%/dtk, radius `Light 2D` menyusut; `SPACE` memotong 15% & menstun musuh radius 3.5 | ✅ |
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

---

## 5. Skenario Rekaman Video Demo (1–2 menit)

| Waktu | Aksi yang direkam |
|---|---|
| 0:00–0:10 | Main Menu: judul **LENTERA DIRAH**, klik **MULAI PENYUCIAN** |
| 0:10–0:25 | Dialog Mpu Bharada muncul (potret + naskah), klik **MENGERTI (E)** |
| 0:25–0:45 | Gameplay: jelajah lorong gelap, tunjukkan bar energi turun & radius cahaya menyusut |
| 0:45–1:00 | Musuh mendekat (tint ungu, state Chase) → tekan `SPACE`: kilatan cahaya, musuh membeku sian (Stunned) |
| 1:00–1:15 | Ambil **Minyak Obor** (energi +35%, radius membesar) lalu ambil **Lontar Suci** (counter 1/3, kutipan muncul) |
| 1:15–1:30 | Ambil 2 Lontar sisanya → segel Altar terbuka (cahaya emas) → sentuh Altar |
| 1:30–1:45 | Layar **Victory** "Desa Girah Pulih" + dialog penutup + klik **MAIN LAGI** |
| 1:45–2:00 | (Opsional) Tunjukkan **Game Over** dengan membiarkan energi habis, lalu **COBA LAGI** |

Tips rekaman: `Cmd+Shift+5` (QuickTime screen recording), resolusi jendela 1920×1080, aktifkan suara sistem agar BGM/SFX terdengar.

---

## 6. Struktur Proyek

```
Game/
├── Assets/_Project/
│   ├── Art/{Characters,Monsters,Items,Tilesets,UI,Animations,Materials}
│   ├── Audio/{BGM,SFX}
│   ├── Prefabs/            (LontarSuci, MinyakObor, AltarPenyucian)
│   ├── Scenes/LenteraDirah_Girah.unity
│   └── Scripts/{Managers,Player,Enemies,Interactables,Editor}
├── Builds/macOS/LenteraDirah.app
├── Packages/  ProjectSettings/
└── README_GAMEPLAY.md
```

## 7. Troubleshooting

| Gejala | Penyebab & solusi |
|---|---|
| Sprite tampak pink/magenta | Material belum `Sprite-Lit-Default` → jalankan menu **1**, lalu menu **2** |
| Peta terang tanpa efek lentera | URP asset belum aktif → menu **1** sudah mengeset `GraphicsSettings`/`QualitySettings`; pastikan paket URP terpasang |
| `Input.GetAxisRaw` error / karakter diam | `Project Settings → Player → Active Input Handling` harus **Both** atau **Input Manager (Old)** |
| Dialog tidak muncul | `GameManager` di `_Managers` belum punya referensi `uiManager` → jalankan menu **2** ulang |
| Animasi diam | `Art/Animations/Bahula.controller` belum ada → menu **1** |
| Build gagal karena lisensi | Buka Unity Editor sekali (login lisensi), lalu build dari menu |

---

## 8. Kredit Aset

- **Ninja Adventure Asset Pack** — Pixel-Boy & AAA, **CC0 1.0** (sprite karakter, monster, item, tileset, UI, font, SFX). Lisensi lengkap: `Assets/_Project/LICENSE_NinjaAdventure_CC0.txt`.
- **BGM Gamelan Gender Wayang** — rekaman *Gendér Wayang* (1928), **Public Domain**, Wikimedia Commons; rincian di `Assets/_Project/Audio/BGM/LICENSE_BGM.md`.
- **Karakter Bahula** — restyle CC0 dari sprite Monk (baju putih + udeng coklat + sabuk emas) via `Game/Tools/restyle_bahula_balinese.py`; catatan di `Assets/_Project/Art/Characters/LICENSE_Bahula_Restyle.md`.
- **Universal Render Pipeline 2D Lights** — Unity Technologies (Unity Companion License).

---

## 9. Dokumentasi Visual & Uji Otomatis

Screenshot hasil render nyata (play mode) tersimpan di `Game/Docs/`:

| File | Isi |
|---|---|
| `preview_menu.png` | Layar Main Menu "LENTERA DIRAH" + gapura, beringin, penjor di latar |
| `preview_dialog.png` | Dialog Mpu Bharada dengan potret + naskah GDD |
| `preview_gameplay.png` | HUD gameplay: 3 nyawa, bar energi 98%, counter Lontar, radius lentera di kegelapan |
| `preview_world.png` | Peta Desa Girah: 2 gapura, pura meru, bale kulkul, beringin, pelinggih, penjor |

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

Uji otomatis (play mode, 19 assertion) dapat dijalankan ulang dengan:

```bash
"/Applications/Unity/Hub/Editor/6000.6.9f1/Unity.app/Contents/MacOS/Unity" \
  -batchmode -projectPath "$(pwd)/Game" \
  -executeMethod LenteraDirah.Editor.PlayModeSmokeTest.Run \
  -logFile -
```

Hasil terakhir: **19/19 PASS** (FSM 3 level, light decay 2%, radius 6.0→1.8, burst 15%, stun 3 dtk, 3 Lontar, segel Altar, Victory).
