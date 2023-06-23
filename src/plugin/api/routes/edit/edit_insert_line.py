from flask import jsonify, request, abort

import fileinput

from utils import console
from .helpers import get_file_view

def do_insert(filename, line_num, text):
    with fileinput.input(files=(filename), inplace=True) as f:
        for i, line in enumerate(f, start=1):
            if i == line_num:
                print(text)
            print(line, end='')

def insert_line(server):
    @server.route('/edit/insert_line', methods=['POST'])
    def _insert_line():
        """
        ---
        post:
            operationId: edit_insert_line
            summary: EASIEST way to edit! Inserts new_text in file_name at line_number, moving other lines down. ALWAYS view_file to check line nums 1st! NEVER Use the Shell Tool To Edit!
            requestBody:
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/EditLineRequest'
            responses:
                200:
                    description: Line Insert result, how the file looks after the insert
                    content:
                        application/json:
                            schema:
                                $ref: '#/components/schemas/FileView'
                400:
                    description: Invalid input. ATTENTION Double check escape sequences in new_text! The request must be a JSON and contain 'line_number', 'new_text', 'file_name' fields.
        """
        console.verbose(f"insert_line request")
        console.verbose(request.json)

        if not request.json or 'line_number' not in request.json or 'new_text' not in request.json or 'file_name' not in request.json:
            abort(400)

        do_insert(request.json['file_name'], request.json['line_number'], request.json['new_text'])

        return jsonify(get_file_view(request.json['file_name'], request.json['line_number'])), 200

    return _insert_line
