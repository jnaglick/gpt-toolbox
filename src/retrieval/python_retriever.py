from .document_retriever import DocumentRetriever
from .extract import PythonExtractor, PythonFileExtractor, PythonProjectExtractor

class PythonRetriever(DocumentRetriever):
    def __init__(self, db):
        super().__init__(db, PythonExtractor())
        self.file_extractor = PythonFileExtractor()
        self.project_extractor = PythonProjectExtractor()

    def load_file(self, source: str):
        self.index(self.file_extractor.extract(source))

    def load_project(self, source: str):
        self.index(self.project_extractor.extract(source))

    def search_for_function(self, fname):
        return self.query("", metadata_filter={"node_name": fname, "node_type": "function"}, max_results=3)

    def search_for_method(self, mname):
        return self.query("", metadata_filter={"node_name": mname, "node_type": "method"}, max_results=3)

    def search_for_class(self, cname):
        return self.query("", metadata_filter={"node_name": cname, "node_type": "class"}, max_results=3)

    def search_comments(self, query):
        return self.query(query, metadata_filter={"node_type": "comment"}, max_results=3)

    def search_in_file(self, file_path, query):
        return self.query(query, metadata_filter={"file_path": file_path}, max_results=3)
