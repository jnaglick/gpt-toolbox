from utils import current_datetime

def datetime(server):
    @server.route('/datetime', methods=['GET'])
    def _dt():
        """
        ---
        get:
            operationId: datetime
            summary: Get the current datetime in the user's local timezone. Before answering questions related to the current datetime, you can use this to know it exactly in order to give a better answer.
            responses:
                200:
                    description: The current datetime in the user's local timezone.
                    content:
                        application/json:
                            schema:
                                type: string
                                description: The current datetime in the user's local timezone.
        """
        return current_datetime()

    return _dt