import pytest
from apps import kasir_kantin, presensi_kelas, perpustakaan_mini, keuangan_pribadi, nilai_mahasiswa


def test_kasir_total():
    keranjang = kasir_kantin.tambah_keranjang([], 'M1', 2)
    keranjang = kasir_kantin.tambah_keranjang(keranjang, 'M2', 1)
    assert kasir_kantin.ringkasan(keranjang)['total'] == 35000
    with pytest.raises(ValueError): kasir_kantin.tambah_keranjang([], 'M9', 1)


def test_presensi():
    data = presensi_kelas.catat_presensi([], 'S1', 1, 'hadir')
    data = presensi_kelas.catat_presensi(data, 'S1', 2, 'izin')
    assert presensi_kelas.rekap(data, 'S1')['persentase'] == 50
    with pytest.raises(ValueError): presensi_kelas.catat_presensi(data, 'S1', 1, 'hadir')


def test_perpustakaan():
    data = perpustakaan_mini.pinjam([], 'B1', 'Alya', 3)
    assert perpustakaan_mini.ringkasan(data)['total_denda'] == 6000
    with pytest.raises(ValueError): perpustakaan_mini.pinjam(data, 'B1', 'Bima')
    assert perpustakaan_mini.kembali(data, 'T1')[0]['status'] == 'Kembali'


def test_keuangan():
    data = keuangan_pribadi.catat([], 'Uang saku', 'masuk', 'Saku', 200000)
    data = keuangan_pribadi.catat(data, 'Makan', 'keluar', 'Makan', 25000)
    assert keuangan_pribadi.ringkasan(data)['saldo'] == 175000
    with pytest.raises(ValueError): keuangan_pribadi.catat(data, 'X', 'lain', 'Y', 1)


def test_nilai():
    data = nilai_mahasiswa.tambah_nilai([], 'Alya', 90, 85, 88)
    data = nilai_mahasiswa.tambah_nilai(data, 'Bima', 50, 50, 50)
    assert data[0]['akhir'] == 87.7
    assert nilai_mahasiswa.peringkat(data)[0][1] == 'Alya'
    assert nilai_mahasiswa.ringkasan(data)['lulus'] == 1
    with pytest.raises(ValueError): nilai_mahasiswa.tambah_nilai([], 'Alya', 101, 50, 80)
