from random import randint

def random_number(server):
    @server.route("/random-number", methods=["GET"])
    def _random_number():
        """
        ---
        get:
            operationId: random_number
            summary: Get a random integer between 1 and 100.
            responses:
                200:
                    description: A random integer between 1 and 100.
                    content:
                        application/json:
                            schema:
                                type: integer
                                description: A random integer between 1 and 100.
        """
        return {"random_number": randint(1, 100)}

    return _random_number
