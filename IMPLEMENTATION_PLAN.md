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

- [x] `GameManager.cs` — FSM `MainMenu → IntroDialog → Playing → Victory / GameOver`, singleton, event `StateChanged/LontarChanged/HealthChanged/EnergyChanged/HintChanged`, dialog Mpu Bharada verbatim GDD, restart scene
- [x] `AudioManager.cs` — BGM loop + 5 SFX (`Lontar`, `Burst`, `Oil`, `Hurt`, `Victory`)
- [x] `UIManager.cs` — panel Menu/Dialog/HUD/Victory/GameOver, 3 ikon nyawa, bar energi, counter Lontar, baris petunjuk kearifan lokal, tombol interaktif
- [x] User Flow GDD Bab VI terimplementasi (klik **MULAI PENYUCIAN** → dialog → **MENGERTI (E)** / `E` → gameplay)

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
- [x] **Automated play-mode smoke test 19/19 PASS**:
  - [x] 3 musuh, player, GameManager terpasang
  - [x] `MainMenu → IntroDialog → Playing`, HUD aktif, Main Menu non-aktif
  - [x] Light decay terukur **2.40%/1.2 dtk**, radius menyusut **5.99 → 3.79**
  - [x] Minyak Obor mengisi energi ke **100%**
  - [x] Burst memakai **15.0%** energi & menstun musuh
  - [x] Stun berakhir setelah 3 detik → kembali Patrol
  - [x] 3 Lontar terkumpul → segel Altar terbuka → **Victory** + panel tampil
- [x] Review visual: menu, dialog, gameplay (`Game/Docs/preview_menu.png`, `preview_dialog.png`, `preview_gameplay.png`)
- [x] `README_GAMEPLAY.md` — cara menjalankan, checklist rubrik, build, skenario video demo

---

### Catatan penyimpangan kecil dari GDD (disengaja, demi kualitas)

1. **Font UI** memakai font bawaan Unity (`LegacyRuntime.ttf`) karena `NormalFont.ttf` dari paket memiliki metrik glyph yang rusak (spasi hilang & teks terpotong). File font asli tetap tersimpan di `Art/UI/NormalFont.ttf`.
2. **Dialog frame** memakai panel kayu (`FacesetBox`) dan tombol memakai `DialogueBubble`, karena `DialogueBubble` 19×19 bila diregangkan penuh menghasilkan area tengah ungu yang tidak enak dilihat.
3. **Animasi** memakai `Animator.Play()` per state (bukan Blend Tree), agar transisi deterministik dan bebas drift; tetap memakai Animator Controller + clip 4 arah sesuai GDD.
4. **Kamar & koridor** dibuat prosedural (carve rect) agar konektivitas peta dijamin, bukan tilemap manual.
