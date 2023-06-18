from utils import run_shell_command

from flask import jsonify, request, abort

def vim_ex(server):
    @server.route('/vim_ex', methods=['POST'])
    def _vim_ex():
        """
        ---
        post:
            operationId: vim_ex
            summary: Run a series of Vim commands in Ex mode on the user's machine and get the results (the final "wq" is supplied automatically). ATTENTION ALWAYS Use This To Edit Files - NEVER Use the Shell Tool!
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
                    description: Invalid input. The request must be a JSON and contain 'commands' and 'file_name' fields.
        """
        if not request.json or 'commands' not in request.json or 'file_name' not in request.json:
            abort(400)

        vim_commands = ' '.join(f'-c "{command}"' for command in request.json["commands"])
        vim_command = f'vim -es -u NONE {vim_commands} -c "wq" {request.json["file_name"]}'
        return jsonify(run_shell_command(vim_command)), 200
  
    return _vim_ex
