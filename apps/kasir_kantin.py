"""Aplikasi 1: Kasir kantin - menu, keranjang, total belanja."""
from apps.tampilan import tampilkan
from fplib import (clean_text, make_entry, append_entry, remove_entry, search_entries,
                   filter_entries, sort_entries, sum_values, average_values, group_counts, as_number)

MENU = [make_entry(id='M1', nama='Nasi Goreng', kategori='Makanan', harga=15000),
        make_entry(id='M2', nama='Es Teh', kategori='Minuman', harga=5000),
        make_entry(id='M3', nama='bakmie', kategori='Makanan', harga=12000),
        make_entry(id='M4', nama='Nasi Ayam', kategori='Makanan', harga=18000),
        make_entry(id='M5', nama='Es Jeruk', kategori='Minuman', harga=7000)]


def tambah_keranjang(keranjang, kode, jumlah):
    cocok = filter_entries(MENU, lambda m: clean_text(m['id']) == clean_text(kode))
    if not cocok:
        raise ValueError('Kode menu tidak ditemukan.')
    qty = as_number(jumlah, minimum=1)
    if not qty.is_integer():
        raise ValueError('Jumlah harus bilangan bulat.')
    menu = cocok[0]
    return append_entry(keranjang, make_entry(id=f'K{len(keranjang)+1}', nama=menu['nama'],
                         kategori=menu['kategori'], jumlah=int(qty), subtotal=menu['harga'] * int(qty)))


def ringkasan(keranjang):
    return {'total': sum_values(keranjang, 'subtotal'),
            'rata_item': average_values(keranjang, 'subtotal'),
            'kategori': group_counts(keranjang, 'kategori')}


def data_awal():
    keranjang = []
    for kode, jumlah in [('M1', 2), ('M2', 1), ('M3', 1), ('M4', 1), ('M5', 2)]:
        keranjang = tambah_keranjang(keranjang, kode, jumlah)
    return keranjang


def run_demo():
    menu = sort_entries(MENU, 'harga')
    keranjang = data_awal()
    tampilkan('Menu urut harga:', [(m['nama'], m['harga']) for m in menu])
    tampilkan('Cari nasi:', [m['nama'] for m in search_entries(MENU, 'nama', 'nasi')])
    tampilkan('Makanan:', [m['nama'] for m in filter_entries(MENU, lambda m: m['kategori'] == 'Makanan')])
    tampilkan('Keranjang:', keranjang)
    tampilkan('Ringkasan:', ringkasan(keranjang))
    tampilkan('Contoh hapus K2:', remove_entry(keranjang, 'K2'))
    return keranjang


def main(keranjang=None):
    keranjang = data_awal() if keranjang is None else keranjang
    while True:
        print('\n[KASIR]\n1.Menu\n2.Tambah\n3.Keranjang\n4.Hapus\n5.Cari\n0.Keluar')
        pilihan = input('Pilih: ').strip()
        try:
            if pilihan == '1':
                tampilkan('Daftar menu', sort_entries(MENU, 'harga'))
            elif pilihan == '2':
                keranjang = tambah_keranjang(keranjang, input('Kode menu: '), input('Jumlah: '))
                print('Berhasil ditambahkan.')
            elif pilihan == '3':
                tampilkan('Keranjang', keranjang); tampilkan('Ringkasan belanja', ringkasan(keranjang))
            elif pilihan == '4':
                keranjang = remove_entry(keranjang, input('ID keranjang: ').strip().upper())
            elif pilihan == '5':
                tampilkan('Hasil pencarian', search_entries(MENU, 'nama', input('Nama menu: ')))
            elif pilihan == '0': return keranjang
            else: print('Pilihan tidak dikenal.')
        except ValueError as err: print('Kesalahan:', err)


if __name__ == '__main__':
    import sys
    run_demo() if '--demo' in sys.argv else main()
