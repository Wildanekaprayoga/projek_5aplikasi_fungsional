"""Aplikasi 5: Nilai mahasiswa - komponen nilai, nilai akhir, peringkat."""
from apps.tampilan import tampilkan
from fplib import (clean_text, make_entry, append_entry, remove_entry, search_entries,
                   filter_entries, sort_entries, sum_values, average_values, group_counts, as_number)

BOBOT = {'tugas': .3, 'uts': .3, 'uas': .4}


def tambah_nilai(data, nama, tugas, uts, uas):
    if not clean_text(nama): raise ValueError('Nama mahasiswa wajib diisi.')
    if search_entries(data, 'nama', nama) and any(clean_text(e['nama']) == clean_text(nama) for e in data):
        raise ValueError('Nama sudah tercatat.')
    skor = [as_number(v) for v in (tugas, uts, uas)]
    if any(v > 100 for v in skor): raise ValueError('Nilai maksimum 100.')
    akhir = round(sum(s * w for s, w in zip(skor, BOBOT.values())), 2)
    return append_entry(data, make_entry(id=f'N{len(data)+1}', nama=nama.strip(), tugas=skor[0],
                        uts=skor[1], uas=skor[2], akhir=akhir,
                        predikat='Lulus' if akhir >= 60 else 'Tidak lulus'))


def peringkat(data):
    return [(i, e['nama'], e['akhir']) for i, e in enumerate(sort_entries(data, 'akhir', reverse=True), 1)]


def ringkasan(data):
    return {'total_nilai_akhir': sum_values(data, 'akhir'), 'rata_kelas': average_values(data, 'akhir'),
            'predikat': group_counts(data, 'predikat'),
            'lulus': len(filter_entries(data, lambda e: e['predikat'] == 'Lulus'))}


def data_awal():
    data = tambah_nilai([], 'Alya', 90, 85, 88)
    data = tambah_nilai(data, 'Bima', 70, 75, 65)
    data = tambah_nilai(data, 'Citra', 50, 45, 55)
    data = tambah_nilai(data, 'Dimas', 85, 80, 90)
    data = tambah_nilai(data, 'Eka', 65, 60, 70)
    return data


def run_demo():
    data = data_awal()
    tampilkan('Cari Alya:', search_entries(data, 'nama', 'alya'))
    tampilkan('Peringkat:', peringkat(data))
    tampilkan('Rekap:', ringkasan(data))
    tampilkan('Hapus N3:', remove_entry(data, 'N3'))
    return data


def main(data=None):
    data = data_awal() if data is None else data
    while True:
        print('\n[NILAI]\n1.Input\n2.Peringkat\n3.Rekap\n4.Cari\n5.Hapus\n0.Keluar')
        pilihan = input('Pilih: ').strip()
        try:
            if pilihan == '1':
                data = tambah_nilai(data, input('Nama: '), input('Tugas: '), input('UTS: '), input('UAS: '))
                print('Berhasil.')
            elif pilihan == '2': tampilkan('Peringkat mahasiswa', peringkat(data))
            elif pilihan == '3': tampilkan('Rekap nilai', ringkasan(data))
            elif pilihan == '4': tampilkan('Hasil pencarian', search_entries(data, 'nama', input('Cari nama: ')))
            elif pilihan == '5': data = remove_entry(data, input('ID nilai: ').strip().upper())
            elif pilihan == '0': return data
            else: print('Pilihan tidak dikenal.')
        except ValueError as err: print('Kesalahan:', err)


if __name__ == '__main__':
    import sys
    run_demo() if '--demo' in sys.argv else main()
