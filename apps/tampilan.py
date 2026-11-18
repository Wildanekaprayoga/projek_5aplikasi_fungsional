"""Format output aplikasi tanpa dependensi tambahan."""


UANG = {'harga', 'subtotal', 'total', 'rata_item', 'denda', 'total_denda',
        'rata_denda', 'jumlah', 'nilai', 'pemasukan', 'pengeluaran',
        'saldo', 'rata_transaksi'}


def label(kunci):
    return {'id': 'ID', 'uts': 'UTS', 'uas': 'UAS'}.get(kunci, kunci.replace('_', ' ').capitalize())


def format_nilai(nilai, kunci=''):
    if isinstance(nilai, (int, float)):
        angka = f'{nilai:,.2f}'.rstrip('0').rstrip('.')
        angka = angka.replace(',', '_').replace('.', ',').replace('_', '.')
        if kunci in UANG:
            return f'Rp {angka}'
        return angka + ('%' if kunci == 'persentase' else '')
    return str(nilai)


def ringkasan(data, indent='  '):
    lebar = max((len(label(k)) for k in data), default=0)
    for kunci, nilai in data.items():
        if isinstance(nilai, dict):
            print(f'{indent}{label(kunci)}:')
            ringkasan(nilai, indent + '  ')
        else:
            print(f'{indent}{label(kunci):<{lebar}} : {format_nilai(nilai, '' if kunci == 'jumlah' and 'subtotal' in data else kunci)}')


def tampilkan(judul, data):
    print(f'\n  {judul.rstrip(":")}')
    print('  ' + '-' * len(judul.rstrip(':')))
    if isinstance(data, dict):
        ringkasan(data)
        return
    if not data:
        print('  Tidak ada data.')
        return
    if isinstance(data[0], tuple):
        kolom = ('peringkat', 'nama', 'akhir') if len(data[0]) == 3 else ('nama', 'harga')
        data = [dict(zip(kolom, baris)) for baris in data]
    elif not isinstance(data[0], dict):
        for nilai in data:
            print(f'  - {nilai}')
        return
    for nomor, entri in enumerate(data, 1):
        print(f'  Data {nomor}')
        ringkasan(entri, '    ')
        if nomor < len(data):
            print()
