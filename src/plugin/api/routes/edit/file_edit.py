from flask import jsonify, request, abort

import fileinput

from utils import console
from .helpers import get_file_view

def do_edit(file_name, operations):
    with fileinput.input(files=(file_name), inplace=True) as f:
        for i, line in enumerate(f, start=1):
            matching_operations = [op for op in operations if op['line_number'] == i]

            if len(matching_operations) == 0:
                print(line, end='')
                continue

            operation = matching_operations[0]

            if operation['op'] == 'replace':
                print(operation['new_text'], end='')
            elif operation['op'] == 'insert':
                print(operation['new_text'], end='')
                print(line, end='')
            elif operation['op'] == 'delete':
                continue
            else:
                print(line, end='')

def file_edit(server):
    @server.route('/edit/file_edit', methods=['POST'])
    def _file_edit():
        """
        ---
        post:
            operationId: file_edit
            summary: Edit a file with multiple operations. Each operation can be a replace, insert, or delete. ALWAYS file_view to check line nums 1st!
            requestBody:
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/FileEditRequest'
            responses:
                200:
                    description: File Edit result, how the file looks after the edit
                    content:
                        application/json:
                            schema:
                                $ref: '#/components/schemas/FileView'
                400:
                    description: Invalid input. The request must be a JSON and contain 'file_name', 'operations' fields.
        """
        console.verbose(f"file_edit request")
        console.verbose(request.json)

        if not request.json or 'file_name' not in request.json or 'operations' not in request.json:
            abort(400)

        for op in request.json['operations']:
            if 'line_number' not in op or 'op' not in op:
                abort(400, "All operations must contain 'line_number' and 'op'")
            
            if op['op'] in ['replace', 'insert'] and 'new_text' not in op:
                abort(400, "Replace and insert operations must all contain 'new_text'")
            
            matching_operations = [o for o in request.json['operations'] if op['line_number'] == o['line_number']]
            if len(matching_operations) > 1:
                abort(400, f"More than one operation for line {op['line_number']}")

        do_edit(request.json['file_name'], request.json['operations'])

        return jsonify(get_file_view(request.json['file_name'])), 200

    return _file_edit
