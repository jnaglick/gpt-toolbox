from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

Document = str
DocumentMetadata = Dict[str, Any] # TODO surely not Any?

@dataclass
class QueryResult:
    _id: str
    document: Document
    metadata: DocumentMetadata
    distance: Optional[float] = None

QueryResults = List[QueryResult]

class AbstractDocumentDatabase(ABC):
    def __init__(self, database_name: str):
        self.database_name = database_name

    @abstractmethod
    def add_document(self, 
                     document: Document, 
                     metadata: Optional[DocumentMetadata] = None):
        pass

    @abstractmethod
    def query(self, 
              query: str, 
              metadata_filter: Optional[Any] = None, 
              max_results: Optional[int] = None) -> QueryResults:
        pass
