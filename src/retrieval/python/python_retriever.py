from ..document_retriever import DocumentRetriever
from .python_extractor import PythonExtractor

class PythonRetriever(DocumentRetriever):
    def __init__(self, db, extractor: PythonExtractor = None):
        if extractor is None:
            extractor = PythonExtractor()
        super().__init__(db, extractor)

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
