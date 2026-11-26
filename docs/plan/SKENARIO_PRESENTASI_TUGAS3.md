# Skenario Presentasi & Rekaman — Final

**Lentera Dirah: Lontar Mpu Bharada** · Muhammad Sufyan (230030309)
Durasi target: **5–7 menit** (3 menit presentasi + 3–4 menit demo).

---

## 1. Susunan Slide

| # | Judul slide | Isi |
|---|---|---|
| 1 | Lentera Dirah — Finalisasi | Judul, nama, NIM, mata kuliah, ITB STIKOM Bali, 2026 |
| 2 | Masalah & Arah Final | Sesi pendek; fokus pada konten 3 level, alur jelas, dan skor/replay |
| 3 | Alur Permainan | `Main Menu → Pilih Kesulitan → Level 1/2/3 → Hasil → Level Berikutnya/Menu` |
| 4 | Tiga Wilayah | Peta Desa Girah, Hutan Bambu Lemah Tulis, Pelataran Setra Gandamayu (3/4/5 musuh) |
| 5 | Mekanik & Kesulitan | Lentera, burst, Rwa Bhineda Exposure; Mudah/Normal/Sulit + pengali skor |
| 6 | Skor, Gelar, Progres | Rumus skor, gelar, skor total, rekor; tombol level berikutnya |
| 7 | Arsitektur | `LevelManager` + `LevelController`; FSM `DifficultySelect`/`Paused`; reset per level |
| 8 | UI/UX | Halaman kesulitan, HUD level/skor, panel jeda, kredit, game over |
| 9 | Verifikasi | 74/74 assertion PASS; build macOS & Windows; build macOS dijalankan |
| 10 | Demo | Rekaman/live sesuai skenario |
| 11 | Penutup & Roadmap | Android + virtual joystick, level tambahan, save progres bila konten bertambah |

Screenshot siap pakai di `Game/Docs/`:
`preview_menu.png`, `preview_difficulty.png`, `preview_settings.png`, `preview_credits.png`,
`preview_world.png`, `preview_level2_world.png`, `preview_level3_world.png`,
`preview_gameplay.png`, `preview_pause.png`, `preview_victory.png`, `preview_victory3.png`, `preview_gameover.png`.

---

## 2. Naskah Narasi

### Slide 1 — Pembuka (10 dtk)
> “Selamat pagi. Saya Muhammad Sufyan, NIM 230030309. Presentasi ini membahas finalisasi **Lentera Dirah: Lontar Mpu Bharada**, game 2D top-down bertema budaya Bali.”

### Slide 2 — Masalah & Arah (25 dtk)
> “Pada versi sebelumnya, permainan selesai dalam satu misi singkat. Karena itu, pengembangan final berfokus pada tiga hal: menambah dua peta baru sehingga total menjadi tiga level, memperjelas alur menu, dan memberi skor serta alasan untuk mengulang.”

### Slide 3 — Alur (25 dtk)
> “Alurnya sekarang linier. Pemain menekan **Mulai Bermain**, memilih kesulitan di halaman terpisah, membaca dialog Mpu Bharada, lalu memainkan level satu sampai tiga. Setiap level menghasilkan halaman hasil berisi skor. Pemain dapat lanjut ke level berikutnya atau kembali ke menu utama.”

### Slide 4 — Tiga Wilayah (30 dtk)
> “Level satu adalah Desa Girah dengan tiga musuh. Level dua adalah Hutan Bambu Lemah Tulis, lorong sempit dengan empat musuh. Level tiga adalah Pelataran Setra Gandamayu, plaza dan pura dengan lima musuh. Setiap level punya altar, tiga Lontar, dan tiga Minyak Obor sendiri.”

### Slide 5 — Mekanik & Kesulitan (30 dtk)
> “Mekanik inti tetap: energi lentera menyusut, burst membekukan musuh, dan tingkat keterlihatan memengaruhi deteksi. Kesulitan dipilih sekali di awal, lalu diterapkan ke seluruh level. Mudah memperlambat musuh, Sulit mempercepat dan menaikkan pengali skor.”

### Slide 6 — Skor & Progres (25 dtk)
> “Skor level dihitung dari bonus waktu, nyawa, dan sisa energi, dikali pengali kesulitan. Skor total diakumulasikan. Di level tiga, rekor skor disimpan. Setelah level satu dan dua, tombol utama adalah **Level Berikutnya**; setelah level tiga menjadi **Selesai**.”

### Slide 7 — Arsitektur (25 dtk)
> “Secara teknis, ketiga level berada dalam satu scene. `LevelManager` mengaktifkan satu `LevelController` dan menonaktifkan yang lain. Saat level dimuat, posisi pemain, energi, nyawa, musuh, item, dan altar direset. FSM game kini punya state `DifficultySelect` dan `Paused`.”

### Slide 8 — UI/UX (20 dtk)
> “HUD menampilkan level, skor, waktu, dan status cahaya. Halaman kesulitan memakai tiga pilihan dengan deskripsi. Panel jeda, pengaturan, kredit, dan game over mengikuti bahasa visual yang sama.”

### Slide 9 — Verifikasi (20 dtk)
> “Uji otomatis play-mode mencakup tujuh puluh empat assertion dan semuanya lulus, termasuk perpindahan tiga level, reset, skor, dan kembali ke menu. Build macOS dan Windows berhasil; build macOS sudah dijalankan.”

### Slide 10 — Demo (3–4 mnt)
Ikuti tabel demo.

### Slide 11 — Penutup (15 dtk)
> “Pengembangan berikutnya adalah ekspor Android dengan virtual joystick, penambahan level, dan save progres setelah jumlah konten bertambah. Terima kasih.”

---

## 3. Skenario Demo (rekam build, 1920×1080)

| Waktu | Aksi | Yang ditekankan |
|---|---|---|
| 0:00–0:08 | Main Menu | Tombol Mulai, Cara Bermain, Pengaturan, Kredit, Keluar |
| 0:08–0:18 | **MULAI BERMAIN** → halaman **PILIH KESULITAN** → **NORMAL** | Alur baru |
| 0:18–0:28 | Dialog Mpu Bharada → **MENGERTI (E)** | Narasi |
| 0:28–0:55 | **Level 1 — Desa Girah**: jelajah, status TERANG, `SPACE` stun, ambil Minyak + Lontar | Mekanik |
| 0:55–1:10 | Ambil Lontar sisanya → Altar → **hasil level 1** → **LEVEL BERIKUTNYA** | Skor & progres |
| 1:10–1:40 | **Level 2 — Hutan Bambu Lemah Tulis**: lorong sempit, 4 musuh, 3 Lontar → Altar → hasil | Peta baru 1 |
| 1:40–2:10 | **Level 3 — Pelataran Setra Gandamayu**: plaza & pura, 5 musuh, 3 Lontar → Altar | Peta baru 2 |
| 2:10–2:25 | **Hasil akhir**: skor total, rekor, tombol **SELESAI** → Menu | Klimaks |
| 2:25–2:40 | (Opsional) `ESC` → **JEDA** → **PENGATURAN** → kembali | UI |
| 2:40–2:55 | (Opsional) **Game Over** → **COBA LAGI** → kembali ke level saat ini | Fail state |
| 2:55–3:10 | (Opsional) **KREDIT** | Lisensi |

Tips:
- Rekam dari build (`Game/Builds/macOS/LenteraDirah.app`), bukan Editor.
- `Cmd+Shift+5` → *Record Selected Portion*; aktifkan audio sistem.
- Jangan memotong transisi level; justru itu yang menunjukkan progres.
- Pastikan cursor tidak menutupi HUD.

---

## 4. Checklist Pengumpulan

- [ ] GDD final: `docs/gdd/…GDD….pdf` (+ DOCX)
- [ ] Build: `Game/Builds/macOS/LenteraDirah.app` dan folder `Game/Builds/Windows/`
- [ ] Source code: folder `Game/` tanpa `Library/`, `Temp/`, `Logs/`
- [ ] Video presentasi + demo (MP4, 5–7 menit)
- [ ] Unggah ke Google Drive, set *Anyone with the link can view*, submit tautan di e-learning
- [ ] Batas waktu: **20 November 2026, 13:00**

---

## 5. Catatan Teknis untuk Q&A

- **Kenapa satu scene untuk tiga level?** Level root diaktifkan/nonaktifkan oleh `LevelManager`; tidak ada loading screen, dan state UI/audio tetap. Reset dilakukan per `LevelController`.
- **Bagaimana item bisa muncul lagi saat retry?** `CollectibleItem` tidak di-`Destroy`, tetapi di-`SetActive(false)`; `ResetItem()` mengaktifkan dan mengembalikan posisi.
- **Apakah skor level 1–2 memengaruhi rekor?** Rekor hanya disimpan setelah level 3 selesai, memakai skor total.
- **Apakah kesulitan bisa diubah di tengah permainan?** Tidak; halaman kesulitan hanya muncul dari menu utama.
- **Apakah nyawa/energi dibawa antar level?** Tidak; tiap level dimulai penuh agar tiap peta dapat dinilai secara adil.
