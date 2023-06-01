from abc import ABC, abstractmethod
from typing import List

from tqdm.notebook import tqdm

from db import AbstractDocumentDatabase
from .extract import AbstractDocumentExtractor, DocumentExtractor, DocumentExtractorResult

class AbstractDocumentRetriever(ABC):
    # TODO abstract db and extractor props

    @abstractmethod
    def load(self, source: str) -> None:
        pass

class DocumentRetriever(AbstractDocumentRetriever):
    def __init__(self, document_database: AbstractDocumentDatabase, extractor: AbstractDocumentExtractor = None):
        if extractor is None:
            extractor = DocumentExtractor()

        self.db = document_database
        self.extractor = extractor

        self.query = self.db.query

    def index(self, items: List[DocumentExtractorResult]):
        for item in tqdm(items, desc="Adding documents to store"):
            self.db.add_document(item.document, item.metadata)
        self.db.client.persist() # TODO necessary?
        return items

    def load(self, source: str):
        items = self.extractor.extract(source)
        self.index(items)
        return items
