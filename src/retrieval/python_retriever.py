from .filesys_retriever import FilesysRetriever
from .extract import PythonFileExtractor, PythonProjectExtractor

class PythonRetriever(FilesysRetriever):
    def __init__(self, db):
        super().__init__(db, PythonFileExtractor(), PythonProjectExtractor())

    def search_for_function(self, fname, max_results=3):
        return self.query("", metadata_filter={"node_name": fname, "node_type": "function"}, max_results=max_results)

    def search_for_method(self, mname, max_results=3):
        return self.query("", metadata_filter={"node_name": mname, "node_type": "method"}, max_results=max_results)

    def search_for_class(self, cname, max_results=3):
        return self.query("", metadata_filter={"node_name": cname, "node_type": "class"}, max_results=max_results)

    def search_in_comments(self, query, max_results=3):
        return self.query(query, metadata_filter={"node_type": "comment"}, max_results=max_results)
