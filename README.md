# Satu Library, Lima Aplikasi - Pemrograman Fungsional

Proyek ini berisi lima aplikasi sederhana yang dijalankan lewat terminal. Kelimanya memakai fungsi dari `fplib.py` untuk mengolah data, mulai dari pencarian sampai menghitung ringkasan. Proyek ini digunakan untuk latihan pemrograman fungsional dengan Python.

1. Kasir Kantin: daftar menu, keranjang, total belanja.
2. Presensi Kelas: input kehadiran, rekap tiap mahasiswa.
3. Perpustakaan Mini: katalog, pinjam/kembali, denda (Rp2.000 per hari).
4. Keuangan Pribadi: catatan pemasukan/pengeluaran, saldo dan kategori.
5. Nilai Mahasiswa: input tugas/UTS/UAS, nilai akhir, peringkat.

Menu dan hasil ditampilkan ke bawah dengan label pada setiap data agar mudah dibaca. Program dimulai dengan 5 data contoh per aplikasi. Kasir juga memiliki 5 menu, presensi memiliki 5 mahasiswa, dan perpustakaan memiliki 5 buku. Perubahan data tetap tersimpan saat kembali ke menu utama dan membuka aplikasi lagi, selama program belum ditutup.

## Struktur proyek

```text
FP_Library_5_Aplikasi/
├── fplib.py                 # 11 fungsi reusable
├── jalankan.py              # Menu pemilih aplikasi
├── requirements.txt         # pytest untuk pengujian
├── apps/
│   ├── __init__.py
│   ├── kasir_kantin.py
│   ├── presensi_kelas.py
│   ├── perpustakaan_mini.py
│   ├── keuangan_pribadi.py
│   ├── nilai_mahasiswa.py
│   └── tampilan.py          # Format output dan angka
├── tests/
│   ├── test_fplib.py
│   └── test_aplikasi.py
└── docs/
    ├── matriks_fungsi_aplikasi.md
    └── contoh_output.txt
```

## Persiapan di VS Code (Windows)

Pastikan Python sudah terpasang. Buka folder `FP_Library_5_Aplikasi` di VS Code dan buka terminal. Perintah di bawah dijalankan dari folder yang berisi `jalankan.py`.

Untuk langsung memakai aplikasi, cukup jalankan:

```powershell
python jalankan.py
```

Kalau terminal masih berada di folder luar `FP_Library_5_Aplikasi_SIAP_RUN`, masuk dulu dengan `cd FP_Library_5_Aplikasi`.

Aplikasi tidak memerlukan paket tambahan. Langkah berikut bersifat opsional jika ingin membuat environment terpisah dan memasang kebutuhan pengujian.

Buat environment:

```powershell
py -m venv venv
```

Aktifkan:

```powershell
.\venv\Scripts\activate
```

Jika PowerShell melarang aktivasi, gunakan terminal Command Prompt dan jalankan `venv\Scripts\activate.bat`.

Pasang paket untuk pengujian:

```powershell
python -m pip install -r requirements.txt
```

Pilih menu **1 sampai 5** untuk melihat dan mengubah data masing-masing aplikasi. Di dalam aplikasi, pilih **0** untuk kembali. Pilih **0** di menu utama untuk menutup program. Perubahan data tetap tersedia saat aplikasi dibuka kembali selama program belum ditutup.

## Menjalankan satu per satu

Dari root proyek:

```powershell
python -m apps.kasir_kantin --demo
python -m apps.presensi_kelas --demo
python -m apps.perpustakaan_mini --demo
python -m apps.keuangan_pribadi --demo
python -m apps.nilai_mahasiswa --demo
```

Untuk mode interaktif, hilangkan `--demo`, contohnya `python -m apps.kasir_kantin`.

## Menjalankan pytest

```powershell
python -m pytest -v
```

## Fungsi di library

| Fungsi | Penjelasan |
|---|---|
| `clean_text` | Merapikan teks dan menyeragamkan huruf untuk pencarian |
| `make_entry` | Membuat data baru berbentuk dictionary |
| `append_entry` | Menambah data ke daftar baru |
| `remove_entry` | Menghapus data berdasarkan ID tanpa mengubah daftar asal |
| `search_entries` | Mencari data yang mengandung kata kunci |
| `filter_entries` | Mengambil data sesuai kondisi yang diberikan |
| `sort_entries` | Mengurutkan data berdasarkan kolom tertentu |
| `sum_values` | Menjumlahkan angka pada kolom tertentu |
| `average_values` | Menghitung rata-rata, atau menghasilkan 0 jika data kosong |
| `group_counts` | Menghitung jumlah data dalam tiap kelompok |
| `as_number` | Mengubah input menjadi angka dan memeriksa batas nilainya |

Rincian penggunaan fungsi ada di [matriks fungsi aplikasi](docs/matriks_fungsi_aplikasi.md). Kode pemanggilannya bisa dilihat langsung di masing-masing file dalam folder `apps`.

## Penerapan pemrograman fungsional

Pengolahan data di `fplib.py` dipisahkan dari bagian input dan tampilan. Fungsi penambahan, penghapusan, pencarian, dan pengurutan menghasilkan daftar baru sehingga daftar asal tetap bisa digunakan.

Fungsi `filter_entries()` menerima fungsi kondisi. Misalnya, aplikasi keuangan memakai lambda untuk mengambil transaksi bertipe `keluar`. Hasil penyaringan ini kemudian dipakai bersama fungsi penjumlahan dan rata-rata untuk membuat ringkasan.

## Contoh penggunaan

Untuk mencatat pengeluaran, pilih **4. Keuangan Pribadi**, lalu **1. Catat**. Isi deskripsi, tipe `keluar`, kategori, dan jumlah. Pilih **2. Semua** untuk melihat transaksi atau **3. Rekap** untuk melihat saldo dan ringkasannya.

Masukkan uang tanpa pemisah ribuan, misalnya `70000`. Program akan menampilkannya sebagai `Rp 70.000`. Untuk angka desimal, gunakan titik, misalnya `87.5`.

```text
Data 1
  ID        : F1
  Deskripsi : Makan siang
  Tipe      : keluar
  Kategori  : Makan
  Jumlah    : Rp 25.000
  Nilai     : Rp -25.000
```

Nilai transaksi bertanda negatif untuk pengeluaran dan positif untuk pemasukan. Nilai ini dipakai untuk menghitung saldo.

## Batasan

Data belum disimpan ke file atau database. Saat program ditutup, perubahan hilang. Menjalankan program kembali akan memuat 5 data contoh per aplikasi. Mode `--demo` yang dijalankan secara terpisah tetap memakai data contoh.

Perhitungan yang dipakai dalam aplikasi:

- Denda perpustakaan sebesar **Rp 2.000 per hari terlambat**. Jumlah hari dimasukkan saat mencatat peminjaman.
- Nilai akhir berasal dari **30% tugas, 30% UTS, dan 40% UAS**. Batas kelulusan adalah **60**.
- Persentase kehadiran dihitung dari catatan pertemuan mahasiswa yang sudah dimasukkan.
