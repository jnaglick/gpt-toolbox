from flask import request, jsonify

def create_memory(server):
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
                            $ref: "#/components/schemas/MemoryRequest"
            responses:
                200:
                    description: What happened when creating the memory.
                    content:
                        application/json:
                            schema:
                                $ref: "#/components/schemas/MemoryResult"
        """

        print(request.json)
        print(server.context)

        return jsonify({
            "returncode": 0,
        })

    return _create_memory
