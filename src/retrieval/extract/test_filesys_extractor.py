import pytest
from .filesys_extractor import FileExtractor, DirectoryExtractor

def test_file_extractor(tmp_path):
    # Arrange
    file = tmp_path / "test.txt"
    file.write_text("Hello, World!")
    extractor = FileExtractor()

    # Act
    results = extractor.extract(str(file))

    # Assert
    assert len(results) == 1
    assert results[0].document == "Hello, World!"
    assert results[0].metadata['file_name'] == "test.txt"
    assert results[0].metadata['file_path'] == str(file)

def test_directory_extractor(tmp_path):
    # Arrange
    dir = tmp_path / "sub"
    dir.mkdir()
    file1 = dir / "test1.txt"
    file1.write_text("Hello, World!")
    file2 = dir / "test2.txt"
    file2.write_text("Hello, again!")
    extractor = DirectoryExtractor()

    # Act
    results = extractor.extract(str(dir))

    # Assert
    assert len(results) == 2
    assert any(r.document == "Hello, World!" for r in results)
    assert any(r.document == "Hello, again!" for r in results)

def test_directory_extractor_nested(tmp_path):
    # Arrange
    dir = tmp_path / "sub"
    dir.mkdir()
    sub_dir = dir / "sub_sub"
    sub_dir.mkdir()
    file1 = dir / "test1.txt"
    file1.write_text("Hello, World!")
    file2 = sub_dir / "test2.txt"
    file2.write_text("Hello, again!")
    extractor = DirectoryExtractor()

    # Act
    results = extractor.extract(str(dir))

    # Assert
    assert len(results) == 2
    assert any(r.document == "Hello, World!" for r in results)
    assert any(r.document == "Hello, again!" for r in results)

# TODO Additional tests for FileExtractor with sub-extractors
