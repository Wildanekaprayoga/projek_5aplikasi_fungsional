"""Kumpulan fungsi murni untuk dipakai ulang di lima aplikasi.

Tidak ada input(), print(), atau mutasi terhadap koleksi yang diterima.
"""
from collections import Counter
from decimal import Decimal, InvalidOperation
from typing import Any, Callable


def clean_text(value: object) -> str:
    """Hilangkan spasi berlebih dan seragamkan kapitalisasi untuk pencarian."""
    return ' '.join(str(value).strip().split()).casefold()


def make_entry(**fields: Any) -> dict[str, Any]:
    """Buat salinan record, tanpa mempertahankan referensi dictionary pemanggil."""
    return dict(fields)


def append_entry(entries: list[dict], entry: dict) -> list[dict]:
    """Kembalikan list baru dengan satu record tambahan."""
    return [*entries, dict(entry)]


def remove_entry(entries: list[dict], identifier: object, key: str = 'id') -> list[dict]:
    """Hapus record dengan identitas cocok tanpa mengubah list asal."""
    return [dict(e) for e in entries if e.get(key) != identifier]


def search_entries(entries: list[dict], key: str, query: str) -> list[dict]:
    """Temukan record yang berisi kata kunci (abaikan besar/kecil huruf)."""
    needle = clean_text(query)
    return [dict(e) for e in entries if needle in clean_text(e.get(key, ''))]


def filter_entries(entries: list[dict], predicate: Callable[[dict], bool]) -> list[dict]:
    """Filter berdasarkan predikat tanpa mengubah list asal."""
    return [dict(e) for e in entries if predicate(e)]


def sort_entries(entries: list[dict], key: str, reverse: bool = False) -> list[dict]:
    """Urutkan data pada field tertentu, tanpa mengubah list asal."""
    return sorted((dict(e) for e in entries), key=lambda e: e.get(key, 0), reverse=reverse)


def sum_values(entries: list[dict], key: str) -> float:
    """Jumlahkan field numerik; field kosong dianggap 0."""
    return float(sum(Decimal(str(e.get(key, 0) or 0)) for e in entries))


def average_values(entries: list[dict], key: str) -> float:
    """Rata-rata field numerik; koleksi kosong menghasilkan 0."""
    return sum_values(entries, key) / len(entries) if entries else 0.0


def group_counts(entries: list[dict], key: str) -> dict[Any, int]:
    """Hitung jumlah record per kategori."""
    return dict(Counter(e.get(key) for e in entries))


def as_number(value: object, minimum: float = 0) -> float:
    """Konversi teks menjadi bilangan dan validasi batas bawah."""
    try:
        result = float(Decimal(str(value).strip()))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError('Masukkan angka yang valid.') from exc
    if not (float('-inf') < result < float('inf')) or result < minimum:
        raise ValueError(f'Angka harus finite dan minimal {minimum}.')
    return result
