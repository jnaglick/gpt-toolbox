import shlex

from flask import jsonify, request, abort

from utils import console, run_shell_command

def vim_ex_command(commands, file_path):
    commands = [shlex.quote(command) for command in commands] # shell escape each command
    vim_commands = ' '.join(f'-c "{command}"' for command in commands)
    vim_command = f'vim -es -u NONE {vim_commands} -c "wq" {file_path}'
    return vim_command

def vim_view(file_path):
    response = {
        'file_contents': [],
        'error': None,
    }

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        for i in range(len(lines)):
            response['file_contents'].append({'n': i+1, 't': lines[i]})
    except Exception as e:
        console.error(f"vim_view error: {e}")
        response['error'] = str(e)
    
    return response

def vim(server):
    @server.route('/vim_ex', methods=['POST'])
    def _vim_ex():
        """
        ---
        post:
            operationId: vim_ex
            summary: Run Vim command in Ex mode a file (final -c "wq" is implied) ALWAYS file_view to check line nums 1st! ONLY USE WHEN you cannot use a simpler edit_* tool
            requestBody:
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/VimExRequest'
            responses:
                200:
                    description: Vim Ex mode result
                    content:
                        application/json:
                            schema:
                                $ref: '#/components/schemas/ShellResult'
                400:
                    description: Invalid input. The request must be a JSON and contain 'command' and 'file_name' fields.
        """
        console.verbose(f"vim_ex request: {request.json}")

        if not request.json or 'command' not in request.json or 'file_name' not in request.json:
            abort(400)

        vim_command = vim_ex_command([request.json["command"]], request.json["file_name"])

        console.verbose(f"vim_ex running vim command")
        console.verbose(vim_command)

        return jsonify(run_shell_command(vim_command)), 200

    return _vim_ex
