import pytest
from fplib import (clean_text, make_entry, append_entry, remove_entry, search_entries,
                   filter_entries, sort_entries, sum_values, average_values, group_counts, as_number)

DATA = [make_entry(id='A', nama='  Nasi Goreng ', kategori='Makan', nilai=10),
        make_entry(id='B', nama='Es Teh', kategori='Minum', nilai=20),
        make_entry(id='C', nama='Nasi Uduk', kategori='Makan', nilai=30)]


def test_clean_text():
    assert clean_text('  NASI   Goreng ') == 'nasi goreng'


def test_make_entry():
    assert make_entry(id=1)['id'] == 1


def test_append_entry_immutable():
    hasil = append_entry(DATA, {'id': 'D'})
    assert len(DATA) == 3 and len(hasil) == 4


def test_remove_entry_immutable():
    hasil = remove_entry(DATA, 'B')
    assert len(hasil) == 2 and len(DATA) == 3


def test_search_entries():
    assert len(search_entries(DATA, 'nama', 'NASI')) == 2


def test_filter_entries():
    assert len(filter_entries(DATA, lambda e: e['nilai'] >= 20)) == 2


def test_sort_entries():
    assert sort_entries(DATA, 'nilai', reverse=True)[0]['id'] == 'C'
    assert DATA[0]['id'] == 'A'


def test_sum_values():
    assert sum_values(DATA, 'nilai') == 60


def test_average_values():
    assert average_values(DATA, 'nilai') == 20
    assert average_values([], 'nilai') == 0


def test_group_counts():
    assert group_counts(DATA, 'kategori') == {'Makan': 2, 'Minum': 1}


def test_as_number_invalid():
    for n in ('abc', -1, 'NaN', 'Infinity'):
        with pytest.raises(ValueError): as_number(n)
    assert as_number('3.5') == 3.5
