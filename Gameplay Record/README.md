# Gameplay Record — Lentera Dirah

**Berkas:** `Lentera Dirah - Gameplay (Menang & Kalah).mp4`

| Atribut | Nilai |
|---|---|
| Resolusi | 1280 × 720 (16:9) |
| Frame rate | 30 fps |
| Durasi | ± 33 detik |
| Video | H.264 (yuv420p) |
| Audio | AAC 160 kbps — BGM *Gendér Wayang* (1928), Public Domain |
| Ukuran | ± 7 MB |

## Isi rekaman

| Waktu | Adegan |
|---|---|
| 0:00 | Main Menu — tombol MULAI PENYUCIAN, CARA BERMAIN, KELUAR |
| 0:02 | Panel **CARA BERMAIN** dibuka lalu ditutup |
| 0:03 | Dialog pembuka Mpu Bharada |
| 0:05 | Gameplay: berjalan melewati gapura menuju alun-alun, menyentuh Altar yang masih tersegel |
| 0:09 | Sektor utara: mengambil **Lontar Usada** |
| 0:12 | Holy Light Burst membekukan Bayangan Wabah |
| 0:15 | Mengambil **Minyak Obor** (energi +35%) dan **Lontar Dharma** (sektor barat) |
| 0:19 | Mengambil **Lontar Rwa Bhineda** (sektor timur) |
| 0:21 | Altar terbuka, disentuh → layar **Victory** "DESA GIRAH PULIH" |
| 0:24 | Sesi kedua: Bahula terkena Bayangan Wabah (1 nyawa berkurang) |
| 0:29 | Energi lentera habis → layar **Game Over** "KEGELAPAN MENYELIMUTI" |

## Cara rekaman dibuat

Frame dirender langsung dari Unity Play Mode (bukan screen capture) dengan
`Assets/_Project/Scripts/Editor/PlayModeGameplayRecorder.cs`:

```bash
Unity -batchmode -projectPath Game \
  -executeMethod LenteraDirah.Editor.PlayModeGameplayRecorder.RecordWin

Unity -batchmode -projectPath Game \
  -executeMethod LenteraDirah.Editor.PlayModeGameplayRecorder.RecordLose
```

Frame PNG kemudian di-encode dengan ffmpeg (30 fps, H.264) dan diberi BGM.

## Kredit

- BGM: *Gendér Wayang* (1928), Gamelan Gender Wayang Bali — Public Domain
  (`Game/Assets/_Project/Audio/BGM/LICENSE_BGM.md`).
- Aset visual: Ninja Adventure (CC0) + aset lingkungan Bali orisinal (CC0).
