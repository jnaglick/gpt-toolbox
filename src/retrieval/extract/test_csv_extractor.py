import pytest
from .csv_extractor import CsvRowExtractor, CsvFileExtractor

def test_csv_extractor():
    extractor = CsvRowExtractor()
    source = 'h1,h2,h3\na,b,c\nd,e,f'

    results = extractor.extract(source)

    assert len(results) == 2
    assert results[0].document == 'h1: a\nh2: b\nh3: c'
    assert results[0].metadata['rownum'] == 0
    assert results[1].document == 'h1: d\nh2: e\nh3: f'
    assert results[1].metadata['rownum'] == 1

def test_csv_file_extractor(tmp_path):
    d = tmp_path / 'sub'
    d.mkdir()
    p = d / 'hello.csv'
    p.write_text('h1,h2,h3\na,b,c\nd,e,f')
    extractor = CsvFileExtractor()

    results = extractor.extract(str(p))

    assert len(results) == 2
    assert results[0].document == 'h1: a\nh2: b\nh3: c'
    assert results[0].metadata['rownum'] == 0
    assert results[0].metadata['file_name'] == 'hello.csv'
    assert results[0].metadata['file_path'] == str(p)

    assert results[1].document == 'h1: d\nh2: e\nh3: f'
    assert results[1].metadata['rownum'] == 1
    assert results[0].metadata['file_name'] == 'hello.csv'
    assert results[0].metadata['file_path'] == str(p)
