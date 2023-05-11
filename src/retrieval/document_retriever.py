from abc import ABC, abstractmethod

from tqdm.notebook import tqdm

from db import AbstractDocumentDatabase

from .document_extractor import AbstractDocumentExtractor, DocumentExtractor

class AbstractDocumentRetriever(ABC):
    @abstractmethod
    def index(self, source: str) -> None:
        pass

class DocumentRetriever(AbstractDocumentRetriever):
    def __init__(self, document_database: AbstractDocumentDatabase, extractor: AbstractDocumentExtractor = DocumentExtractor()):
        self.db = document_database
        self.query = self.db.query
        self.extractor = extractor

    def index(self, source: str):
        items = self.extractor.extract(source)
        for item in tqdm(items, desc="Adding documents to store"):
            self.db.add_document(item.document, item.metadata)
