from flask import abort, request, jsonify

from utils import console
from retrieval import DocumentRetriever
from retrieval.extract import DocumentExtractor, FileExtractor, DirectoryExtractor, CsvFileExtractor, PythonFileExtractor, WebExtractor

class PluginRetriever(DocumentRetriever):
    def __init__(self, db):
        super().__init__(db)
        # this looks wonky, you'd expect to see a FileExtractor here. This is because the *FileExtractor classes has the condition() in them. Fix this.
        self.file_extractor = DocumentExtractor([
            FileExtractor(),
            CsvFileExtractor(),
            PythonFileExtractor(),
        ])
        self.directory_extractor = DirectoryExtractor([
            FileExtractor(),
            CsvFileExtractor(),
            PythonFileExtractor(),
        ])
        self.web_extractor = WebExtractor()

    def load_file(self, source: str):
        items = self.file_extractor.extract(source)
        console.verbose(f"Extracted {len(items)} items from file: {source}")
        return self.index(items)

    def load_directory(self, source: str):
        items = self.directory_extractor.extract(source)
        console.verbose(f"Extracted {len(items)} items from directory: {source}")
        return self.index(items)

    def load_url(self, source: str):
        items = self.web_extractor.extract(source)
        console.verbose(f"Extracted {len(items)} items from url: {source}")
        return self.index(items)

def memory(server):
    retriever = PluginRetriever(server.context.db)
    console.log(f"Plugin Retriever initialized with {retriever.db.collection.count()} items")

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
                memories = retriever.load(request.json['text'])

            if 'file_path' in request.json:
                memories = retriever.load_file(request.json['file_path'])

            if 'dir_path' in request.json:
                memories = retriever.load_directory(request.json['dir_path'])

            if 'url' in request.json:
                memories = retriever.load_url(request.json['url'])

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
        Remember something you memorized previously. If the user seems to be referencing something specific not in the chat history, try to find it with this. This makes you a much better assistant, so use it often!
        ---
        post:
            operationId: remember
            summary: Remember something you memorized previously. If the user seems to be referencing something specific not in the chat history, try to find it with this. This makes you a much better assistant, so use it often!
            requestBody:
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/RememberRequest"
            responses:
                200:
                    description: The memory that was found, if any. If nothing was found, try again with a much different query, or better yet, ask the user for clarification. If an error is returned, dont try again.
                    content:
                        application/json:
                            schema:
                                $ref: "#/components/schemas/RememberResult"
        """
        if not request.json or 'query' not in request.json:
            abort(400)

        result = retriever.query(request.json['query'])

        if len(result) == 0:
            return jsonify({
                "document": "No results found. Try another query.",
            })

        return jsonify({
            "document": result[0].document,
            "metadata": result[0].metadata,
        })

    return [_create_memory, _remember]
