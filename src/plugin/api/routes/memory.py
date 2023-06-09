from flask import abort, request, jsonify
from db import DocumentMetadata

from utils import console
from retrieval import DocumentRetriever, FilesysRetriever
from retrieval.extract import DocumentExtractor, FileExtractor, DirectoryExtractor, CsvFileExtractor, PythonFileExtractor, WebExtractor

class OtherFileExtractor(FileExtractor):
    # capture non-csv and non-python so we dont redundantly index
    def condition(self, source: str, additional_metadata: DocumentMetadata) -> bool:
        return not CsvFileExtractor.s_condition(source, additional_metadata)\
            and not PythonFileExtractor.s_condition(source, additional_metadata)

# short term: used for files and urls
class ShortTermRetriever(FilesysRetriever):
    def __init__(self, db):
        super().__init__(db, DocumentExtractor([
            OtherFileExtractor(),
            CsvFileExtractor(),
            PythonFileExtractor(),
        ]), DirectoryExtractor([
            OtherFileExtractor(),
            CsvFileExtractor(),
            PythonFileExtractor(),
        ]))
        self.web_extractor = WebExtractor()

    def load_url(self, source: str):
        items = self.web_extractor.extract(source)
        console.verbose(f"Extracted {len(items)} items from url: {source}")
        return self.index(items)

# long term: used for 'text'. currently a placeholder class
class LongTermRetriever(DocumentRetriever):
    def __init__(self, db):
        super().__init__(db)

def memory(server):
    short_term = ShortTermRetriever(db=server.context.db)
    long_term = LongTermRetriever(db=server.context.db_long_term)

    console.log(f"Plugin memory initialized. short_term: {short_term.db.collection.count()}, long_term: {long_term.db.collection.count()}")

    @server.route("/create_memory", methods=["POST"])
    def _create_memory():
        """
        Memorizes something. It's very important to use the right request param so the system knows how to memorize it. Before you memorize, think step by step about exactly what to memorize and how.
        ---
        post:
            operationId: create_memory
            summary: Memorizes something. It's very important to use the right request param so the system knows how to memorize it. Before you memorize, think step by step about exactly what to memorize and how.
            requestBody:
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/MemorizeRequest"
            responses:
                200:
                    description: What happened when creating the memory.
                    content:
                        application/json:
                            schema:
                                $ref: "#/components/schemas/MemorizeResult"
        """
        console.verbose(f"create_memory: {request.json}")

        if not request.json or (
            'text' not in request.json and 
            'url' not in request.json and 
            'file_path' not in request.json and 
            'dir_path' not in request.json
        ):
            abort(400)

        try:
            memories = []

            if 'text' in request.json:
                memories = long_term.load(request.json['text'])

            if 'file_path' in request.json:
                memories = short_term.load_file(request.json['file_path'])

            if 'dir_path' in request.json:
                memories = short_term.load_directory(request.json['dir_path'])

            if 'url' in request.json:
                memories = short_term.load_url(request.json['url'])

            return jsonify({
                "returncode": 0,
                "count": len(memories),
            })
        except Exception as e:
            console.error(e)
            return jsonify({
                "returncode": 1,
                "error": str(e),
            })

    @server.route("/remember", methods=["POST"])
    def _remember():
        """
        Recalls important things, code and data from the local filesystem and remote locations, and your own past notes. This functionality makes you a MUCH Better Assistant, so use it as often as possible!
        ---
        post:
            operationId: remember
            summary: Recalls important things, code and data from the local filesystem and remote locations, and your own past notes. This functionality makes you a MUCH Better Assistant, so use it as often as possible!
            requestBody:
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/RememberRequest"
            responses:
                200:
                    description: The memory that was found, if any. If nothing was found, try again with a much different query.
                    content:
                        application/json:
                            schema:
                                $ref: "#/components/schemas/RememberResult"
        """
        if not request.json or 'query' not in request.json:
            abort(400)

        short_term_result = short_term.query(request.json['query'], max_results=5)
        long_term_result = long_term.query(request.json['query'], max_results=5)

        console.verbose(f"Short term results: {len(short_term_result)}")
        console.verbose(f"Long term results: {len(long_term_result)}")

        result = short_term_result + long_term_result

        if len(result) == 0:
            return jsonify({
                "document": "No results found. ATTENTION: Please try again with a much different query.",
            })

        return jsonify({
            "document": result[0].document,
            "metadata": result[0].metadata,
        })

    return [_create_memory, _remember]
