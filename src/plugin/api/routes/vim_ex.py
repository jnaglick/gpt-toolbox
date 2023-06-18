from utils import run_shell_command

from flask import jsonify, request, abort

def vim_ex(server):
    @server.route('/vim_ex', methods=['POST'])
    def _vim_ex():
        """
        ---
        post:
            operationId: vim_ex
            summary: Run a series of Vim commands in Ex mode on the user's machine and get the results.
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
                                type: array
                                items:
                                    $ref: '#/components/schemas/ShellResult'
                400:
                    description: Invalid input, a required field is missing
        """
        if not request.json or 'commands' not in request.json or 'file' not in request.json:
            abort(400)

        vim_commands = ' '.join(f'-c "{command}"' for command in request.json["commands"])
        vim_command = f'vim -es -u NONE {vim_commands} -c "wq" {request.json["file"]}'
        return jsonify(run_shell_command(vim_command)), 200
  
    return _vim_ex
