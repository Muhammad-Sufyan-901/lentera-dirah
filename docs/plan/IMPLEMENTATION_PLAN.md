# IMPLEMENTATION PLAN — Lentera Dirah: Lontar Mpu Bharada

Prototipe 2D Top-Down (Unity **6000.6.9f1**, URP **17.6**, 2D Lights).
Seluruh kode sumber & executable berada di folder `Game/`.

Legenda: `[x]` selesai & terverifikasi · `[~]` sebagian · `[ ]` belum.

---

## Fase 1 — Struktur Folder & Akuisisi Aset Open-Source

- [x] Proyek Unity URP 2D dibuat dari template resmi (`com.unity.template.2d-cross-platform-2d-7.0.0`) di `Game/`
- [x] `ProjectSettings`: product "Lentera Dirah", 1920×1080, Active Input Handling = **Both** (legacy `GetAxisRaw` + Input System), resizable window
- [x] Struktur folder GDD Bab VIII: `Assets/_Project/{Art/{Characters,Monsters,Items,Tilesets,UI,Animations,Materials},Audio/{BGM,SFX},Prefabs,Scenes,Scripts/{Managers,Player,Enemies,Interactables,Editor}}`
- [x] **Ninja Adventure Asset Pack (CC0 1.0)** diunduh via CLI dari mirror resmi (archive.org, 30 MB)
- [x] Pemetaan aset sesuai GDD:
  - [x] Bahula: `Monk/SeparateAnim/Walk.png` (4×4 walk cycle) + `Faceset.png`
  - [x] Mpu Bharada: `OldMan/Faceset.png`
  - [x] Bayangan Wabah: `Monsters/Spirit/Spirit.png` (4×4)
  - [x] Lontar: `Items/Scroll/ScrollEmpty.png` + `ScrollThunder.png`
  - [x] Minyak Obor: `Items/Potion/MilkPot.png`
  - [x] Tileset: `TilesetFloor.png`, `TilesetNature.png`, `TilesetElement.png`
  - [x] UI: `HUD/Heart.png`, `NinePathRect/DialogueBubble.png`, `FacesetBox.png`, `Font/NormalFont.ttf`
  - [x] SFX: `Secret1`, `Magic1`, `PowerUp1`, `Hit1`, `Success1` → nama sesuai GDD
  - [x] BGM: `Musics/2 - The Cave.ogg` → `bgm_gender_girah.ogg`
- [x] Lisensi aset disimpan di `Assets/_Project/LICENSE_NinjaAdventure_CC0.txt`
- [x] *(N/A)* Fallback generator PNG/WAV tidak dipakai — semua unduhan berhasil

## Fase 2 — Core System & State Management

- [x] `GameManager.cs` — FSM `MainMenu → IntroDialog → Playing ⇄ Paused → Victory / GameOver`, singleton, event `StateChanged/LontarChanged/HealthChanged/EnergyChanged/HintChanged`, dialog Mpu Bharada verbatim GDD, timer, gelar, rekor waktu, restart scene
- [x] `AudioManager.cs` — BGM loop + 5 SFX (`Lontar`, `Burst`, `Oil`, `Hurt`, `Victory`) + volume BGM/SFX tersimpan (`PlayerPrefs`)
- [x] `UIManager.cs` — panel Menu/Dialog/HUD/Jeda/Victory/GameOver/Pengaturan/Kredit, 3 ikon nyawa, bar energi, counter Lontar, timer, status cahaya, tombol interaktif
- [x] User Flow GDD Bab VI terimplementasi (**MULAI BERMAIN** → pilih kesulitan → dialog → gameplay); revisi tiga level pada Fase 8

## Fase 3 — Karakter Pemain & Mekanik Lentera

- [x] `PlayerController.cs` — input 4 arah `GetAxisRaw` + normalisasi diagonal, `Rigidbody2D.linearVelocity`, FSM `Idle/Walking/CastingLight/Hurt`
- [x] Light Decay **2%/detik** → radius `Light 2D` **6.0 → 1.8**, intensitas 1.4, warna `#FFB84D`
- [x] Holy Light Burst (`Space`): biaya **15%**, cooldown **4 dtk**, `Physics2D.OverlapCircleAll` radius **3.5**, stun **3 dtk**, flash cahaya 0.3 dtk
- [x] Nyawa 3, invulnerability 1 dtk, kedip merah saat `Hurt`
- [x] `CameraFollow2D.cs` — smooth follow + clamp batas peta

## Fase 4 — AI Musuh & Objek Budaya Interaktif

- [x] `EnemyShadowAI.cs` — FSM `Patrol 2.2 → Chase 3.4 → Stunned 3.0`, deteksi 4.0, lepas 5.5
- [x] Tint `#6B2D5C` → `#64C8FF` transparan saat stun + aura Light 2D
- [x] Kontak musuh mengurangi nyawa (solid + trigger collider), tidak melukai saat Stunned
- [x] `CollectibleItem.cs` — Lontar & Minyak Obor (+35%), animasi `Mathf.Sin`, glow pulse, SFX, `Destroy`
- [x] `AltarPurification.cs` — segel terbuka saat 3 Lontar, cahaya emas, trigger `Victory`

## Fase 5 — Automasi Perakitan Scene

- [x] `Tools → Lentera Dirah → 1. Configure Pixel Art Assets & Tags` — tag `Player/Enemy/Obstacle`, layer 8/9/10, semua tekstur PPU **16** / Filter **Point** / Compression **None**, slicing grid 16×16, border nine-slice UI, material `Sprite-Lit-Default`, animasi 4 arah (`Walk_*`, `Idle_*`, `Float`) + Animator Controller
- [x] `Tools → Lentera Dirah → 2. Build Complete Prototype Scene` — Global Light 2D `#121324` @0.08, Tilemap Ground (4 varian) + Walls (collider), Player + Point Light 2D, 3 Enemy + waypoint, 3 Lontar, 3 Minyak, Altar, Camera, Canvas HUD/Dialog/Menu/Victory/GameOver, prefab, binding seluruh `[SerializeField]` otomatis
- [x] `Tools → Lentera Dirah → 3. Build macOS App` (+ build CLI batchmode)
- [x] `Tools → Lentera Dirah → Run Full Setup (1 then 2)`
- [x] `Tools → Lentera Dirah → Capture Preview Screenshot` (preview play-mode ke `Game/Docs/`)

## Fase 6 — Verifikasi & Playtesting

- [x] Kompilasi bersih — **0 `error CS`** (batchmode)
- [x] Scene `Assets/_Project/Scenes/LenteraDirah_Girah.unity` dibuat & masuk **Build Settings**
- [x] Build macOS berhasil: `Game/Builds/macOS/LenteraDirah.app`
- [x] **Automated play-mode smoke test (Tugas 2) 19/19 PASS**:
  - [x] 3 musuh, player, GameManager terpasang
  - [x] `MainMenu → IntroDialog → Playing`, HUD aktif, Main Menu non-aktif
  - [x] Light decay terukur **2.40%/1.2 dtk**, radius menyusut **5.99 → 3.79**
  - [x] Minyak Obor mengisi energi ke **100%**
  - [x] Burst memakai **15.0%** energi & menstun musuh
  - [x] Stun berakhir setelah 3 detik → kembali Patrol
  - [x] 3 Lontar terkumpul → segel Altar terbuka → **Victory** + panel tampil
- [x] Review visual: menu, dialog, gameplay (`Game/Docs/preview_menu.png`, `preview_dialog.png`, `preview_gameplay.png`)
- [x] `README_GAMEPLAY.md` — cara menjalankan, checklist rubrik, build, skenario video demo

## Fase 7 — Finalisasi Prototipe (Tugas 3)

- [x] **Menu Pengaturan & Jeda** — slider BGM/SFX (persisten via `PlayerPrefs`), tombol layar penuh, pilihan kesulitan (dipindah ke halaman khusus pada Fase 8), `ESC` membuka/menutup Jeda; panel Jeda berisi Lanjutkan / Pengaturan / Ke Menu Utama
- [x] **Layar Kredit** — atribusi Ninja Adventure (CC0), Gendér Wayang 1928 (Public Domain), aset lingkungan Bali orisinal (CC0), URP 2D Lights
- [x] **Tiga tingkat kesulitan** — Mudah/Normal/Sulit mengubah laju energi (×0.75/×1.00/×1.35), kecepatan musuh (×0.85/×1.00/×1.15), deteksi musuh (×0.80/×1.00/×1.25); diterapkan saat misi dimulai
- [x] **Mekanik 3 — Rwa Bhineda Exposure** — radius deteksi musuh = basis × kesulitan × `Lerp(0.7, 1.3, energi/100)`; HUD menampilkan TERANG/SEIMBANG/REDUP
- [x] **Hasil akhir, gelar, rekor** — timer HUD, panel hasil (waktu/nyawa/energi), gelar Penyuci Agung / Murid Teladan / Pejalan Malam, rekor skor (direvisi menjadi skor total pada Fase 8)
- [x] **Save progres tidak diimplementasikan** — sesi permainan ±2 menit; persistensi dibatasi pada pengaturan, kesulitan, dan rekor
- [x] **Uji otomatis diperluas — 40/40 PASS** (panel baru, Paused/timeScale, wiring Pengaturan dari Jeda, volume BGM, exposure ±30%, penerapan kesulitan, gelar & rekor)
- [x] **Build ulang** — `Game/Builds/macOS/LenteraDirah.app` dan `Game/Builds/Windows/LenteraDirah.exe`; build macOS dijalankan dan berjalan normal
- [x] **Screenshot baru** — `preview_settings.png`, `preview_credits.png`, `preview_pause.png`, `preview_victory.png`
- [x] **Dokumen final** — GDD HTML/DOCX/PDF, README, README_GAMEPLAY, skenario presentasi

---

## Fase 8 — Tiga Level, Halaman Kesulitan, & Skor (revisi final)

- [x] **Tiga level dalam satu scene** — `Level_1_DesaGirahBagianLuar`, `Level_2_HutanBambuLemahTulis`, `Level_3_PelataranSetraGandamayu`; hanya satu root aktif, level lain diaktifkan oleh `LevelManager`
- [x] **Dua peta baru** — layout prosedural Hutan Bambu (14 rect) dan Pelataran Setra (16 rect), tema props berbeda (hutan vs pura/setra), warna tanah berbeda
- [x] **Kesulitan per level** — 3 / 4 / 5 musuh, 3 Lontar + 3 Minyak + altar per level, skor terakumulasi
- [x] **Halaman Pilih Kesulitan** — `MAIN MENU → MULAI BERMAIN → DifficultySelect`; pilihan Mudah/Normal/Sulit + pengali skor; dihapus dari panel Pengaturan
- [x] **Alur hasil level** — `Victory` menampilkan skor level, skor total, gelar, dan tombol **LEVEL BERIKUTNYA**; level 3 menjadi **SELESAI**
- [x] **Game Over** — menampilkan skor total, **COBA LAGI** (mengulang level saat ini), **MENU UTAMA**
- [x] **Reset per level** — player (energi/nyawa/posisi), musuh (state/posisi), item (diaktifkan ulang), altar (tersegel lagi), kamera snap
- [x] **HUD** — `LEVEL n/3 — Nama`, `SKOR`, timer, status cahaya
- [x] **Uji otomatis 74/74 PASS** — alur menu→kesulitan→3 level→hasil, skor, reset, pindah level, game over/retry, rekor
- [x] **Screenshot baru** — `preview_difficulty.png`, `preview_level2.png`, `preview_level2_world.png`, `preview_level3.png`, `preview_level3_world.png`, `preview_gameover.png`, `preview_victory3.png`
- [x] **Build ulang** — macOS `.app` dan Windows `.exe`; build macOS dijalankan
- [x] **Dokumen** — GDD HTML/DOCX/PDF, README, README_GAMEPLAY, skenario presentasi diperbarui

---

### Catatan penyimpangan kecil dari GDD (disengaja, demi kualitas)

1. **Font UI** memakai font bawaan Unity (`LegacyRuntime.ttf`) karena `NormalFont.ttf` dari paket memiliki metrik glyph yang rusak (spasi hilang & teks terpotong). File font asli tetap tersimpan di `Art/UI/NormalFont.ttf`.
2. **Dialog frame** memakai panel kayu (`FacesetBox`) dan tombol memakai `DialogueBubble`, karena `DialogueBubble` 19×19 bila diregangkan penuh menghasilkan area tengah ungu yang tidak enak dilihat.
3. **Animasi** memakai `Animator.Play()` per state (bukan Blend Tree), agar transisi deterministik dan bebas drift; tetap memakai Animator Controller + clip 4 arah sesuai GDD.
4. **Kamar & koridor** dibuat prosedural (carve rect) agar konektivitas peta dijamin, bukan tilemap manual.
