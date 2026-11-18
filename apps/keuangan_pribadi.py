"""Aplikasi 4: Keuangan pribadi - pemasukan, pengeluaran, kategori."""
from apps.tampilan import tampilkan
from fplib import (clean_text, make_entry, append_entry, remove_entry, search_entries,
                   filter_entries, sort_entries, sum_values, average_values, group_counts, as_number)


def catat(data, deskripsi, tipe, kategori, jumlah):
    if not clean_text(deskripsi) or not clean_text(kategori):
        raise ValueError('Deskripsi dan kategori harus diisi.')
    tipe = clean_text(tipe)
    if tipe not in ('masuk', 'keluar'): raise ValueError('Tipe harus masuk/keluar.')
    uang = as_number(jumlah, 0.01)
    return append_entry(data, make_entry(id=f'F{len(data)+1}', deskripsi=deskripsi.strip(),
                        tipe=tipe, kategori=kategori.strip(), jumlah=uang,
                        nilai=uang if tipe == 'masuk' else -uang))


def ringkasan(data):
    masuk = filter_entries(data, lambda e: e['tipe'] == 'masuk')
    keluar = filter_entries(data, lambda e: e['tipe'] == 'keluar')
    return {'pemasukan': sum_values(masuk, 'jumlah'), 'pengeluaran': sum_values(keluar, 'jumlah'),
            'saldo': sum_values(data, 'nilai'), 'rata_transaksi': average_values(data, 'jumlah'),
            'kategori': group_counts(data, 'kategori')}


def data_awal():
    data = catat([], 'Uang saku', 'masuk', 'Saku', 200000)
    data = catat(data, 'Makan siang', 'keluar', 'Makan', 25000)
    data = catat(data, 'Ongkos kuliah', 'keluar', 'Transportasi', 15000)
    data = catat(data, 'Jasa desain', 'masuk', 'Penghasilan', 100000)
    data = catat(data, 'Beli buku', 'keluar', 'Pendidikan', 45000)
    return data


def run_demo():
    data = data_awal()
    tampilkan('Transaksi tertinggi:', sort_entries(data, 'jumlah', reverse=True))
    tampilkan('Cari makan:', search_entries(data, 'deskripsi', 'makan'))
    tampilkan('Pengeluaran:', filter_entries(data, lambda e: e['tipe'] == 'keluar'))
    tampilkan('Ringkasan:', ringkasan(data))
    tampilkan('Hapus F2:', remove_entry(data, 'F2'))
    return data


def main(data=None):
    data = data_awal() if data is None else data
    while True:
        print('\n[KEUANGAN]\n1.Catat\n2.Semua\n3.Rekap\n4.Cari\n5.Hapus\n0.Keluar')
        pilihan = input('Pilih: ').strip()
        try:
            if pilihan == '1':
                data = catat(data, input('Deskripsi: '), input('Tipe masuk/keluar: '),
                             input('Kategori: '), input('Jumlah: ')); print('Berhasil.')
            elif pilihan == '2': tampilkan('Daftar transaksi', sort_entries(data, 'jumlah', reverse=True))
            elif pilihan == '3': tampilkan('Rekap keuangan', ringkasan(data))
            elif pilihan == '4': tampilkan('Hasil pencarian', search_entries(data, 'deskripsi', input('Cari: ')))
            elif pilihan == '5': data = remove_entry(data, input('ID transaksi: ').strip().upper())
            elif pilihan == '0': return data
            else: print('Pilihan tidak dikenal.')
        except ValueError as err: print('Kesalahan:', err)


if __name__ == '__main__':
    import sys
    run_demo() if '--demo' in sys.argv else main()
