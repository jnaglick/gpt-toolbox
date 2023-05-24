import uuid

import chromadb
from chromadb.config import Settings

from llm import generate_embedding

from .abstract_document_database import AbstractDocumentDatabase, QueryResult, QueryResults

def serialize_chroma_query_result(data) -> QueryResults:
    output = []
    for idx, item in enumerate(data["ids"][0]):
        output.append(
            QueryResult(
                _id=item,
                document=data["documents"][0][idx],
                metadata=data["metadatas"][0][idx],
                distance=data["distances"][0][idx],
            )
        )
    return output

def _generate_embedding(text):
    if isinstance(text, list):
        return [generate_embedding(t) for t in text]

    return [generate_embedding(text)]

class Chroma(AbstractDocumentDatabase):
    def __init__(self, database_name):
        # TODO dont hardcode to local
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=".chromadb"
        ))
        self.collection = self.client.get_or_create_collection(
            name=database_name,
            embedding_function=_generate_embedding,
            metadata={"hnsw:space": "cosine"}
        )

    def add_document(self, document, metadata=None):
        doc_id = str(uuid.uuid4())
        self.collection.add(documents=document, metadatas=metadata, ids=doc_id)

    def query(self, query, metadata_filter=None, max_results=None) -> QueryResults:
        args = dict(
            query_texts=[query],
        )

        if metadata_filter is not None:
            args["where"] = metadata_filter

        if max_results is not None:
            args["n_results"] = max_results
        
        result = self.collection.query(**args)
        
        return serialize_chroma_query_result(result)
