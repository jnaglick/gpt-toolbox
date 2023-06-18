from db import AbstractDocumentDatabase
from utils import console

from .document_retriever import DocumentRetriever, AbstractDocumentExtractor
from .extract import FileExtractor, DirectoryExtractor

class FilesysRetriever(DocumentRetriever):
    def __init__(self, document_database: AbstractDocumentDatabase, file_extractor: AbstractDocumentExtractor = None, dir_extractor: AbstractDocumentExtractor = None):
        super().__init__(document_database)

        if file_extractor is None:
            file_extractor = FileExtractor()

        if dir_extractor is None:
            dir_extractor = DirectoryExtractor()

        self.file_extractor = file_extractor
        self.dir_extractor = dir_extractor

    def load_file(self, source: str):
        items = self.file_extractor.extract(source)
        console.verbose(f"Extracted {len(items)} items from file: {source}")
        return self.index(items)

    def load_directory(self, source: str):
        items = self.dir_extractor.extract(source)
        console.verbose(f"Extracted {len(items)} items from directory: {source}")
        return self.index(items)

    def search_by_file_name(self, file_name, max_results=3):
        return self.query("", metadata_filter={"file_name": file_name}, max_results=max_results)

    def search_in_file_name(self, file_name, query, max_results=3):
        return self.query(query, metadata_filter={"file_name": file_name}, max_results=max_results)

    def search_by_file_path(self, file_path, max_results=3):
        return self.query("", metadata_filter={"file_path": file_path}, max_results=max_results)

    def search_in_file_path(self, file_path, query, max_results=3):
        return self.query(query, metadata_filter={"file_path": file_path}, max_results=max_results)
