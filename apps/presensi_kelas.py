"""Aplikasi 2: Presensi kelas - input hadir dan rekap per mahasiswa."""
from apps.tampilan import tampilkan
from fplib import (clean_text, make_entry, append_entry, remove_entry, search_entries,
                   filter_entries, sort_entries, sum_values, average_values, group_counts, as_number)

MAHASISWA = [make_entry(id='S1', nama='Alya'), make_entry(id='S2', nama='Bima'),
             make_entry(id='S3', nama='Citra'), make_entry(id='S4', nama='Dimas'),
             make_entry(id='S5', nama='Eka')]


def catat_presensi(data, nim, pertemuan, status):
    if not filter_entries(MAHASISWA, lambda m: clean_text(m['id']) == clean_text(nim)):
        raise ValueError('ID mahasiswa tidak ditemukan.')
    sesi = as_number(pertemuan, 1)
    if not sesi.is_integer(): raise ValueError('Pertemuan harus bulat.')
    status = clean_text(status)
    if status not in {'hadir', 'izin', 'sakit', 'alpa'}:
        raise ValueError('Status harus hadir/izin/sakit/alpa.')
    if filter_entries(data, lambda e: e['mahasiswa'] == nim.upper() and e['pertemuan'] == int(sesi)):
        raise ValueError('Presensi pada pertemuan ini sudah dicatat.')
    return append_entry(data, make_entry(id=f'P{len(data)+1}', mahasiswa=nim.upper(),
                        pertemuan=int(sesi), status=status, hadir=1 if status == 'hadir' else 0))


def rekap(data, nim):
    baris = filter_entries(data, lambda e: e['mahasiswa'] == nim.upper())
    return {'jumlah_pertemuan': len(baris), 'hadir': sum_values(baris, 'hadir'),
            'persentase': average_values(baris, 'hadir') * 100,
            'status': group_counts(baris, 'status')}


def data_awal():
    data = []
    for nim, status in [('S1', 'hadir'), ('S2', 'izin'), ('S3', 'sakit'),
                        ('S4', 'hadir'), ('S5', 'alpa')]:
        data = catat_presensi(data, nim, 1, status)
    return data


def run_demo():
    data = data_awal()
    tampilkan('Mahasiswa:', sort_entries(MAHASISWA, 'nama'))
    tampilkan('Cari Alya:', search_entries(MAHASISWA, 'nama', 'alya'))
    tampilkan('Catatan:', data)
    tampilkan('Rekap S1:', rekap(data, 'S1'))
    tampilkan('Hapus P2:', remove_entry(data, 'P2'))
    return data


def main(data=None):
    data = data_awal() if data is None else data
    while True:
        print('\n[PRESENSI]\n1.Mahasiswa\n2.Catat\n3.Rekap\n4.Hapus\n5.Cari\n0.Keluar')
        pilihan = input('Pilih: ').strip()
        try:
            if pilihan == '1': tampilkan('Daftar mahasiswa', sort_entries(MAHASISWA, 'nama'))
            elif pilihan == '2':
                data = catat_presensi(data, input('ID mahasiswa: ').strip().upper(),
                                      input('Pertemuan ke: '), input('Status: '))
                print('Presensi tercatat.')
            elif pilihan == '3': tampilkan('Rekap presensi', rekap(data, input('ID mahasiswa: ').strip().upper()))
            elif pilihan == '4': data = remove_entry(data, input('ID catatan: ').strip().upper())
            elif pilihan == '5': tampilkan('Hasil pencarian', search_entries(MAHASISWA, 'nama', input('Nama: ')))
            elif pilihan == '0': return data
            else: print('Pilihan tidak dikenal.')
        except ValueError as err: print('Kesalahan:', err)


if __name__ == '__main__':
    import sys
    run_demo() if '--demo' in sys.argv else main()
