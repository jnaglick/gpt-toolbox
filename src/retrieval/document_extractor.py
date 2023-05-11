from abc import ABC, abstractmethod
from dataclasses import dataclass
import time
from typing import List

from db import Document, DocumentMetadata

@dataclass
class DocumentExtractorResult:
    document: Document
    metadata: DocumentMetadata

DocumentExtractorResults = List[DocumentExtractorResult]

class AbstractDocumentExtractor(ABC):
    @abstractmethod
    def extract(self, source: str) -> DocumentExtractorResults:
        pass

class DocumentExtractor(AbstractDocumentExtractor):
    def extract(self, source: str) -> DocumentExtractorResults:
        return [
            DocumentExtractorResult(
                document=source,
                metadata={
                    'created_at': int(time.time()),
                }
            )
        ]
