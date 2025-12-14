# GoSic — Go Music Player
Aplikasi Pemutar Musik Berbasis Struktur Data

---

## Deskripsi Proyek
GoSic (Go Music) adalah aplikasi pemutar musik berbasis GUI yang dikembangkan menggunakan Python dan PyQt6 dengan menerapkan berbagai **struktur data linear**.  
Aplikasi ini dibuat sebagai **Tugas Besar Struktur Data** dan bertujuan untuk mengimplementasikan konsep struktur data seperti Linked List, Stack, Queue, dan Multi Linked List dalam kasus nyata pemutaran musik.

Aplikasi memiliki dua peran pengguna:
- **Admin** → mengelola data musik
- **User** → memutar musik dan mengelola playlist pribadi

---

## Fitur Aplikasi

### Fitur Admin
- Login Admin
- Menampilkan daftar musik (SLL)
- Add Music (judul, artis, genre, vibes, file music, cover)
- Edit Music
- Delete Music
- Logout Admin

---

### Fitur User
- Login User
- Home (daftar semua musik)
- Search Music (judul, artis, genre, vibes)
- Music Player (Play, Pause, Next, Prev berdasarkan vibes)
- Playlist:
  - Create Playlist
  - Tambah Lagu ke Playlist (multi select)
  - Delete Lagu dari Playlist
  - Play Playlist
- Queue (FIFO)
- Favorites
- History Pemutaran
- Logout User

---

## Struktur Data yang Digunakan

| Struktur Data | Fungsi |
|--------------|-------|
| Record (Song) | Menyimpan data musik |
| Single Linked List (SLL) | Katalog musik & search |
| Double Linked List (DLL) | Playlist & navigasi musik |
| Queue | Antrian pemutaran musik |
| Stack | History pemutaran |
| Multi Linked List (MLL) | Navigasi musik berdasarkan vibes |

---

## Teknologi yang Digunakan
- Python 3.12
- PyQt6
- Qt Multimedia (QMediaPlayer)
- FFmpeg
- OOP (Object Oriented Programming)

---

## Cara Menjalankan Program

1. Pastikan Python sudah terinstall
2. Install dependency:
   ```bash
   pip install PyQt6
3. Pastikan folder project lengkap (assets, gui, controllers, structures, dll)

4. Jalankan program dengan perintah:
   ```bash
   python main.py

---

## Akun Login

### Admin
- **Username:** admin  
- **Password:** admin123  

### User
- **Username:** feysha123  
- **Password:** feysha123 
---
- **Username:** faza123  
- **Password:** faza123
---
- **Username:** hafshah123  
- **Password:** hafshah123
---
- **Username:** vincent123  
- **Password:** vincent123 

---

## Anggota Kelompok

- **HAFSHAH** — 103102400014  
- **VINCENT BERWYN C** — 103102400017  
- **FEYSHA KAMILA PRACILYA** — 103102400054  
- **FAZA NUR AULIA SURAYA** — 103102400066  
