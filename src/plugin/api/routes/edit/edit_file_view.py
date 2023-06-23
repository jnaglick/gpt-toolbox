from flask import jsonify, request, abort

from utils import console
from .helpers import get_file_view

def file_view(server):
    @server.route('/edit/view_file', methods=['POST'])
    def _file_view():
        """
        ---
        post:
            operationId: edit_view_file
            summary: ATTENTION Its Dangerous To Edit A File Without Looking At It First! ALWAYS use this before editing a file to check line nums 1st!
            requestBody:
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/FileViewRequest'
            responses:
                200:
                    description: Vim View result - always check line numbers with this before editing!
                    content:
                        application/json:
                            schema:
                                $ref: '#/components/schemas/FileView'
                400:
                    description: Invalid input. The request must be a JSON and contain 'file_name' field.
        """
        console.verbose(f"file_view request: {request.json}")

        if not request.json or 'file_name' not in request.json:
            abort(400)

        return jsonify(get_file_view(request.json['file_name'])), 200

    return _file_view
