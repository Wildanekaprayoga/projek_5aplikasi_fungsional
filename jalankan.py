"""Launcher satu pintu untuk menjalankan 5 aplikasi CLI."""
from apps import kasir_kantin, presensi_kelas, perpustakaan_mini, keuangan_pribadi, nilai_mahasiswa

APLIKASI = {
    '1': ('Kasir Kantin', kasir_kantin),
    '2': ('Presensi Kelas', presensi_kelas),
    '3': ('Perpustakaan Mini', perpustakaan_mini),
    '4': ('Keuangan Pribadi', keuangan_pribadi),
    '5': ('Nilai Mahasiswa', nilai_mahasiswa),
}


def main():
    data_aplikasi = {kode: modul.data_awal() for kode, (_, modul) in APLIKASI.items()}
    while True:
        print('\n=== SATU LIBRARY, LIMA APLIKASI ===')
        for nomor, (nama, _) in APLIKASI.items(): print(f'{nomor}. {nama}')
        print('0. Keluar')
        
        try:
            opsi = input('Pilih aplikasi: ').strip()
        except EOFError:
            break
        if opsi == '0': break
        if opsi in APLIKASI:
            data_aplikasi[opsi] = APLIKASI[opsi][1].main(data_aplikasi[opsi])
        else: print('Pilihan tidak dikenal.')


if __name__ == '__main__':
    main()
