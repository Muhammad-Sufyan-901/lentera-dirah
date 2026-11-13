# Lisensi & Catatan — Restyle Bahula

**Berkas:** `Bahula_SpriteSheet.png`, `Bahula_IdleSheet.png`, `Bahula_Faceset.png`

Sprite asli berasal dari **Ninja Adventure Asset Pack** oleh Pixel-Boy & AAA, lisensi
**CC0 1.0** (`Assets/_Project/LICENSE_NinjaAdventure_CC0.txt`).

Modifikasi pada branch `feature/gamelan-bgm-balinese-character`:

- Jubah oranye → pakaian/kamen **putih** (`#F4EFE6` dengan shading `#D8D1C2`)
- Rambut/ikat kepala → **udeng coklat** (`#6B4A2F`, highlight `#8A6238`, shadow `#4A3018`) + garis lipatan
- Ikat pinggang hijau → **sabuk emas** (`#FFB84D` / `#B87A22`)
- Kumis/jenggot → dihaluskan agar wajah tampak muda (sesuai tokoh Bahula)
- Kulit, mata, dan outline dipertahankan

Proses recolor dilakukan oleh skrip reproducible `Game/Tools/restyle_bahula_balinese.py`
menggunakan sprite asli yang disimpan di `Game/Tools/source/` (di luar `Assets/`).

Karena asal sprite adalah CC0, hasil modifikasi ini juga dilepas **CC0 1.0**.
