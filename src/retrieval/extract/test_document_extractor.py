import pytest
from .document_extractor import DocumentExtractor, SimpleDocumentExtractor, to_documents

def test_to_documents():
    # arrange
    source = "test document"
    metadata = {"author": "test author"}

    # act
    result = to_documents(source, metadata)

    # assert
    assert len(result) == 1
    assert result[0].document == source
    assert result[0].metadata["author"] == metadata["author"]

def test_simple_document_extractor():
    # arrange
    extractor = SimpleDocumentExtractor()
    source = "test document"
    metadata = {"author": "test author"}
    
    # act
    result = extractor.extract(source, metadata)

    # assert
    assert len(result) == 1
    assert result[0].document == source
    assert result[0].metadata["author"] == metadata["author"]

def test_document_extractor():
    # arrange
    extractor = DocumentExtractor()
    source = "test document"
    metadata = {"author": "test author"}

    # act
    result = extractor.extract(source, metadata)

    # assert
    assert len(result) == 1
    assert result[0].document == source
    assert result[0].metadata["author"] == metadata["author"]

class NoopSubDocumentExtractor(DocumentExtractor):
    def condition(self, source, additional_metadata) -> bool:
        return False

    def run_extract(self, source, additional_metadata):
        return to_documents("should not appear")

class SubDocumentExtractor(DocumentExtractor):
    def run_extract(self, source, additional_metadata):
        return to_documents("test", {"test": "test"})

def test_document_extractor_with_sub_extractors():
    # arrange
    extractor = DocumentExtractor([SimpleDocumentExtractor(), SubDocumentExtractor(), NoopSubDocumentExtractor()])
    source = "test document"
    metadata = {"author": "test author"}

    # act
    result = extractor.extract(source, metadata)

    # assert
    assert len(result) == 2
    assert result[0].document == "test document"
    assert result[0].metadata["author"] == metadata["author"]
    assert result[1].document == "test"
    assert result[1].metadata["test"] == "test"