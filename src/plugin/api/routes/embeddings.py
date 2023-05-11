from flask import request, jsonify

from llm import generate_embedding

def create_embedding(server):
    @server.route("/create_embedding", methods=["POST"])
    def _create_embedding():
        """
        Create an embedding for the given input data.
        ---
        post:
            operationId: create_embedding
            summary: Create an embedding for the given input data.
            requestBody:
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/EmbeddingRequest"
            responses:
                200:
                    description: The created embedding.
                    content:
                        application/json:
                            schema:
                                $ref: "#/components/schemas/EmbeddingResult"
        """
        input_data = request.json.get("input_data")
        embedding = generate_embedding(input_data)
        return jsonify(embedding=embedding)

    return _create_embedding
