"""Aplikasi 3: Perpustakaan mini - katalog, peminjaman, denda."""
from apps.tampilan import tampilkan
from fplib import (clean_text, make_entry, append_entry, remove_entry, search_entries,
                   filter_entries, sort_entries, sum_values, average_values, group_counts, as_number)

BUKU = [make_entry(id='B1', judul='Algoritma Python', kategori='Teknologi'),
        make_entry(id='B2', judul='Statistika Dasar', kategori='Sains'),
        make_entry(id='B3', judul='Pemrograman Web', kategori='Teknologi'),
        make_entry(id='B4', judul='Matematika Diskrit', kategori='Sains'),
        make_entry(id='B5', judul='Sejarah Indonesia', kategori='Sejarah')]
DENDA_HARIAN = 2000


def pinjam(data, kode, peminjam, hari_terlambat=0):
    buku = filter_entries(BUKU, lambda e: clean_text(e['id']) == clean_text(kode))
    if not buku: raise ValueError('Kode buku tidak ditemukan.')
    if not clean_text(peminjam): raise ValueError('Peminjam tidak boleh kosong.')
    if filter_entries(data, lambda e: e['kode'] == kode.upper() and e['status'] == 'Dipinjam'):
        raise ValueError('Buku ini sedang dipinjam.')
    hari = as_number(hari_terlambat)
    if not hari.is_integer(): raise ValueError('Hari terlambat harus bulat.')
    return append_entry(data, make_entry(id=f'T{len(data)+1}', kode=kode.upper(),
                        judul=buku[0]['judul'], peminjam=peminjam.strip(),
                        kategori=buku[0]['kategori'], status='Dipinjam', hari=int(hari),
                        denda=int(hari) * DENDA_HARIAN))


def kembali(data, id_transaksi):
    if not filter_entries(data, lambda e: e['id'] == id_transaksi and e['status'] == 'Dipinjam'):
        raise ValueError('Transaksi aktif tidak ditemukan.')
    return [make_entry(**{**e, 'status': 'Kembali'}) if e['id'] == id_transaksi else dict(e) for e in data]


def ringkasan(data):
    return {'total_denda': sum_values(data, 'denda'), 'rata_denda': average_values(data, 'denda'),
            'kategori': group_counts(data, 'kategori')}


def data_awal():
    data = []
    for kode, nama, hari in [('B1', 'Alya', 3), ('B2', 'Bima', 0),
                             ('B3', 'Citra', 1), ('B4', 'Dimas', 0), ('B5', 'Eka', 2)]:
        data = pinjam(data, kode, nama, hari)
    return data


def run_demo():
    data = data_awal()
    tampilkan('Katalog:', sort_entries(BUKU, 'judul'))
    tampilkan('Cari Python:', search_entries(BUKU, 'judul', 'python'))
    tampilkan('Sedang dipinjam:', filter_entries(data, lambda e: e['status'] == 'Dipinjam'))
    tampilkan('Ringkasan:', ringkasan(data))
    tampilkan('Kembali T1:', kembali(data, 'T1'))
    tampilkan('Hapus T2:', remove_entry(data, 'T2'))
    return data


def main(data=None):
    data = data_awal() if data is None else data
    while True:
        print('\n[PERPUSTAKAAN]\n1.Katalog\n2.Pinjam\n3.Kembali\n4.Rekap\n5.Cari\n6.Hapus\n0.Keluar')
        pilihan = input('Pilih: ').strip()
        try:
            if pilihan == '1': tampilkan('Katalog buku', sort_entries(BUKU, 'judul'))
            elif pilihan == '2':
                data = pinjam(data, input('Kode buku: '), input('Peminjam: '), input('Hari terlambat (0 jika belum): '))
                print('Transaksi tercatat.')
            elif pilihan == '3': data = kembali(data, input('ID transaksi: ').strip().upper())
            elif pilihan == '4': tampilkan('Daftar peminjaman', data); tampilkan('Ringkasan', ringkasan(data))
            elif pilihan == '5': tampilkan('Hasil pencarian', search_entries(BUKU, 'judul', input('Cari judul: ')))
            elif pilihan == '6': data = remove_entry(data, input('ID transaksi: ').strip().upper())
            elif pilihan == '0': return data
            else: print('Pilihan tidak dikenal.')
        except ValueError as err: print('Kesalahan:', err)


if __name__ == '__main__':
    import sys
    run_demo() if '--demo' in sys.argv else main()
